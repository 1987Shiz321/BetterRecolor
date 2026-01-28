import os
import shutil

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
from btrc.json5_io import list_json5_files, read_json5, write_json5

print(f"Using Assets directory: {ASSETS_DIR}")
print(f"Using temporary BRLYT JSON5 directory: {BRLYT_JSON5_DIR}")
print(f"Using temporary BRLAN JSON5 directory: {BRLAN_JSON5_DIR}")
print(f"Using WUJ5 script: {WUJ5_SCRIPT}")
print(f"Using Edited BRLYT directory: {EDITED_BRLYT_DIR}")
print(f"Using Edited BRLAN directory: {EDITED_BRLAN_DIR}")

def copy_all(src_dir, dst_dir):
    src_dir = str(src_dir)
    dst_dir = str(dst_dir)
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        dst_root = os.path.join(dst_dir, rel) if rel != "." else dst_dir
        os.makedirs(dst_root, exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(root, f), os.path.join(dst_root, f))


def main():
    color_map = run_color_input_flow()

    default_free_text = (220, 220, 220)
    default_select_text = (255, 255, 255)
    free_outline = get_outline_color_from_user("free", "#282828")
    select_outline = get_outline_color_from_user("select", "#787878")
    text_free_colors = (default_free_text, free_outline)
    text_select_colors = (default_select_text, select_outline)

    os.makedirs(BRLYT_JSON5_DIR, exist_ok=True)
    os.makedirs(BRLAN_JSON5_DIR, exist_ok=True)
    copy_all(ASSETS_DIR / "BRLYT", BRLYT_JSON5_DIR)
    copy_all(ASSETS_DIR / "BRLAN", BRLAN_JSON5_DIR)

    brlyt_files = list_json5_files(BRLYT_JSON5_DIR)
    text_black_rgb, text_white_rgb = (text_select_colors[1], text_select_colors[0])
    arrow_black_rgb, arrow_white_rgb = color_map["color_yajirushi"]
    color_map.update(
        {
            "text": (text_black_rgb, text_white_rgb),
            "active_text": (text_black_rgb, text_white_rgb),
            "chara02": (arrow_white_rgb, arrow_black_rgb),
        }
    )

    for path in brlyt_files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        new_text = apply_tev_colors(text, color_map)
        if new_text is not None:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)

    brlan_files = list_json5_files(BRLAN_JSON5_DIR)
    for path in brlan_files:
        data = read_json5(path)
        rule = select_color_rule(path, text_free_colors, text_select_colors)
        if rule is None:
            continue
        (start_outline, start_text), (end_outline, end_text) = rule
        updated = update_tev_colors(data, start_outline, start_text, end_outline, end_text)
        write_json5(path, updated)

    encode_json5_files(brlyt_files + brlan_files, WUJ5_SCRIPT)
    remove_json5_files(brlyt_files + brlan_files)

    os.makedirs(EDITED_BRLYT_DIR, exist_ok=True)
    os.makedirs(EDITED_BRLAN_DIR, exist_ok=True)
    move_all_files(BRLYT_JSON5_DIR, EDITED_BRLYT_DIR)
    move_all_files(BRLAN_JSON5_DIR, EDITED_BRLAN_DIR)


if __name__ == "__main__":
    main()
