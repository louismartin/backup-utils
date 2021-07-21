import argparse

from tqdm import tqdm

from backuputils import get_files, get_file_hash, trash, remove_empty_dirs


if __name__ == '__main__':
    print('TODO: This script was never run so it might contain bugs.')
    input('This script will remove files aggressively, caution is advised! Press any key to continue.')
    parser = argparse.ArgumentParser(description='Move files that were already backed up to trash.')
    parser.add_argument('--paths-to-clean', nargs='+', help='Path to the original. We will check that all files in the original are also in the backup.', required=True)
    parser.add_argument('--backup-paths', nargs='+', help='Path to the backup where some files might be missing.', required=True)
    args = parser.parse_args()

    backup_hashes = set([get_file_hash(filepath) for dirpath in args.backup_paths for filepath in get_files(dirpath)])
    for path_to_clean in args.paths_to_clean:
        trash_path = path_to_clean / 'trash'
        for filepath in tqdm(get_files(path_to_clean), 'Cleaning'):
            if filepath.name == 'trash':
                continue
            if filepath.name.startswith('.'):
                continue
            if get_file_hash(filepath) in backup_hashes:
                print(f'Removing "{filepath}"')
                trash(filepath, trash_path, path_to_clean)
        remove_empty_dirs(path_to_clean)