import os
import hashlib

correct_files = r"E:/Stuff"
rename_files = r"F:/Stuff"

hash_names = {}

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

for file in os.listdir(correct_files):
    hash_names[md5(os.path.join(correct_files, os.path.basename(file)))] = os.path.basename(file)
    print(os.path.basename(file))

for file in os.listdir(rename_files):
    new_name = hash_names[md5(os.path.join(rename_files, os.path.basename(file)))]
    print(file, "->", new_name)
    os.rename(os.path.join(rename_files, file), os.path.join(rename_files, new_name))
