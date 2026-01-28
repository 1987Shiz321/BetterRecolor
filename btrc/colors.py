import re
from colr import color
from .i18n import t

HEX_PATTERN = re.compile(r"^#([A-Fa-f0-9]{6})$")


def get_valid_hex_color(prompt):
    while True:
        value = input(prompt).strip()
        if HEX_PATTERN.match(value):
            return value
        print(t("invalid_hex"))


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return "#%02X%02X%02X" % (r, g, b)


def print_color(name, rgb):
    print(f"{name}: {rgb} {color('■', fore=rgb_to_hex(*rgb))}")


def get_outline_color_from_user(state_name, default_hex):
    while True:
        user_input = input(
            t("prompt_outline_color").format(
                state_name=state_name, default_hex=default_hex
            )
        ).strip()
        if user_input == "":
            user_input = default_hex
        if HEX_PATTERN.match(user_input):
            return tuple(int(user_input[i : i + 2], 16) for i in (1, 3, 5))
        print(t("invalid_hex"))


color_presets = {
    "fuchi_pattern2": {"black": "#ffffff", "white": "#000000"},
    "color_base2": {"black": "#434343", "white": "#434343"},
    "black_base2": {"black": "#434343", "white": "#434343"},
    "pikapika": {"black": "#ffffff", "white": "#ffffff"},
    "color_yajirushi": {"black": "#FFFFFF", "white": "#C8C8C8"},
    "ability_graph2": {"black": "#434343", "white": "#434343"},
    "black_pt00": {"black": "#434343", "white": "#434343"},
    "black_pt01": {"black": "#434343", "white": "#434343"},
}


def print_preset(name):
    preset = color_presets[name]
    print(t("preset_title").format(name=name))
    print(
        t("preset_black").format(
            value=preset["black"], block=color("■", fore=preset["black"])
        )
    )
    print(
        t("preset_white").format(
            value=preset["white"], block=color("■", fore=preset["white"])
        )
    )


def get_custom_color_and_update(name):
    print(t("section_color_settings").format(name=name))
    default_black = color_presets[name]["black"]
    default_white = color_presets[name]["white"]
    print(
        t("defaults_black_white").format(
            default_black=default_black, default_white=default_white
        )
    )

    black = get_valid_hex_color(t("prompt_black").format(name=name))
    white = get_valid_hex_color(t("prompt_white").format(name=name))

    color_presets[name]["black"] = black
    color_presets[name]["white"] = white

    if name == "color_base2":
        color_presets["black_base2"]["black"] = black
        color_presets["black_base2"]["white"] = white
        color_presets["pikapika"]["black"] = black
        color_presets["pikapika"]["white"] = white
    elif name == "ability_graph2":
        color_presets["black_pt00"]["black"] = black
        color_presets["black_pt00"]["white"] = white
        color_presets["black_pt01"]["black"] = black
        color_presets["black_pt01"]["white"] = white

    return hex_to_rgb(black), hex_to_rgb(white)


def run_color_input_flow():
    fuchi_black_rgb, fuchi_white_rgb = get_custom_color_and_update("fuchi_pattern2")
    base_black_rgb, base_white_rgb = get_custom_color_and_update("color_base2")
    arrow_black_rgb, arrow_white_rgb = get_custom_color_and_update("color_yajirushi")
    ability_black_rgb, ability_white_rgb = get_custom_color_and_update("ability_graph2")

    print(t("section_color_preview"))
    for preset_name in color_presets:
        print_preset(preset_name)

    color_map = {
        "fuchi_pattern2": (fuchi_black_rgb, fuchi_white_rgb),
        "color_base2": (base_black_rgb, base_white_rgb),
        "black_base2": (base_black_rgb, base_white_rgb),
        "pikapika": (base_black_rgb, base_white_rgb),
        "color_yajirushi": (arrow_black_rgb, arrow_white_rgb),
        "ability_graph2": (ability_black_rgb, ability_white_rgb),
        "black_pt00": (ability_black_rgb, ability_white_rgb),
        "black_pt01": (ability_black_rgb, ability_white_rgb),
    }
    return color_map
