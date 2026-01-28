try:
    import i18n as _i18n
except Exception:
    _i18n = None

if _i18n is not None:
    _i18n.load_path.append("./i18n")

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


def set_locale(locale: str):
    global LANG
    LANG = locale
    if _i18n is not None:
        _i18n.set("locale", locale)


def t(key: str):
    if _i18n is not None:
        try:
            return _i18n.t(key)
        except Exception:
            pass
    return MESSAGES.get(LANG, {}).get(key, key)
