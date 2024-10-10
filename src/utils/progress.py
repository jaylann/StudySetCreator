# src/utils/progress.py

from tqdm import tqdm
from typing import Iterable

def get_progress_bar(iterable: Iterable, **kwargs):
    return tqdm(iterable, **kwargs)
