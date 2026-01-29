# BetterRecolor

MKWii向けのUI編集ツールです。Google Colabでもローカル環境でも使用できます。

## 概要

マリオカートWiiで表示されるボタンやテキストの**色を一括で編集できるツール**です。  
JSON5形式にデコードされたファイルを編集し、BRLYT（レイアウトファイル）とBRLAN（アニメーションファイル）としてエンコードします。

## はじめに

Google Colaboratoryを初めて利用する方は、以下の動画を参考にしてください。

- [【研究生活ハック】Google Colabの使い方](https://youtu.be/j2p9pLGHRPg?si=_Q9bPEW3dKxtqkcs)

### Colabの利点

- **実行環境に依存しない**：  
  クラウド上の割り当てられたマシンで処理を実行するため、個人のPC環境に左右されません。
- **環境構築不要**：  
  Pythonの知識がない方でも、セルをクリックするだけでツールを利用できます。

## 使い方

セルを順番に実行するだけで簡単に使用できます。  
すべてのファイルの実行が完了したら、以下の手順でファイルをダウンロードしてください。

1. **Googleドライブを開く**：  
   `マイドライブ` → `8MeTools` → `BetterRecolor` → `EditedBRLYT` と `EditedBRLAN` フォルダを選択して保存します。

2. **ファイルの適用**：  
   ダウンロードしたzipファイルを展開し、`"〇〇.d"`というフォルダをご自身のアセットに上書きコピーします。

3. **動作確認**：  
   wszstで圧縮してszs形式に変換後、ゲームを起動して動作を確認してください。

## ローカルでの実行

Google Colab以外の環境でも実行できます。`Assets` などのフォルダ構成はそのままにしてください。

1. **依存関係のインストール**  
   `pip install -r requirements.txt`

2. **実行**  
   `python main.py`

3. **言語の選択**  
   起動時に `Language / 言語 (ja/en) [ja]:` と表示されるので、`ja` または `en` を入力してください。

4. **出力先**  
   完了後、`EditedBRLYT` と `EditedBRLAN` に出力されます。

## 開発者向け

### Lint / Test

```sh
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest
```

### リリース運用（CalVer）

日付+連番のバージョン形式を使用します。例: `26.01.28.1`

1. バージョン更新

   ```sh
   python scripts/bump_version.py
   ```

2. タグ作成

   ```sh
   python scripts/bump_version.py --tag
   ```

3. タグ作成 + push（CI成功後にReleaseが作成されます）

   ```sh
   python scripts/bump_version.py --tag --push
   ```

### CI / Release 条件

- CI: `push` と `pull_request` で `ruff check .` と `pytest` が実行されます。
- Release: CIが成功したコミットに付いた `v*` タグ（例: `v26.01.28.1`）がある場合のみ作成されます。

## よくある質問

### Q. 実行するセルの順番を間違えてしまった場合、どうすればよいですか？

**A.** Colabの使用に自信がない場合は、次の手順を実行してやり直してください。\
画面左上のメニューバーから「**ランタイム**」を選択し、「**ランタイムを接続解除して削除**」を実行してください。セルの実行順序に注意して、最初から実行してください。

### Q. マルチプレイ時、一部のボタンが指定された色に変わっていません。

**A.** マルチプレイヤーでのボタンカラー変更は、プレイヤーごとの識別が困難になるため、意図的に変更していません。ご了承ください。

### Q. 今後、BRLYTフォルダとBRLANフォルダをまとめる仕様に変わりますか？

**A.** 現段階では予定していません。これは「どちらか一方を編集したい」という状況下で、別々にしておくと都合がよいからです。

## 不具合について

- GitHubのIssuesにてお知らせください。

## Third-Party

このリポジトリには MIT ライセンスの[wuj5](https://github.com/stblr/wuj5)を同梱しています。ライセンスは `wuj5/LICENSE` を参照してください。
