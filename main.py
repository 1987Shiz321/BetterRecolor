import os
import shutil
import time

from btrc.config import (
    ASSETS_DIR,
    BRLAN_JSON5_DIR,
    BRLYT_JSON5_DIR,
    EDITED_BRLAN_DIR,
    EDITED_BRLYT_DIR,
    WUJ5_SCRIPT,
)
from btrc.brlan import select_color_rule, update_tev_colors
from btrc.brlyt import apply_tev_colors
from btrc.cleanup import move_all_files, remove_json5_files
from btrc.colors import get_outline_color_from_user, run_color_input_flow
from btrc.encode import encode_json5_files
from btrc.i18n import set_locale, t
from btrc.json5_io import list_json5_files, read_json5, write_json5


def choose_locale():
    choice = input("Language / 言語 (ja/en) [ja]: ").strip().lower()
    if choice not in {"ja", "en"}:
        choice = "ja"
    set_locale(choice)
    return choice


def print_paths():
    print(t("using_assets_dir").format(path=ASSETS_DIR))
    print(t("using_tmp_brlyt_dir").format(path=BRLYT_JSON5_DIR))
    print(t("using_tmp_brlan_dir").format(path=BRLAN_JSON5_DIR))
    print(t("using_wuj5_script").format(path=WUJ5_SCRIPT))
    print(t("using_edited_brlyt_dir").format(path=EDITED_BRLYT_DIR))
    print(t("using_edited_brlan_dir").format(path=EDITED_BRLAN_DIR))


def copy_all(src_dir, dst_dir):
    src_dir = str(src_dir)
    dst_dir = str(dst_dir)
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        dst_root = os.path.join(dst_dir, rel) if rel != "." else dst_dir
        os.makedirs(dst_root, exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(root, f), os.path.join(dst_root, f))


def reset_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def main():
    start_time = time.perf_counter()
    choose_locale()
    print_paths()
    print(t("btrc_start"))
    color_map = run_color_input_flow()

    default_free_text = (220, 220, 220)
    default_select_text = (255, 255, 255)
    free_outline = get_outline_color_from_user("free", "#282828")
    select_outline = get_outline_color_from_user("select", "#787878")
    text_free_colors = (default_free_text, free_outline)
    text_select_colors = (default_select_text, select_outline)

    print(t("reset_tmp_and_edited"))
    reset_dir(BRLYT_JSON5_DIR)
    reset_dir(BRLAN_JSON5_DIR)
    reset_dir(EDITED_BRLYT_DIR)
    reset_dir(EDITED_BRLAN_DIR)

    print(t("copy_assets_to_tmp"))
    copy_all(ASSETS_DIR / "BRLYT", BRLYT_JSON5_DIR)
    copy_all(ASSETS_DIR / "BRLAN", BRLAN_JSON5_DIR)

    brlyt_files = list_json5_files(BRLYT_JSON5_DIR)
    print(t("brlyt_json5_count").format(count=len(brlyt_files)))
    text_black_rgb, text_white_rgb = (text_select_colors[1], text_select_colors[0])
    arrow_black_rgb, arrow_white_rgb = color_map["color_yajirushi"]
    color_map.update(
        {
            "text": (text_black_rgb, text_white_rgb),
            "active_text": (text_black_rgb, text_white_rgb),
            "chara02": (arrow_white_rgb, arrow_black_rgb),
        }
    )

    for i, path in enumerate(brlyt_files, 1):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        new_text = apply_tev_colors(text, color_map)
        if new_text is not None:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
        if i == 1 or i % 50 == 0 or i == len(brlyt_files):
            print(
                t("brlyt_update_progress").format(
                    current=i, total=len(brlyt_files)
                )
            )

    brlan_files = list_json5_files(BRLAN_JSON5_DIR)
    print(t("brlan_json5_count").format(count=len(brlan_files)))
    for i, path in enumerate(brlan_files, 1):
        data = read_json5(path)
        rule = select_color_rule(path, text_free_colors, text_select_colors)
        if rule is None:
            continue
        (start_outline, start_text), (end_outline, end_text) = rule
        updated = update_tev_colors(data, start_outline, start_text, end_outline, end_text)
        write_json5(path, updated)
        if i == 1 or i % 50 == 0 or i == len(brlan_files):
            print(
                t("brlan_update_progress").format(
                    current=i, total=len(brlan_files)
                )
            )

    print(t("encode_json5"))
    encode_json5_files(brlyt_files + brlan_files, WUJ5_SCRIPT)
    print(t("cleanup_json5"))
    remove_json5_files(brlyt_files + brlan_files)

    print(t("move_tmp_to_edited"))
    move_all_files(BRLYT_JSON5_DIR, EDITED_BRLYT_DIR)
    move_all_files(BRLAN_JSON5_DIR, EDITED_BRLAN_DIR)
    elapsed = time.perf_counter() - start_time
    print(t("btrc_done").format(elapsed=elapsed))


if __name__ == "__main__":
    main()
