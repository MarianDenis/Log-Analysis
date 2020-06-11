import tkinter as tk
from tkinter import constants as ct


class ListApp(tk.Tk):
    def __init__(self, list_of_values, cluster_type):
        super().__init__()
        self.geometry("1550x400")

        self.list = tk.Listbox(self, width=400, height=200)

        if cluster_type == -1:
            self.list.insert(ct.END, "Noise Cluster: ")

        for x in list_of_values:
            item = ""
            for y in x:
                item = item + str(x[y]) + "    "
            self.list.insert(ct.END, item)

        self.list.pack()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_btn(self, mode):
        cmd = lambda: self.list.config(selectmode=mode)
        return tk.Button(self, command=cmd,
                         text=mode.capitalize())

    def print_selection(self):
        selection = self.list.curselection()
        print([self.list.get(i) for i in selection])

    def on_closing(self):
        self.destroy()


def show(list_of_values, dlist):
    app = ListApp(list_of_values, dlist)
    app.mainloop()
