from btrc.brlyt import apply_tev_colors


def test_apply_tev_colors_updates_block():
    json_text = """
    {
      "name": "text",
      "tev color 0 r": 1,
      "tev color 0 g": 2,
      "tev color 0 b": 3,
      "tev color 1 r": 4,
      "tev color 1 g": 5,
      "tev color 1 b": 6,
      "tev color 1 a": 255
    }
    """
    color_map = {"text": ((10, 20, 30), (200, 210, 220))}

    updated = apply_tev_colors(json_text, color_map)

    assert '"tev color 0 r": 10' in updated
    assert '"tev color 0 g": 20' in updated
    assert '"tev color 0 b": 30' in updated
    assert '"tev color 1 r": 200' in updated
    assert '"tev color 1 g": 210' in updated
    assert '"tev color 1 b": 220' in updated


def test_apply_tev_colors_returns_none_when_no_match():
    json_text = '{"name": "other", "tev color 1 a": 255}'
    assert apply_tev_colors(json_text, {}) is None
