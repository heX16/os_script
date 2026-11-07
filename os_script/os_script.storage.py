# WIP
# Not imported or used by the library.

import os
import platform
from pathlib import Path


def get_mount_point(path: Path | str) -> Path:
    """
    Return the mount point that serves `path`.

    Walks up from `path` until a mount point is found. For a regular
    directory on the root filesystem this is `/`.
    """
    p = Path(path).resolve()
    while not os.path.ismount(p):
        if p.parent == p:
            break
        p = p.parent
    return p


def get_mount_info(path: Path | str) -> dict[str, str] | None:
    """
    Return mount information for `path`.

    Keys: `mount_point`, `fstype`, `source`, `options`.
    Linux only. Returns None when the mount cannot be determined.
    """
    if not _is_linux():
        raise RuntimeError('Not running on Linux.')

    mount_point = str(get_mount_point(path))
    try:
        with open('/proc/self/mountinfo') as fh:
            lines = fh.read().splitlines()
    except OSError:
        return None

    # mountinfo format:
    # 36 35 98:0 /mnt1 /mnt2 rw,noatime master:1 - ext3 /dev/root rw,errors=continue
    # Fields before ' - ' vary in count, so split on the separator.
    result = None
    for line in lines:
        head, _, tail = line.partition(' - ')
        head_fields = head.split()
        tail_fields = tail.split()
        if len(head_fields) < 6 or len(tail_fields) < 2:
            continue
        # Mount points with spaces are escaped as \040.
        target = head_fields[4].replace('\\040', ' ')
        if target == mount_point:
            # The last matching line is the most recent mount on top.
            result = {
                'mount_point': target,
                'fstype': tail_fields[0],
                'source': tail_fields[1],
                'options': head_fields[5],
            }
    return result
