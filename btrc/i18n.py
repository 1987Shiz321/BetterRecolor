MESSAGES = {
    "ja": {
        "invalid_hex": "無効なカラーコードです。#RRGGBB の形式で入力してください。",
        "no_json5": "指定されたディレクトリにJSON5ファイルが存在しません。",
        "done_encode": "すべてのJSON5ファイルをエンコードしました！",
    },
    "en": {
        "invalid_hex": "Invalid color code. Use #RRGGBB.",
        "no_json5": "No JSON5 files found in the directory.",
        "done_encode": "All JSON5 files were encoded!",
    },
}

LANG = "ja"


def t(key):
    return MESSAGES.get(LANG, {}).get(key, key)
