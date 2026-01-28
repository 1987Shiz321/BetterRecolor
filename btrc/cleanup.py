import os
import shutil


def remove_json5_files(files):
    for path in files:
        os.remove(path)


def move_all_files(src_dir, dst_dir):
    for name in os.listdir(src_dir):
        src = os.path.join(src_dir, name)
        dst = os.path.join(dst_dir, name)
        shutil.move(src, dst)
