#!/usr/bin/env python3

import argparse
import os
from shutil import copyfile

def find_all_files(root):
    all_files = []
    for root, dirs, files in os.walk(root):
        all_files += files
        for d in dirs:
            # Change to regex ignore list
            files += find_all_files(os.path.join(root, d))
    return all_files

def find_sync_files(target_dir, src_dir):
    """ Return a list of files to be added and deleted """
    
    src_files = find_all_files(src_dir)
    target_files = find_all_files(target_dir)

def execute_changes(changelist):
    pass

def get_changelist_str(description, files, line_format=None):
    """ Return string summarizing changes """
    return description

def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("target_dir", metavar="target-dir", type=str, help="directory to sync files to")
    parser.add_argument("src_dir", metavar="src-dir", type=str, help="directory to sync files from")
    parser.add_argument("-i", "--interactive", action="store_true", help="require confirmation before adding/deleting files")
    parser.add_argument("-l", "--list-changes", action="store_true", help="list changes that would be made")
    parser.add_argument("-a", "--add-only", action="store_true", help="perform only copy operations (no deletions)")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose logging")
    return parser

def main():
    # First cut -- sync to backup
    parser = get_argument_parser()
    args = parser.parse_args()

    sync_files = find_sync_files(args.target_dir, args.src_dir)

    if args.list_changes:
        print(str(sync_files))
    else:
        print("")

if __name__ == "__main__":
    main()