import os
import socket

import ftputil
import ftputil.session

SOURCE_DIR = "X:/"

LOCAL_IP = str(socket.gethostbyname(socket.gethostname()))
FTP_IP = ".".join(LOCAL_IP.split(".")[0:3]) + ".112"

sf = ftputil.session.session_factory(port=2221, debug_level=0)
ftp = ftputil.FTPHost(FTP_IP, user="android", password="android", session_factory=sf)
ftp.listdir(ftp.curdir)

TARGET_DIR = ftp.curdir + "/uploads"
failed = []

def get_full_path(directory):
    return os.path.abspath(directory)


def create_dir(path, change_to=False, in_target=False):
    if in_target:
        path = path[1:] if path[0] == "/" else path
        path = TARGET_DIR + "/" + path

    #print("Creating ", path)

    if not ftp.path.isdir(path):
        ftp.makedirs(path)

    if change_to:
        ftp.chdir(path)

    #print(ftp.curdir)


def upload_file(source, path, in_target=False):
    if in_target:
        path = path[1:] if path[0] == "/" else path
        path = TARGET_DIR + "/" + path

    print("Uploading to\n", path)
    if ftp.upload_if_newer(source, path):
        print("Uploading to\n", path)
    else:
        print("Skipped\n", source)


def upload_directory(path):
    dir_name = path[0]
    sub_dirs = path[1]
    files = path[2]

    create_dir(os.path.basename(dir_name), in_target=True)

    for walk in os.walk(dir_name):
        if not walk[1]:
            create_dir(os.path.normpath(os.path.splitdrive(walk[0])[1]).replace("\\", "/"), in_target=True)

    for walk in os.walk(dir_name):
        for f in walk[2]:
            source = os.path.normpath(os.path.join(walk[0], f)).replace("\\", "/")
            target = os.path.normpath(os.path.splitdrive(os.path.join(walk[0], f))[1]).replace("\\", "/")
            try:
                upload_file(source, target, True)
            except:
                failed.append(source)

create_dir(TARGET_DIR)

for path in os.walk(SOURCE_DIR):
    if "upload" in path[2] + path[1]:
        upload_directory(path)

with open("failed.txt", "w") as f:
    for s in failed:
        f.writeline(s)
