# import tkinter as tk
from tkinter.filedialog import askdirectory

from .proc_executor import *
from .viz_executor import *

# This file contains python code for the main GUI of the bulk image processor


def processing_handler() -> None:
    '''
    This function is triggered on click of the run button. Calls helper function that actually handles the processing.
    This function itself handles the status bar and out dir printing

    :return: None
    '''

    # getting relevant data
    src_path = lbl_inp_dir_overview_data["text"]
    dest_path = lbl_out_dir_overview_data["text"]
    split_no = lbl_split_no_overview_data["text"]
    # model_threshold = lbl_thresh_no_overview_data["text"]

    # asserting data format
    if src_path == "":
        proc_run_err_msg["text"] = "Please enter a valid input directory path"
        return

    if dest_path == "":
        proc_run_err_msg["text"] = "Please enter a valid input directory path"
        return
    elif dest_path == src_path:
        proc_run_err_msg["text"] = "Please ensure the input and output directory paths are different"
        return

    if split_no == "":
        proc_run_err_msg["text"] = "Please enter a valid number of image splits"
        return

    split_no_int = int(split_no)

    proc_run_err_msg["text"] = ""

    proc_executor(src_path=src_path, split_no=split_no_int, dest_path=dest_path)
    return

def visualization_handler() -> None:
    '''
    Function to check label fields and step into the visualization process
    :return: None
    '''

    # getting the data from label fields
    img_src_path = lbl_viz_img_dir_overview_data["text"]
    msk_src_path = lbl_viz_msk_dir_overview_data["text"]
    out_path = lbl_viz_out_dir_overview_data["text"]
    thresh = lbl_viz_thresh_overview_data["text"]
    color = lbl_viz_color_overview_data["text"]
    yes_transp = pres_transp.get()

    # data validity checking
    if img_src_path == "":
        proc_viz_run_err_msg["text"] = "Please enter a valid input image path"
        return

    if msk_src_path == "":
        proc_viz_run_err_msg["text"] = "Please enter a valid input mask path"
        return

    if out_path == "":
        proc_viz_run_err_msg["text"] = "Please enter a valid output path"
        return
    elif out_path == img_src_path or out_path == msk_src_path:
        proc_viz_run_err_msg["text"] = "Please ensure the input and output paths are different"
        return

    if thresh == "":
        proc_viz_run_err_msg["text"] = "Please enter a valid threshold value"
        return

    if color == "":
        proc_viz_run_err_msg["text"] = "Please enter a valid segmentation color"
        return

    # all values OK, proceeding...
    proc_viz_run_err_msg["text"] = ""

    ft_thresh = float(thresh)
    viz_executor(img_dir = img_src_path, msk_dir = msk_src_path, out_dir = out_path, thresh = ft_thresh, color=color,
                 pres_transp=yes_transp)
    return

def get_dir(*destinations) -> None:
    '''
    Asks to select a directory and print dir path to destinations
    :param destinations: list of tkinter elements to which to print destinations
    :return: None
    '''

    filepath = askdirectory()
    if not filepath:
        return
    for elem in destinations:
        elem["text"] = filepath

def confirm_pix_int(inp) -> bool:
    '''
    This function confirms that an input is an integer between 0 and 255. Intended to check if a mask pixel is a
    uint-8
    Args:
        inp: input value

    Returns:
        Boolean output

    '''

    try:
        inp_to_int = int(inp)
        if (inp_to_int >= 0 and inp_to_int <= 255):
            return True
        else:
            return False
    except:
        return False

def confirm_pos_int(inp) -> bool:
    '''
    confirms that the parameter is a positive integer
    :param inp: input value
    :return:
    Boolean output
    '''

    try:
        inp_to_int = int(inp)
        if (inp_to_int > 0):
            return True
        else:
            return False
    except:
        return False

def ret_true(ignore) -> bool:
    '''
    Function that takes a dummy input and returns True. Made for the sake of compatibility with bulk img proc code
    Args:
        ignore: dummy input

    Returns:
        True
    '''

    return True

def confirm_button(source, confirmer, err_field, *destinations):
    '''
    This function is meant to be used with a confirm button widget

    It obtains data from source, checks it with a confirmer function. If true, copies to destinations.
    If false, prints err msg to err field

    :param source:
    :param confirmer:
    :param destinations:
    :return:
    '''

    if not confirmer(source.get()):
        if err_field is not None:
            err_field["text"] = "Please enter a valid input"
    else:
        if err_field is not None:
            err_field["text"] = ""
        for elem in destinations:
            elem["text"] = source.get()


# displaying if frozen or running from source
import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
else:
    print('running in a normal Python process')

# initializing base gui window
base_win = tk.Tk()
base_win.title("Bulk Image Processor")
base_win.geometry("1300x600")

# initializing base frame
frm_win = tk.Frame(master=base_win, bg="skyblue")
frm_win.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frm_viz = tk.Frame(master=base_win, bg="gold")
frm_viz.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# configuring details of base frame grid
frm_win.columnconfigure(0, weight=1, minsize=300)
frm_win.rowconfigure(0, weight=1, minsize=30)
frm_win.rowconfigure([1, 2, 3], weight=1, minsize=75)

frm_viz.columnconfigure(0, weight=1, minsize=300)
frm_viz.rowconfigure(0, weight=1, minsize=30)
frm_viz.rowconfigure([1, 2, 3], weight=1, minsize=75)

# =========================
# Frame Win
# =========================

# creating frames for each step
frm_sec1_head = tk.Frame(master=frm_win, bg="white", border=3)

frm_get_dir = tk.Frame(master=frm_win, bg="white", border=3)

frm_get_splits = tk.Frame(master=frm_win, bg="white", border=3)

frm_run_model = tk.Frame(master=frm_win, bg="white", border=3)

# frm_result_dir = tk.Frame(master=frm_win, bg="white", border=3)

# griddying each step frame
frm_sec1_head.grid(row=0, column=0, padx=5, pady=5, sticky="news")
frm_get_dir.grid(row=1, column=0, padx=5, pady=5, sticky="news")
frm_get_splits.grid(row=2, column=0, padx=5, pady=5, sticky="news")
frm_run_model.grid(row=3, column=0, padx=5, pady=5, sticky="news")
# frm_result_dir.grid(row=3, column=0, padx=5, pady=5, sticky="news")

lbl_heading_info = tk.Label(master=frm_sec1_head, bg="white", relief=tk.SUNKEN, text="Mask Generation")

lbl_heading_info.pack(fill=tk.BOTH, expand=True)

# =============================================================
# DIRECTORY ENTRY SECTION

# heading label for directory entry section
lbl_get_dir_info = tk.Label(master=frm_get_dir, bg="white", relief=tk.SUNKEN, text="1) Enter relevant directories")

# getting input directory
lbl_get_inp_dir = tk.Label(master=frm_get_dir, bg="white", border=3, text="Enter the image input directory: ")
btn_get_inp_dir = tk.Button(master=frm_get_dir, text="Select Directory...",
                            command=lambda: get_dir(lbl_confirm_inp_dir, lbl_inp_dir_overview_data))
lbl_confirm_inp_dir = tk.Label(master=frm_get_dir, bg="white", border=3, text="")

lbl_get_out_dir = tk.Label(master=frm_get_dir, bg="white", border=3, text="Enter the mask output directory: ")
btn_get_out_dir = tk.Button(master=frm_get_dir, text="Select Directory...",
                            command=lambda: get_dir(lbl_confirm_out_dir, lbl_out_dir_overview_data))
lbl_confirm_out_dir = tk.Label(master=frm_get_dir, bg="white", border=3, text="")


# adding everything to grid
lbl_get_dir_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

lbl_get_inp_dir.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
btn_get_inp_dir.grid(row=1, column=1, padx=2, pady=2, sticky="nw")
lbl_confirm_inp_dir.grid(row=1, column=2, padx=2, pady=2, sticky="nw")

lbl_get_out_dir.grid(row=2, column=0, padx=2, pady=2, sticky="nw")
btn_get_out_dir.grid(row=2, column=1, padx=2, pady=2, sticky="nw")
lbl_confirm_out_dir.grid(row=2, column=2, padx=2, pady=2, sticky="nw")


# ===========================================================
# SPLIT COUNT SELECTION SECTION

lbl_get_preproc_info = tk.Label(master=frm_get_splits, bg="white", relief=tk.SUNKEN, text="2) Enter preprocessing directives")

lbl_get_splits = tk.Label(master=frm_get_splits, bg="white", border=3,
                          text="Enter the number of image splits per dimension (Positive integer): ")
ent_get_splits = tk.Entry(master=frm_get_splits, bg="white", width=7)
lbl_split_err_msg = tk.Label(master=frm_get_splits, bg="white", fg="red", border=3, text="")
btn_split_confirmer = tk.Button(master=frm_get_splits, text="Confirm",
                                command= lambda: confirm_button(ent_get_splits, confirm_pos_int,
                                                            lbl_split_err_msg, lbl_split_no_overview_data))


# adding to grid
lbl_get_preproc_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

lbl_get_splits.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
ent_get_splits.grid(row=1, column=1, padx=2, pady=2, sticky="nw")
btn_split_confirmer.grid(row=1, column=2, padx=2, pady=2, sticky="nw")
lbl_split_err_msg.grid(row=1, column=3, padx=2, pady=2, sticky="nw")


# ===========================================================
# EXECUTION INFO

# heading
lbl_run_model_info = tk.Label(master=frm_run_model, bg="white", relief=tk.SUNKEN, text="3) Review and process images")

# overview labels
lbl_run_model_warning = tk.Label(master=frm_run_model, bg="white", text="Please review your selections before proceeding: ")
lbl_model_overview = tk.Label(master=frm_run_model, bg="white", text="\tModel Overview:\t")#VGG16, pretrained on Khanhha's Dataset")
lbl_inp_dir_overview = tk.Label(master=frm_run_model, bg="white", text="\tInput directory:\t")
lbl_out_dir_overview = tk.Label(master=frm_run_model, bg="white", text="\tOutput directory:\t")
lbl_split_no_overview = tk.Label(master=frm_run_model, bg="white", text="\tNumber of splits per dimension:\t")


# overview data
lbl_model_overview_data = tk.Label(master=frm_run_model, bg="white", text="VGG16, pretrained on Khanhha's Dataset")
lbl_inp_dir_overview_data = tk.Label(master=frm_run_model, bg="white", text="")
lbl_out_dir_overview_data = tk.Label(master=frm_run_model, bg="white", text="")
lbl_split_no_overview_data = tk.Label(master=frm_run_model, bg="white", text="")


btn_proc_run = tk.Button(master=frm_run_model, bg="limegreen", text="Run", command=processing_handler)
proc_run_err_msg = tk.Label(master=frm_run_model, bg="white", fg="red", text="")

# adding to grid
lbl_run_model_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

lbl_run_model_warning.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
lbl_model_overview.grid(row=2, column=0, padx=2, pady=2, sticky="nw")
lbl_inp_dir_overview.grid(row=3, column=0, padx=2, pady=2, sticky="nw")
lbl_out_dir_overview.grid(row=4, column=0, padx=2, pady=2, sticky="nw")
lbl_split_no_overview.grid(row=5, column=0, padx=2, pady=2, sticky="nw")


lbl_model_overview_data.grid(row=2, column=1, padx=2, pady=2, sticky="nw")
lbl_inp_dir_overview_data.grid(row=3, column=1, padx=2, pady=2, sticky="nw")
lbl_out_dir_overview_data.grid(row=4, column=1, padx=2, pady=2, sticky="nw")
lbl_split_no_overview_data.grid(row=5, column=1, padx=2, pady=2, sticky="nw")


btn_proc_run.grid(row=6, column=2, ipadx=10, ipady=4, padx=2, pady=2, sticky="nw")
proc_run_err_msg.grid(row=6, column=1, padx=2, pady=2, sticky="w")


# ================================
# Frame Viz
# ================================

frm_viz_heading = tk.Frame(master=frm_viz, bg="white", border=3)
frm_viz_dir = tk.Frame(master=frm_viz, bg="white", border=3)
frm_viz_color_etc = tk.Frame(master=frm_viz, bg="white", border=3)
frm_viz_exec = tk.Frame(master=frm_viz, bg="white", border=3)

frm_viz_heading.grid(row=0, column=0, padx=5, pady=5, sticky="news")
frm_viz_dir.grid(row=1, column=0, padx=5, pady=5, sticky="news")
frm_viz_color_etc.grid(row=2, column=0, padx=5, pady=5, sticky="news")
frm_viz_exec.grid(row=3, column=0, padx=5, pady=5, sticky="news")


# ===============================
# VIZ HEADING
# ===============================
lbl_viz_heading = tk.Label(master=frm_viz_heading, bg="white", relief=tk.SUNKEN, text="Visualize Images")

lbl_viz_heading.pack(fill=tk.BOTH, expand=True)

# ===============================
# VIZ DIRECTORY SELECT
# ===============================
# heading
lbl_viz_dir_info = tk.Label(master=frm_viz_dir, bg="white", relief=tk.SUNKEN, text="1) Enter relevant directories")

lbl_viz_dir_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

# directory selectors
lbl_viz_get_img_dir = tk.Label(master=frm_viz_dir, bg="white", border=3, text="Enter the image input directory: ")
btn_viz_get_img_dir = tk.Button(master=frm_viz_dir, text="Select Directory...",
                            command=lambda: get_dir(lbl_viz_confirm_img_dir, lbl_viz_img_dir_overview_data))
lbl_viz_confirm_img_dir = tk.Label(master=frm_viz_dir, bg="white", border=3, text="")

lbl_viz_get_msk_dir = tk.Label(master=frm_viz_dir, bg="white", border=3, text="Enter the mask input directory: ")
btn_viz_get_msk_dir = tk.Button(master=frm_viz_dir, text="Select Directory...",
                            command=lambda: get_dir(lbl_viz_confirm_msk_dir, lbl_viz_msk_dir_overview_data))
lbl_viz_confirm_msk_dir = tk.Label(master=frm_viz_dir, bg="white", border=3, text="")

lbl_viz_get_out_dir = tk.Label(master=frm_viz_dir, bg="white", border=3, text="Enter the output directory: ")
btn_viz_get_out_dir = tk.Button(master=frm_viz_dir, text="Select Directory...",
                            command=lambda: get_dir(lbl_viz_confirm_out_dir, lbl_viz_out_dir_overview_data))
lbl_viz_confirm_out_dir = tk.Label(master=frm_viz_dir, bg="white", border=3, text="")

lbl_viz_get_img_dir.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
btn_viz_get_img_dir.grid(row=1, column=1, padx=2, pady=2, sticky="nw")
lbl_viz_confirm_img_dir.grid(row=1, column=2, padx=2, pady=2, sticky="nw")

lbl_viz_get_msk_dir.grid(row=2, column=0, padx=2, pady=2, sticky="nw")
btn_viz_get_msk_dir.grid(row=2, column=1, padx=2, pady=2, sticky="nw")
lbl_viz_confirm_msk_dir.grid(row=2, column=2, padx=2, pady=2, sticky="nw")

lbl_viz_get_out_dir.grid(row=3, column=0, padx=2, pady=2, sticky="nw")
btn_viz_get_out_dir.grid(row=3, column=1, padx=2, pady=2, sticky="nw")
lbl_viz_confirm_out_dir.grid(row=3, column=2, padx=2, pady=2, sticky="nw")

# =========================
# SELECT VIZ PREFEERENCES
# =========================

lbl_viz_dir_info = tk.Label(master=frm_viz_color_etc, bg="white", relief=tk.SUNKEN,
                            text="2) Enter vizualization preferences")

lbl_viz_dir_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

lbl_get_thresh = tk.Label(master=frm_viz_color_etc, bg="white", border=3,
                          text="Enter the mask threshold (int between 0 and 255): ")
ent_get_thresh = tk.Entry(master=frm_viz_color_etc, bg="white", width=7)
lbl_thresh_err_msg = tk.Label(master=frm_viz_color_etc, bg="white", fg="red", border=3, text="")
btn_thresh_confirmer = tk.Button(master=frm_viz_color_etc, text="Confirm",
                                 command= lambda: confirm_button(ent_get_thresh, confirm_pix_int,
                                                                 lbl_thresh_err_msg, lbl_viz_thresh_overview_data))

lbl_get_thresh.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
ent_get_thresh.grid(row=1, column=1, padx=2, pady=2, sticky="nw")
btn_thresh_confirmer.grid(row=1, column=2, padx=2, pady=2, sticky="nw")
lbl_thresh_err_msg.grid(row=1, column=3, padx=2, pady=2, sticky="nw")

color_options = [
    "Red",
    "Green",
    "Blue",
    "Yellow",
    "Cyan",
    "Pink"
]

color_clicked = tk.StringVar(master=frm_viz_color_etc, value="Red")

lbl_get_seg_color = tk.Label(master=frm_viz_color_etc, bg="white", border=3,
                             text="Enter segmentation highlight color: ")
ddm_get_seg_color = tk.OptionMenu(frm_viz_color_etc, color_clicked, *color_options)
btn_conf_seg_color = tk.Button(master=frm_viz_color_etc, text="Confirm",
                        command=lambda: confirm_button(color_clicked, ret_true, None, lbl_viz_color_overview_data))

lbl_get_seg_color.grid(row=2, column=0, padx=2, pady=2, sticky="nw")
ddm_get_seg_color.grid(row=2, column=1, padx=2, pady=2, sticky="nw")
btn_conf_seg_color.grid(row=2, column=2, padx=2, pady=2, sticky="nw")

# adding radio button to toggle mask transparency
lbl_check_transp = tk.Label(master=frm_viz_color_etc, bg="white", border=3, text="Preserve confidence gradient: ")
pres_transp = tk.IntVar()
rb_check_transp = tk.Checkbutton(master=frm_viz_color_etc, variable=pres_transp, onvalue=1, offvalue=0)

lbl_check_transp.grid(row=3, column=0, padx=2, pady=2, sticky="nw")
rb_check_transp.grid(row=3, column=1, padx=2, pady=2, sticky="nw")

# ==========================
# REVIEW AND EXECUTE
# ==========================

# heading
lbl_viz_run_model_info = tk.Label(master=frm_viz_exec, bg="white", relief=tk.SUNKEN, text="3) Review and process images")

# overview labels
lbl_viz_run_model_warning = tk.Label(master=frm_viz_exec, bg="white", text="Please review your selections before proceeding: ")
lbl_viz_img_dir_overview = tk.Label(master=frm_viz_exec, bg="white", text="\tInput image directory:\t")
lbl_viz_msk_dir_overview = tk.Label(master=frm_viz_exec, bg="white", text="\tInput mask directory:\t")
lbl_viz_out_dir_overview = tk.Label(master=frm_viz_exec, bg="white", text="\tOutput directory:\t")
lbl_viz_thresh_overview = tk.Label(master=frm_viz_exec, bg="white", text="\tSegmentation threshold:\t")
lbl_viz_color_overview = tk.Label(master=frm_viz_exec, bg="white", text="\tSelected color:\t")

# overview data
lbl_viz_img_dir_overview_data = tk.Label(master=frm_viz_exec, bg="white", text="")
lbl_viz_msk_dir_overview_data = tk.Label(master=frm_viz_exec, bg="white", text="")
lbl_viz_out_dir_overview_data = tk.Label(master=frm_viz_exec, bg="white", text="")
lbl_viz_thresh_overview_data = tk.Label(master=frm_viz_exec, bg="white", text="")
lbl_viz_color_overview_data = tk.Label(master=frm_viz_exec, bg="white", text="")


lbl_viz_progress_status = tk.Label(master=frm_viz_exec, bg="white", text="")

btn_viz_proc_run = tk.Button(master=frm_viz_exec, bg="limegreen", text="Run", command=visualization_handler)
proc_viz_run_err_msg = tk.Label(master=frm_viz_exec, bg="white", fg="red", text="")

# adding to grid
# heading
lbl_viz_run_model_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

# left labels
lbl_viz_run_model_warning.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
lbl_viz_img_dir_overview.grid(row=2, column=0, padx=2, pady=2, sticky="nw")
lbl_viz_msk_dir_overview.grid(row=3, column=0, padx=2, pady=2, sticky="nw")
lbl_viz_out_dir_overview.grid(row=4, column=0, padx=2, pady=2, sticky="nw")
lbl_viz_thresh_overview.grid(row=5, column=0, padx=2, pady=2, sticky="nw")
lbl_viz_color_overview.grid(row=6, column=0, padx=2, pady=2, sticky="nw")
lbl_viz_progress_status.grid(row=7, column=0, padx=2, pady=2, sticky="nw")

# right data
lbl_viz_img_dir_overview_data.grid(row=2, column=1, padx=2, pady=2, sticky="nw")
lbl_viz_msk_dir_overview_data.grid(row=3, column=1, padx=2, pady=2, sticky="nw")
lbl_viz_out_dir_overview_data.grid(row=4, column=1, padx=2, pady=2, sticky="nw")
lbl_viz_thresh_overview_data.grid(row=5, column=1, padx=2, pady=2, sticky="nw")
lbl_viz_color_overview_data.grid(row=6, column=1, padx=2, pady=2, sticky="nw")

btn_viz_proc_run.grid(row=7, column=2, ipadx=10, ipady=4, padx=2, pady=2, sticky="nw")
proc_viz_run_err_msg.grid(row=7, column=1, padx=2, pady=2, sticky="w")

base_win.mainloop()