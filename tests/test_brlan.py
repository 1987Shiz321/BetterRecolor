from btrc.brlan import select_color_rule, update_tev_colors


def build_sample_data():
    return {
        "sections": [
            {
                "contents": [
                    {
                        "name": "text",
                        "animations": [
                            {
                                "targets": [
                                    {
                                        "kind": "tev color 0 r",
                                        "keys": [
                                            {"frame": 0.0, "value": 0},
                                            {"frame": 1.0, "value": 0},
                                        ],
                                    },
                                    {
                                        "kind": "tev color 1 r",
                                        "keys": [
                                            {"frame": 0.0, "value": 0},
                                            {"frame": 1.0, "value": 0},
                                        ],
                                    },
                                ]
                            }
                        ],
                    }
                ]
            }
        ]
    }


def test_update_tev_colors_start_and_end():
    data = build_sample_data()
    start_outline = (9, 9, 9)
    start_text = (1, 1, 1)
    end_outline = (8, 8, 8)
    end_text = (2, 2, 2)

    updated = update_tev_colors(data, start_outline, start_text, end_outline, end_text)
    targets = updated["sections"][0]["contents"][0]["animations"][0]["targets"]

    tev0 = next(t for t in targets if t["kind"] == "tev color 0 r")
    tev1 = next(t for t in targets if t["kind"] == "tev color 1 r")

    assert tev0["keys"][0]["value"] == start_text[0]
    assert tev0["keys"][1]["value"] == end_text[0]
    assert tev1["keys"][0]["value"] == start_outline[0]
    assert tev1["keys"][1]["value"] == end_outline[0]


def test_select_color_rule_variants():
    free = ((1, 1, 1), (2, 2, 2))
    select = ((3, 3, 3), (4, 4, 4))

    assert select_color_rule("abc_free_to_select.json5", free, select) == (free, select)
    assert select_color_rule("abc_select_to_free.json5", free, select) == (select, free)
    assert select_color_rule("abc_free.json5", free, select) == (free, free)
    assert select_color_rule("abc_select.json5", free, select) == (select, select)
    assert select_color_rule("fuchi_check_loop.json5", free, select) is None
