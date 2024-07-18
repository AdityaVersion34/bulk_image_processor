import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory

# This file contains python code for the main GUI of the bulk image processor

def get_dir(where_to):
    filepath = askdirectory()
    if not filepath:
        return
    where_to["text"] = filepath

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
btn_get_inp_dir = tk.Button(master=frm_get_dir, text="Select Directory...", command=lambda: get_dir(lbl_confirm_inp_dir))
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

# adding to grid
lbl_get_preproc_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

lbl_get_splits.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
ent_get_splits.grid(row=1, column=1, padx=2, pady=2, sticky="nw")

# ===========================================================
# EXECUTION INFO

lbl_run_model_info = tk.Label(master=frm_run_model, bg="white", relief=tk.SUNKEN, text="3) Review and process images")

lbl_run_model_warning = tk.Label(master=frm_run_model, bg="white", text="Please review your selections before proceeding: ")
lbl_model_overview = tk.Label(master=frm_run_model, bg="white", text="\tModel Overview:\t")#VGG16, pretrained on Khanhha's Dataset")
lbl_inp_dir_overview = tk.Label(master=frm_run_model, bg="white", text="\tInput directory:\t")
lbl_split_no_overview = tk.Label(master=frm_run_model, bg="white", text="\tNumber of splits per dimension:\t")

# adding to grid
lbl_run_model_info.grid(row=0, column=0, ipadx=5, ipady=5, padx=2, pady=2, sticky="nw")

lbl_run_model_warning.grid(row=1, column=0, padx=2, pady=2, sticky="nw")
lbl_model_overview.grid(row=2, column=0, padx=2, pady=2, sticky="nw")
lbl_inp_dir_overview.grid(row=3, column=0, padx=2, pady=2, sticky="nw")
lbl_split_no_overview.grid(row=4, column=0, padx=2, pady=2, sticky="nw")

# ===========================================================

base_win.mainloop()