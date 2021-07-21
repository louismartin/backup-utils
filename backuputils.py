from functools import lru_cache
from pathlib import Path
import shutil
import hashlib

import imohash
from tqdm import tqdm


@lru_cache(maxsize=500000)
def get_file_hash(filepath):
    return hashlib.md5((imohash.hashfile(filepath, hexdigest=True) + Path(filepath).name).encode()).hexdigest()


def get_files(dirpath):
    paths = []
    for path in tqdm(Path(dirpath).rglob('*'), 'Getting files'):
        if not path.is_file():
            continue
        paths.append(path)
    return paths


def trash(path, trash_path, base_dirpath):
    target_path = Path(trash_path) / Path(path).relative_to(base_dirpath)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists():
        raise FileExistsError(f'File already exists: {target_path}')
    shutil.move(path, target_path)


def is_dir_empty(dirpath):
    for path in Path(dirpath).rglob('*'):
        if path.name == '.DS_Store':
            continue
        if not path.is_dir():
            return False
        if not is_dir_empty(path):
            return False
    return True


def remove_empty_dirs(dirpath):
    for path in Path(dirpath).rglob('*'):
        if not path.is_dir():
            continue
        if not is_dir_empty(path):
            continue
        shutil.rmtree(path)
