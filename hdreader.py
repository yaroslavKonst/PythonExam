#!/usr/bin/python3

import tkinter as tk
import sys
import os
import subprocess
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, showinfo


class Application:
    def __init__(self):
        self.in_file = None
        self.out_file = None
        if len(sys.argv) >= 2:
            self.in_file = sys.argv[1]
            self.out_file = sys.argv[1]
        if len(sys.argv) >= 3:
            self.out_file = sys.argv[2]
        self.main_frame = tk.Frame()
        self.main_frame.master.rowconfigure(0, weight=1)
        self.main_frame.master.columnconfigure(0, weight=1)
        self.update_title()
        self.main_frame.grid(sticky="NEWS")
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.button_frame = tk.Frame(master=self.main_frame)
        self.button_frame.grid(sticky="NEWS", row=0, column=0)

        self.open_button = tk.Button(master=self.button_frame, text="Open",
                                     command=self.open_dial)
        self.save_button = tk.Button(master=self.button_frame, text="Save",
                                     command=self.save_dial)
        self.saveas_button = tk.Button(master=self.button_frame, text="Save as",
                                       command=self.saveas_dial)
        self.undo_button = tk.Button(master=self.button_frame, text="Undo",
                                     command=self.undo)
        self.redo_button = tk.Button(master=self.button_frame, text="Redo",
                                     command=self.redo)
        self.open_button.grid(sticky="EW", column=0, row=0)
        self.save_button.grid(sticky="EW", column=0, row=1)
        self.saveas_button.grid(sticky="EW", column=0, row=2)
        self.undo_button.grid(sticky="EW", column=0, row=3)
        self.redo_button.grid(sticky="EW", column=0, row=4)
        self.text_field = tk.Text(master=self.main_frame, undo=True, width=80,
                                  font=("Source Code Pro", 12))
        self.text_field.grid(sticky="NEWS", row=0, column=1)
        if self.in_file:
            self.open(self.in_file)

    def update_title(self):
        self.main_frame.master.title("hdreader" + ((" " + self.in_file)
                                     if self.in_file else ""))

    def open(self, filename):
        if filename:
            if not os.path.exists(filename):
                showerror("File open error",
                          "%s\nFile does not exist." % filename)
            elif not os.path.isfile(filename):
                showerror("File open error",
                          "%s\nis not a regular file." % filename)
            else:
                status = subprocess.run(["xxd", "-g1", filename],
                                        capture_output=True)
                if status.returncode == 0:
                    text = status.stdout.decode("UTF-8")
                    self.text_field.delete("1.0", "end")
                    self.text_field.insert("1.0", text)
                    self.text_field.edit_reset()
                    self.update_title()
                    return True
                else:
                    showerror("File open error",
                              "%s\nFile can't be opened." % filename)
            self.update_title()
        return False

    def save(self, filename):
        if filename:
            text = self.text_field.get("1.0", "end").encode("UTF-8")
            status = subprocess.run(["xxd", "-r -g1", "-", filename],
                                    input=text, capture_output=True)
            if status.returncode != 0:
                showerror("File save error",
                          "%s\nFile can't be opened." % filename)

    def open_dial(self):
        filename = askopenfilename(title="Open file")
        ret = self.open(filename)
        if ret:
            self.in_file = filename
            self.out_file = filename

    def save_dial(self):
        if self.out_file:
            filename = self.out_file
        else:
            filename = asksaveasfilename(title="Save file")
            self.out_file = filename
        self.save(filename)

    def saveas_dial(self):
        filename = asksaveasfilename(title="Save file")
        self.save(filename)

    def undo(self):
        try:
            self.text_field.edit_undo()
        except Exception:
            showinfo("Undo","No changes left to undo.")

    def redo(self):
        try:
            self.text_field.edit_redo()
        except Exception:
            showinfo("Redo","Nothing to redo.")

    def run(self):
        tk.mainloop()


App = Application()
App.run()
