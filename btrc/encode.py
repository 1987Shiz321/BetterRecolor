import subprocess
from .i18n import t


def encode_json5_files(files, wuj5_script):
    if not files:
        print(t("no_json5"))
        return
    for file_path in files:
        command = ["python", str(wuj5_script), "encode", file_path]
        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"エラー: {file_path}")
            print(e.stderr)
    print(t("done_encode"))
