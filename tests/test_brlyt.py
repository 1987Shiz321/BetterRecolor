from pathlib import Path
import re

import pytest

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


def test_apply_tev_colors_real_data():
    data_path = Path("Assets/BRLYT/Globe.d/message_window/blyt/common_w004_menu.brlyt.json5")
    if not data_path.exists():
        pytest.skip("Sample BRLYT data not found")

    json_text = data_path.read_text(encoding="utf-8")
    color_map = {"text": ((11, 22, 33), (201, 202, 203))}
    updated = apply_tev_colors(json_text, color_map)
    assert updated is not None

    pattern = re.compile(
        r'(\s*"name": "text".*?("tev color 1 a": \d+))',
        re.DOTALL,
    )
    match = re.search(pattern, updated)
    if match is None:
        pytest.skip('No "text" block with tev colors found in sample')
    block_text = match.group(1)
    assert '"tev color 0 r": 11' in block_text
    assert '"tev color 0 g": 22' in block_text
    assert '"tev color 0 b": 33' in block_text
    assert '"tev color 1 r": 201' in block_text
    assert '"tev color 1 g": 202' in block_text
    assert '"tev color 1 b": 203' in block_text
