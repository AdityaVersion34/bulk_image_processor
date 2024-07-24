import cv2 as cv
import numpy as np
from pathlib import Path
from tqdm import tqdm
from PIL import Image
from os.path import join

def viz_executor(img_dir, msk_dir, out_dir, thresh, color, pres_transp):
    '''
    Function to process the visualization of images

    :param img_dir: input image directory
    :param msk_dir: input mask directory
    :param out_dir: output image directory
    :param thresh: segmentation threshold float
    :param color: selected color for segmentation
    :return:
    '''

    # creating a color-to-nparray dictionary
    color_to_arr = {
        "Red" : np.array([0, 0, 1], dtype=np.uint8),
        "Green" : np.array([0, 1, 0], dtype=np.uint8),
        "Blue" : np.array([1, 0, 0], dtype=np.uint8),
        "Yellow" : np.array([0, 1, 1], dtype=np.uint8),
        "Pink" : np.array([1, 0, 1], dtype=np.uint8),
        "Cyan" : np.array([1, 1, 0], dtype=np.uint8)
    }

    # selected color in the form of a numpy array
    selected_color = color_to_arr[color]

    # getting lists of images and mask paths
    images = [img for img in Path(img_dir).glob("*.*")]
    masks = [msk for msk in Path(msk_dir).glob("*.*")]

    # iterate based on shorter dir
    shorter_len = len(images) if len(images) < len(masks) else len(masks)

    # tqdm for a cool progress bar
    for idx in tqdm(range(shorter_len)):

        img_path = images[idx]
        msk_path = masks[idx]

        curr_img = Image.open(str(img_path))
        curr_img = np.asarray(curr_img, dtype=np.uint8)
        curr_msk = Image.open(str(msk_path))
        curr_msk = np.asarray(curr_msk, dtype=np.uint8, copy=True)

        # cutting off to threshold
        curr_msk[curr_msk < thresh] = 0

        if pres_transp == 0:
            curr_msk[curr_msk > thresh] = 255

        # converting to cv images
        cv_curr_img = cv.cvtColor(curr_img, cv.COLOR_BGR2RGB)
        cv_curr_msk = cv.cvtColor(curr_msk, cv.COLOR_BGR2RGB)

        # coloring mask
        cv_curr_msk = cv_curr_msk[:, :] * selected_color

        composite_img = cv.add(cv_curr_img, cv_curr_msk)

        cv.imwrite(filename=join(out_dir, f"{images[idx].stem}.jpg"), img=composite_img)

    return

if __name__ == '__main__':
    viz_executor(img_dir="C:/Users/Aditya/senseimage_stuff/test",
                 msk_dir="C:/Users/Aditya/senseimage_stuff/test/mask_ops",
                 out_dir="C:/Users/Aditya/senseimage_stuff/test/out",
                 thresh=20,
                 color="Red")