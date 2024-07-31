from pathlib import Path
import os
from PIL import Image
import shutil
from .vgg16_khanhha_related.gui_to_model_exec_layer import exec_inference_unet
import re
import sys

'''
This module deals with the image processing execution. It handles the splitting, segmenting, and stitching of the images
'''

def img_splitter(img_path, splits_per_dim, dest_path) -> tuple:
    '''
    Splits each image found in img_path into splits_per_dim images per dimension

    For instance, if splits_per_dim = 10, each image in img_path will be split into 10 images per dimension.
    i.e. 100 smaller images will be made, and saved in dest_path.

    Args:
        img_path (string): path to images
        splits_per_dim (int): number of sub-images per dimension
        dest_path (string): path to destination folder

    Returns:
        None, saves split images in destination folder
    '''

    #TODO: no longer allows images of different dimensions

    #creating img_path and dest_path if necessary
    p_img_path = Path(img_path)
    p_dest_path = Path(dest_path)
    p_img_path.mkdir(exist_ok=True)
    p_dest_path.mkdir(exist_ok=True)

    #clear the dest path
    for path in p_dest_path.glob('*.*'):
        os.remove(str(path))

    #iterate through all files in img path
    for filename in os.listdir(img_path):
        #only consider jpg files
        if filename.endswith('.jpg') or filename.endswith('.JPG'):
            #open images
            img = Image.open(os.path.join(img_path, filename))

            width, height = img.size
            #getting the dimensions of sub images
            sub_width = width // splits_per_dim
            sub_height = height // splits_per_dim

            for i in range(splits_per_dim):
                for j in range(splits_per_dim):
                    #creating coordinate bounds for current sub image
                    top = i * sub_height
                    left = j * sub_width

                    #condition to account for leftover pixels
                    bottom = top + sub_height
                    if i == splits_per_dim - 1:
                        bottom += height % splits_per_dim

                    right = left + sub_width
                    if j == splits_per_dim - 1:
                        right += width % splits_per_dim

                    sub_img = img.crop((left, top, right, bottom))
                    #saving the sub image
                    #hardcoded to jpg for now
                    sub_filename = f"{os.path.splitext(filename)[0]}_" + "{:03d}_".format(i) + "{:03d}.jpg".format(j)
                    sub_img.save(os.path.join(dest_path, sub_filename))

            img.close()

    return img.size

def img_stitcher(img_path, splits_per_dim, dest_path, src_dim) -> None:
    '''
    Stitches the split images into a larger original image
    For instance, consider 100 images in img_path, with splits_per_dim = 10. This function would combine the
    100 images to create a 10x10 composite image.

    Args:
        img_path (Path): Path to the images to be stitched
        splits_per_dim (int): Number of splits to stitch
        dest_path (Path): Path where to save the stitched images

    Returns:
        None, saves stitches images in dest_path
    '''

    #TODO: currently only handles images that are all the same size

    # creating img_path and dest_path if necessary
    p_img_path = Path(img_path)
    p_dest_path = Path(dest_path)
    p_img_path.mkdir(exist_ok=True)
    p_dest_path.mkdir(exist_ok=True)

    # clear the dest path
    for path in p_dest_path.glob('*.*'):
        os.remove(str(path))

    #making a list of the image paths
    img_list = [img for img in os.listdir(img_path) if (img.endswith('.jpg') or img.endswith('.JPG'))]
    # print(f"{len(img_list)} images")

    if len(img_list) == 0:
        return

    #loop through each mega-image
    for img_set in range(len(img_list)//(splits_per_dim**2)):
        #offset for the image list wrt the current mega image
        img_list_offset = img_set*(splits_per_dim**2)

        # getting the dimensions of an image (assuming they are all the same size
        sample_img = Image.open(os.path.join(img_path, img_list[img_set*(splits_per_dim**2)]))
        mini_width, mini_height = sample_img.size

        match = re.match(r'^(.*?)_\d{3}_\d{3}\.jpg$', img_list[img_set*(splits_per_dim**2)])
        if match:
            out_img_name = match.group(1)
        else:
            out_img_name = f"stitched_no_{img_set}"

        out_img_name += ".jpg"

        sample_img.close()

        #creating canvas mega image
        mega_img = Image.new('RGB', src_dim)

        #iterating and stitching images
        for i in range(splits_per_dim**2):
            img = img_list[i + img_list_offset]
            # print(img)
            curr_img_path = os.path.join(img_path, img)
            curr_img = Image.open(curr_img_path)

            row = i // splits_per_dim   #current mini img row and col
            col = i % splits_per_dim

            mega_img.paste(curr_img, (col * mini_width, row * mini_height))
            curr_img.close()

        mega_img.save(os.path.join(dest_path, out_img_name))
        mega_img.close()

def proc_executor(src_path, split_no, dest_path) -> None:
    '''
    This function splits, segments, and stitchs the images in the given path.
    :param src_path: A string containing the image directory path.
    :param split_no: A positive integer containing the number of splits for each image
    :return:
    '''

    # splitting images into temp directory
    pathified_src_path = Path(src_path)
    pathified_dest_path = Path(dest_path)
    temp_split_path = pathified_src_path / "temp_splits"    # this is a path object, not string
    processed_temp_split_path = pathified_src_path / "processed"
    img_dim = img_splitter(img_path=src_path, splits_per_dim=split_no, dest_path=str(temp_split_path))

    # choosing image path to use based on whether code is frozen or not. if frozen, assume it's with
    # pyinstaller and use MEIPASS
    if getattr(sys, 'frozen', False):
        model_path = os.path.join(sys._MEIPASS, "models/model_unet_vgg_16_best.pt")
    else:
        model_path = "./models/model_unet_vgg_16_best.pt"

    # insert code to run the model here
    exec_inference_unet(img_dir=str(temp_split_path), model_path=model_path,
                        model_type="vgg16", out_pred_dir=str(processed_temp_split_path))#, threshold=threshold)

    # stitching images back into larger images

    img_stitcher(img_path=str(processed_temp_split_path), splits_per_dim=split_no, dest_path=str(pathified_dest_path), src_dim=img_dim)

    shutil.rmtree(str(temp_split_path))
    shutil.rmtree(str(processed_temp_split_path))
