import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory

# This file contains python code for the main GUI of the bulk image processor

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

def confirm_pos_int(inp) -> bool:
    '''
    confirms that the parameter is a positive integer
    :param inp:
    :return:
    '''

    try:
        inp_to_int = int(inp)
        if (inp_to_int > 0):
            return True
        else:
            return False
    except:
        return False

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
        err_field["text"] = "Please enter a positive integer"
    else:
        err_field["text"] = ""
        for elem in destinations:
            elem["text"] = source.get()



# initializing base gui window
base_win = tk.Tk()
base_win.title("Bulk Image Processor")
base_win.geometry("700x700")

# initializing base frame
frm_win = tk.Frame(master=base_win, bg="skyblue")
frm_win.pack(fill="both", expand=True)

# configuring details of base frame grid
frm_win.columnconfigure(0, weight=1, minsize=650)
frm_win.rowconfigure([0, 1, 2, 3], weight=1, minsize=150)

# creating frames for each step
frm_get_dir = tk.Frame(master=frm_win, bg="white", border=3)

frm_get_splits = tk.Frame(master=frm_win, bg="white", border=3)

frm_run_model = tk.Frame(master=frm_win, bg="white", border=3)

frm_result_dir = tk.Frame(master=frm_win, bg="white", border=3)

# griddying each step frame
frm_get_dir.grid(row=0, column=0, padx=5, pady=5, sticky="news")
frm_get_splits.grid(row=1, column=0, padx=5, pady=5, sticky="news")
frm_run_model.grid(row=2, column=0, padx=5, pady=5, sticky="news")
frm_result_dir.grid(row=3, column=0, padx=5, pady=5, sticky="news")

# =============================================================
# DIRECTORY ENTRY SECTION

# heading label for directory entry section
lbl_get_dir_info = tk.Label(master=frm_get_dir, bg="white", relief=tk.SUNKEN, text="1) Enter relevant directories")

# getting input directory
lbl_get_inp_dir = tk.Label(master=frm_get_dir, bg="white", border=3, text="Enter the image input directory: ")
btn_get_inp_dir = tk.Button(master=frm_get_dir, text="Select Directory...",
                            command=lambda: get_dir(lbl_confirm_inp_dir, lbl_inp_dir_overview_data))
lbl_confirm_inp_dir = tk.Label(master=frm_get_dir, bg="white", border=3, text="")

# getting output directory
# lbl_get_out_dir = tk.Label(master=frm_get_dir, bg="white", border=3, text="Enter the output directory: ")
# btn_get_out_dir = tk.Button(master=frm_get_dir, text="Select Directory...", command=lambda:get_dir(lbl_confirm_out_dir))
# lbl_confirm_out_dir = tk.Label(master=frm_get_dir, bg="white", border=3, text="")

# adding everything to grid
lbl_get_dir_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

lbl_get_inp_dir.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
btn_get_inp_dir.grid(row=1, column=1, padx=2, pady=2, sticky="nw")
lbl_confirm_inp_dir.grid(row=1, column=2, padx=2, pady=2, sticky="nw")

# lbl_get_out_dir.grid(row=2, column=0, padx=2, pady=2, sticky="nw")
# btn_get_out_dir.grid(row=2, column=1, padx=2, pady=2, sticky="nw")
# lbl_confirm_out_dir.grid(row=2, column=2, padx=2, pady=2, sticky="nw")

# ===========================================================
# SPLIT COUNT SELECTION SECTION

lbl_get_preproc_info = tk.Label(master=frm_get_splits, bg="white", relief=tk.SUNKEN, text="2) Enter preprocessing directives")

lbl_get_splits = tk.Label(master=frm_get_splits, bg="white", border=3, text="Enter the number of image splits per dimension: ")
ent_get_splits = tk.Entry(master=frm_get_splits, bg="white", width=7)
lbl_split_err_msg = tk.Label(master=frm_get_splits, bg="white", border=3, text="")
btn_split_confirmer = tk.Button(master=frm_get_splits, text="Confirm",
                                command= lambda: confirm_button(ent_get_splits, confirm_pos_int, lbl_split_err_msg, lbl_split_no_overview_data))

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
lbl_split_no_overview = tk.Label(master=frm_run_model, bg="white", text="\tNumber of splits per dimension:\t")

# overview data
lbl_model_overview_data = tk.Label(master=frm_run_model, bg="white", text="VGG16, pretrained on Khanhha's Dataset")
lbl_inp_dir_overview_data = tk.Label(master=frm_run_model, bg="white", text="")
lbl_split_no_overview_data = tk.Label(master=frm_run_model, bg="white", text="")

btn_proc_run = tk.Button(master=frm_run_model, bg="limegreen", text="Run")

# adding to grid
lbl_run_model_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

lbl_run_model_warning.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
lbl_model_overview.grid(row=2, column=0, padx=2, pady=2, sticky="nw")
lbl_inp_dir_overview.grid(row=3, column=0, padx=2, pady=2, sticky="nw")
lbl_split_no_overview.grid(row=4, column=0, padx=2, pady=2, sticky="nw")

lbl_model_overview_data.grid(row=2, column=1, padx=2, pady=2, sticky="nw")
lbl_inp_dir_overview_data.grid(row=3, column=1, padx=2, pady=2, sticky="nw")
lbl_split_no_overview_data.grid(row=4, column=1, padx=2, pady=2, sticky="nw")

btn_proc_run.grid(row=5, column=2, ipadx=10, ipady=4, padx=2, pady=2, sticky="nw")

# ===========================================================

base_win.mainloop()