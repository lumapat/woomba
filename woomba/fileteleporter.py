from enum import Enum
from filecmp import dircmp
from shutil import copy2, copytree, rmtree
from typing import Any, Dict, List

import os


def generate_sync_operations(base_dir: str, target_dir: str):
    """ TODO Description

        Left is base and right is target
    """

    dir_comp = dircmp(base_dir, target_dir)

    # Operation names need to be in sync with sync_contents()
    # TODO: Replace with defaultdict
    operations = {
        "copy": [os.path.join(base_dir, o) for o in dir_comp.left_only],
        "remove": [os.path.join(target_dir, o) for o in dir_comp.right_only]
    }

    for d in dir_comp.subdirs:
        subops = generate_sync_operations(
            os.path.join(base_dir, d),
            os.path.join(target_dir, d))
        for s in subops:
            operations[s] += subops[s]

    return operations


def _remove_object(_, path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def _copy_object(src: str, target: str):
    if os.path.isdir(src):
        shutil.copytree(src, target)
    else:
        shutil.copy2(src, target)

def process_contents(
    src_dir: str,
    target_dir: str,
    contents: List[str],
    operation
):
    failed_ops = 0
    total_ops = 0

    contents.sort()

    # TODO: Insert progress bar here
    for c in contents:
        try:
            operation(
                os.path.join(src_dir, c),
                os.path.join(target_dir, c)
            )
        except Exception as e:
            failed_ops += 1
            print(f"Error when {op} on {c}: {e}")
        
        total_ops += 1

    return failed_ops, total_ops


def sync_contents(
    src_dir: str,
    target_dir: str,
    operations: Dict[str, List[str]]
):
    """ Sync contents of into a directory """

    if "copy" in operations:
        failed_copies, total_copies = process_contents(
            src_dir,
            target_dir,
            operations["copy"],
            _copy_object
        )
        print(f"Successfully copied {total_copies - failed_copies} out of {total_copies} items!")

    if "remove" in operations:
        failed_removals, total_removals = process_contents(
            src_dir,
            target_dir,
            operations["remove"],
            _remove_object
        )
        print(f"Successfully removed {total_removals - failed_removals} out of {total_removals} items!")
