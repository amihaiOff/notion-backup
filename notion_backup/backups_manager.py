import os

import pandas as pd
from pathlib import Path

MAX_NUM_FILES = 3  # this assumes we always want to backups and the third is the new download


def read_files(output_dir: str):
    """ read files from backup folder """
    path = Path(output_dir)
    files = [file for file in path.iterdir()]
    if len(files) != MAX_NUM_FILES:
        raise ValueError(f'too many backup files found ({len(files)})')
    return files


def get_earliest_file(files):
    """ find the earliest file to be removed """
    dates_dict = {
        file: pd.to_datetime(file.split('_')[-1].split('.')[0]) for file in files
    }
    dates = sorted(list(dates_dict.values()))
    if dates[-1] != pd.to_datetime('today'):
        raise ValueError(f'problem with backup latest backup isn\'t today (dates: {dates})')

    earliest_file = min(dates_dict, key=dates_dict.get)
    return earliest_file


def run_backup_management(output_dir: str):
    files = read_files(output_dir)
    backup2del = get_earliest_file(files)
    os.remove(backup2del)
