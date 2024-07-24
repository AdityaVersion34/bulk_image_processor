# import os
# from pathlib import Path
# from vgg16_khanhha_related.utils import load_unet_vgg16
# from tqdm import tqdm
# import torchvision.transforms as transforms
# from PIL import Image
# import numpy as np
# from vgg16_khanhha_related.inference_unet import evaluate_img
# import cv2 as cv
# from os.path import join
# import gc

import sys
import os
import numpy as np
from pathlib import Path
import cv2 as cv
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import torchvision.transforms as transforms
from vgg16_khanhha_related.unet.unet_transfer import UNet16, input_size
import matplotlib.pyplot as plt
import argparse
from os.path import join
from PIL import Image
import gc
from vgg16_khanhha_related.utils import load_unet_vgg16, load_unet_resnet_101, load_unet_resnet_34
from tqdm import tqdm
import tkinter as tk


def evaluate_img(model, img):
    input_width, input_height = input_size[0], input_size[1]

    img_height, img_width, img_channels = img.shape

    # added by me
    channel_means = [0.485, 0.456, 0.406]
    channel_stds = [0.229, 0.224, 0.225]
    train_tfms = transforms.Compose([transforms.ToTensor(), transforms.Normalize(channel_means, channel_stds)])

    img_1 = cv.resize(img, (input_width, input_height), cv.INTER_AREA)
    X = train_tfms(Image.fromarray(img_1))
    X = Variable(X.unsqueeze(0)).cuda()  # [N, 1, H, W]

    mask = model(X)

    mask = F.sigmoid(mask[0, 0]).data.cpu().numpy()
    mask = cv.resize(mask, (img_width, img_height), cv.INTER_AREA)
    return mask


# defining a function to emulate the inference_unet.py cli execution command

def exec_inference_unet(img_dir, model_path, model_type, out_pred_dir) -> None:     #       , threshold=0.3) -> None:
    '''
    Emulates the inference_unet.py cli execution command. To allow the GUI to perform the same

    :param img_dir: input image directory
    :param model_path: path to model
    :param model_type: type of model
    :param out_pred_dir: output image directory
    :param threshold: segmentation threshold
    :return:
    '''

    # spawning a tkinter progress tracker
    prog_win = tk.Tk()
    prog_win.title('Image Processing Progress')
    prog_win.geometry('250x40')
    prog_win.resizable(False, False)

    frm_prog = tk.Frame(master=prog_win, bg="red")
    frm_prog.pack(fill=tk.BOTH, expand=True)

    lbl_prog_tracker = tk.Label(master=frm_prog, bg="maroon", fg="white", text="test prog tracker")
    lbl_prog_tracker.pack(fill=tk.BOTH, expand=True)

    # handles out_pred_dir
    if out_pred_dir != '':
        os.makedirs(out_pred_dir, exist_ok=True)
        for path in Path(out_pred_dir).glob('*.*'):
            os.remove(str(path))

    # handling model type
    if model_type == 'vgg16':
        model = load_unet_vgg16(model_path)
    else:
        print('undefined model name pattern')
        exit()

    channel_means = [0.485, 0.456, 0.406]
    channel_stds = [0.229, 0.224, 0.225]

    paths = [path for path in Path(img_dir).glob('*.*')]
    for idx, path in enumerate(paths):
        # print(str(path))

        prog_win.update()
        lbl_prog_tracker["text"] = f"Generating visualizations... {idx + 1}/{len(paths)}"

        #train_tfms = transforms.Compose([transforms.ToTensor(), transforms.Normalize(channel_means, channel_stds)])

        img_0 = Image.open(str(path))
        img_0 = np.asarray(img_0)
        if len(img_0.shape) != 3:
            print(f'incorrect image shape: {path.name}{img_0.shape}')
            continue

        img_0 = img_0[:, :, :3]

        #img_height, img_width, img_channels = img_0.shape

        prob_map_full = evaluate_img(model, img_0)

        # cutting off prob_map_full to threshold
        # prob_map_full[prob_map_full < threshold] = 0

        # if out_pred_dir != '':
        #     # cv.imwrite(filename=join(out_pred_dir, f'{path.stem}.jpg'), img=(prob_map_full * 255).astype(np.uint8))
        #     cv_img_0 = cv.cvtColor(np.array(img_0, dtype=np.uint8), cv.COLOR_RGB2BGR)
        #     cv_prob_map_full = cv.cvtColor(np.array(prob_map_full * 255, dtype=np.uint8), cv.COLOR_RGB2BGR)
        #     cv_prob_map_full = cv_prob_map_full[:, :] * np.array([1, 0, 1], dtype=np.uint8)
        #     # print(cv_img_0.shape)
        #     # print(cv_prob_map_full.shape)
        #     # print(cv_img_0[0,0].shape)
        #     # for i in (cv_prob_map_full[:]):
        #     #     for j in (i[:]):
        #     #         if np.sum(j) > 0:
        #     #             print(j.shape)
        #     #             print(j)
        #     # composite_image = cv.addWeighted(cv_img_0, 0.2, cv_prob_map_full, 0.8, 0)
        #     composite_image = cv.add(cv_img_0, cv_prob_map_full)  # saturating image, no overflow
        #     # composite_image = cv_img_0 + cv_prob_map_full   #allowing overflow for now because of good contrast.
        #     cv.imwrite(filename=join(out_pred_dir, f'{path.stem}.jpg'), img=composite_image)

        if out_pred_dir != '':
            cv_prob_map_full = cv.cvtColor(np.array(prob_map_full * 255, dtype=np.uint8), cv.COLOR_RGB2BGR)
            cv.imwrite(filename=join(out_pred_dir, f'{path.stem}.jpg'), img=cv_prob_map_full)

        if idx == len(paths) - 1:
            prog_win.destroy()

        gc.collect()

    return