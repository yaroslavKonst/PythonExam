#!/usr/bin/python3

import tkinter as tk
import sys


class Application:
    def __init__(self):
        self.args = list()
        if len(sys.argv) >= 2:
            self.args.append(sys.argv[1])
        if len(sys.argv) >= 3:
            self.args.append(sys.argv[2])
        self.main_frame = tk.Frame()
        self.main_frame.master.rowconfigure(0, weight=1)
        self.main_frame.master.columnconfigure(0, weight=1)
        self.main_frame.master.title("hdreader")
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
        self.open_button.grid(column=0, row=0)
        self.undo_button.grid(column=0, row=1)
        self.redo_button.grid(column=0, row=2)
        self.text_field = tk.Text(master=self.main_frame, undo=True, width=80,
                                  font=("Source Code Pro", 12))
        self.text_field.grid(sticky="NEWS", row=0, column=1)

    def open_dial(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def run(self):
        tk.mainloop()

App = Application()
App.run()
