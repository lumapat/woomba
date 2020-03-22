from shutil import copyfile
from typing import Any, Dict, List

import os

def diff_directories(
    base_contents: Dict[str, List[str]],
    target_contents: Dict[str, List[str]],
):
    """ Return list of differences between directories """

    base_contents_keys = set(base_contents.keys()) if base_contents else set()
    target_contents_keys = set(target_contents.keys()) if target_contents else set()

    deleted_contents_keys = base_contents_keys - target_contents_keys
    added_contents_keys = target_contents_keys - base_contents_keys
    same_contents_keys = base_contents_keys & target_contents_keys

    return {
        "added": added_contents_keys,
        "deleted": deleted_contents_keys,
    }


def find_all_files(root: str):
    return {d: set(files) for d, _, files in os.walk(root)}
