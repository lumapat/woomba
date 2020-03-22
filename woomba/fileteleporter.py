from enum import Enum
from filecmp import dircmp
from shutil import copy2, copytree, rmtree
from typing import Any, Dict, List

import os

def get_all_files(root: str):
    """ Get all files per directory """
    return {d: set(files) for d, _, files in os.walk(root)}


def shallow_diff_directories(base_dir: str, target_dir: str):
    """ Shallow compare contents of two directories (recursively)

        Added files are files only in target directory.
        Removed files are files only in base directory.
    """
    return dircmp(base_dir, target_dir)


def sync_contents(
    src_dir: str,
    target_dir: str,
    operations: Dict[str, List[str]]
):
    """ Sync contents of into a directory """

    # 1st arg is unused
    def rmdir(_, d):
        shutil.rmtree(d)

    def rmfile(_, f):
        os.remove(f)

    op_map = {
        "copy-file": shutil.copy2,
        "copy-dir": shutil.copytree,
        "rm-file": rmfile,
        "rm-dir": rmdir
    }

    failed_ops = 0
    total_ops = 0

    for op in operations:
        contents = operations[op]
        contents.sort()

        # TODO: Insert progress bar here
        for c in contents:
            try:
                op_map[op](
                    os.path.join(src_dir, c),
                    os.path.join(target_dir, c)
                )
            except Exception as e:
                failed_ops += 1
                print(f"Error when {op} on {c}: {e}")
            
            total_ops += 1

    print(f"Completed {total_ops - failed_ops} out of {total_ops} operations!")