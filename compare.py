import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("directory", help="Directory to compare current working directory with")
parser.add_argument("--directories", "-d", help="Compare directories only")
args = parser.parse_args()

directory = args.directory
cwd_walks = list(os.walk(os.getcwd()))
dir_walks = list(os.walk(directory))
excludes = ["$RECYCLE.BIN", "sys_exc"]

missing = []
# print([os.path.splitdrive(d[0])[1].replace(os.path.splitdrive(directory)[1], "") for d in dir_walks][1])

for w in cwd_walks:
    wdir = os.path.splitdrive(w[0])[1]
    if w[0] != os.getcwd():
        if wdir not in [os.path.splitdrive(d[0])[1].replace(os.path.splitdrive(directory)[1], "") for d in dir_walks]:
            dont_print = []
            for exclude in excludes:
                if exclude in wdir:
                    dont_print.append(w[0])
            if w[0] not in dont_print:
                print(w[0])
