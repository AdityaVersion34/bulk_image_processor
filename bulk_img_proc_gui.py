import tkinter as tk

#This file contains python code for the main GUI of the bulk image processor

#initializing base gui window
base_win = tk.Tk()
base_win.title("Bulk Image Processor")
base_win.geometry("700x700")

#initializing base frame
frm_win = tk.Frame(master=base_win, bg="maroon")
frm_win.pack(fill="both", expand=True)

#configuring details of base frame grid
frm_win.columnconfigure(0, weight=1, minsize=650)
frm_win.rowconfigure([0, 1, 2, 3], weight=1, minsize=150)

#creating frames for each step
frm_get_dir = tk.Frame(master=frm_win, bg="white", border=3)

frm_get_splits = tk.Frame(master=frm_win, bg="white", border=3)

frm_run_model = tk.Frame(master=frm_win, bg="white", border=3)

frm_result_dir = tk.Frame(master=frm_win, bg="white", border=3)

#griddying each step frame
frm_get_dir.grid(row=0, column=0, padx=5, pady=5, sticky="news")
frm_get_splits.grid(row=1, column=0, padx=5, pady=5, sticky="news")
frm_run_model.grid(row=2, column=0, padx=5, pady=5, sticky="news")
frm_result_dir.grid(row=3, column=0, padx=5, pady=5, sticky="news")

base_win.mainloop()