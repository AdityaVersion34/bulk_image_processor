from pathlib import Path

import cv2
from PIL import Image
import numpy as np
import cv2 as cv
import os
from os.path import join
from tqdm import tqdm

# takes the intersection/union of two directories of masks, maskwise
# unused in the final application, was not appropriately effective

def mask_operator(dir1, dir2, out_dir) -> None:
    '''
    Takes the intersecton of two directories and creates a directory of corresponding mask images
    :param dir1: input dir 1
    :param dir2: input dir 2
    :param out_dir: output dir
    :return: None
    '''

    # making lists of the paths in each dir
    paths1 = [path for path in Path(dir1).glob('*.*')]
    paths2 = [path for path in Path(dir2).glob('*.*')]

    short_len = len(paths1) if len(paths1) < len(paths2) else len(paths2)

    for idx in tqdm(range(short_len)):
        # iterating through the masks
        mask1 = Image.open(str(paths1[idx]))
        mask1 = np.asarray(mask1)

        mask2 = Image.open(str(paths2[idx]))
        mask2 = np.asarray(mask2)

        cv_mask1 = cv.cvtColor(mask1, cv.COLOR_RGB2BGR)
        cv_mask2 = cv.cvtColor(mask2, cv.COLOR_RGB2BGR)

        cv_combo_mask = cv.bitwise_and(cv_mask1, cv_mask2)

        cv.imwrite(filename=join(out_dir, f"{paths1[idx].stem}.jpg"), img=cv_combo_mask)
