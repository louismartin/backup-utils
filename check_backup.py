import argparse

from tqdm import tqdm

from backuputils import get_files, get_file_hash


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check if files are missing from a backup')
    parser.add_argument('original', help='Path to the original. We will check that all files in the original are also in the backup.')
    parser.add_argument('backup', help='Path to the backup where some files might be missing.')
    args = parser.parse_args()

    reference_hashes = set([get_file_hash(filepath) for filepath in get_files(args.backup)])
    for filepath in tqdm(get_files(args.original), 'Checking missing files'):
        if not get_file_hash(filepath) in reference_hashes:
            print(filepath)
