#!/usr/bin/env python3

import argparse
import os

from pprint import PrettyPrinter

from woomba import fileteleporter as ftp


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("src_dir", metavar="src-dir", type=str, help="directory to sync files from")
    parser.add_argument("target_dir", metavar="target-dir", type=str, help="directory to sync files to")
    parser.add_argument("-a", "--add-only", action="store_true", help="perform only copy operations (no deletions)")
    # parser.add_argument("-i", "--interactive", action="store_true", help="require confirmation before adding/deleting files")
    parser.add_argument("-n", "--no-commit", action="store_true", help="do not make any changes and print out operations that will be performed")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose logging")
    return parser


def main():
    # First cut -- sync to backup
    parser = get_argument_parser()
    args = parser.parse_args()

    if not os.path.isdir(args.src_dir) or not os.path.isdir(args.target_dir):
        print("Forgeddaboutit")
        return

    dir_comp = ftp.shallow_diff_directories(args.src_dir, args.target_dir)
    operations = ftp.generate_sync_operations(dir_comp)

    if args.no_commit:
        print(str(operations))
    else:
        print("Not supported yet!")
        


if __name__ == "__main__":
    main()