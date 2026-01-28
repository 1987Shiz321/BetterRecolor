import i18n

# 翻訳ファイルのパスを追加
i18n.load_path.append("./i18n")

# デフォルトのロケールを設定
def set_locale(locale: str):
    i18n.set('locale', locale)