#!/usr/bin/python3

import tkinter as tk
import sys
import os
import subprocess
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror


class Application:
    def __init__(self):
        self.in_file = None
        self.out_file = None
        if len(sys.argv) >= 2:
            self.in_file = sys.argv[1]
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
        self.undo_button = tk.Button(master=self.button_frame, text="Undo",
                                     command=self.undo, state=tk.DISABLED)
        self.redo_button = tk.Button(master=self.button_frame, text="Redo",
                                     command=self.redo, state=tk.DISABLED)
        self.open_button.grid(sticky="EW", column=0, row=0)
        self.undo_button.grid(sticky="EW", column=0, row=1)
        self.redo_button.grid(sticky="EW", column=0, row=2)
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
                self.in_file = None
            elif not os.path.isfile(filename):
                showerror("File open error",
                          "%s\nis not a regular file." % filename)
                self.in_file = None
            else:
                self.in_file = filename
                self.update_title()
                text = subprocess.run(["xxd", "-g1", filename],
                                      capture_output=True).stdout\
                    .decode("UTF-8")
                self.text_field.insert("1.0", text)

    def open_dial(self):
        filename = askopenfilename(title="Open file")
        self.open(filename)

    def undo(self):
        self.text_field.edit_undo()

    def redo(self):
        self.text_field.edit_redo()

    def run(self):
        tk.mainloop()


App = Application()
App.run()
