import datetime
import threading
import tkinter
from tkinter import ttk, messagebox

from pkg_log_analysis import main_modules as md


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Data format should be YYYY-MM-DD")


def validate_time(time_text):
    try:
        datetime.datetime.strptime(time_text, '%H:%M:%S')
    except ValueError:
        raise ValueError("Time format should be hh:mm:ss")


def validate_number(number):
    try:
        num = int(number)
        if num <= 0:
            raise ValueError("Should be more than zero logs to analyse!")
    except TypeError:
        raise TypeError("Input is not number!")


def shutdown_ttk_repeat():
    quit()


class App:
    def __init__(self, window):
        self.window = window

        self.window.title("Intrusion Detector")
        self.check_val_ddos = tkinter.BooleanVar()
        self.check_val_sqli = tkinter.BooleanVar()
        self.check_ddos = tkinter.Checkbutton(self.window, text="DDoS", var=self.check_val_ddos,
                                              command=lambda: self.sel_intrusion_type(self.check_val_ddos,
                                                                                      self.check_val_sqli))
        self.check_sqli = tkinter.Checkbutton(self.window, text="SQL Injection", var=self.check_val_sqli,
                                              command=lambda: self.sel_intrusion_type(self.check_val_ddos,
                                                                                      self.check_val_sqli))

        self.ddos_date_entry = tkinter.Entry(self.window, state='disabled')
        self.ddos_time_entry = tkinter.Entry(self.window, state='disabled')
        self.ddos_num_of_days = tkinter.Entry(self.window, state='disabled')
        self.sqli_date_entry = tkinter.Entry(self.window, state='disabled')
        self.sqli_time_entry = tkinter.Entry(self.window, state='disabled')
        self.sqli_num_of_logs_entry = tkinter.Entry(self.window, state='disabled')

        self.start_button = tkinter.Button(self.window, text="Start", command=self.tapped_start)

        self.progress = ttk.Progressbar(self.window)
        self.show_graph_button = tkinter.Button(self.window, text="Show Graph",
                                                command=lambda: self.show_plot(self.sqli_num_of_logs_entry.get()))
        self.clusters = []
        self.set_layout()
        self.window.mainloop()

    def sel_intrusion_type(self, ddos, sqli):
        if ddos.get():
            self.ddos_date_entry.config(state='normal')
            self.ddos_time_entry.config(state='normal')
            self.ddos_num_of_days.config(state='normal')
        else:
            self.ddos_date_entry.config(state='disabled')
            self.ddos_time_entry.config(state='disabled')
            self.ddos_num_of_days.config(state='disabled')
        if sqli.get():
            self.sqli_date_entry.config(state='normal')
            self.sqli_time_entry.config(state='normal')
            self.sqli_num_of_logs_entry.config(state='normal')
        else:
            self.sqli_date_entry.config(state='disabled')
            self.sqli_time_entry.config(state='disabled')
            self.sqli_num_of_logs_entry.config(state='disabled')

    def set_layout(self):
        tkinter.Label(self.window, text="Select types of attack to detect:").grid(row=0)

        self.check_ddos.grid(row=1, sticky="w")

        self.check_sqli.grid(row=2, sticky="w")

        tkinter.Label(self.window).grid(row=3)
        tkinter.Label(self.window, text="Select inputs for detecting DDOS:").grid(row=4, sticky="w")

        tkinter.Label(self.window, text="Date and Time").grid(row=5, column=0, sticky="w")

        self.ddos_date_entry.insert(0, "Date")
        self.ddos_date_entry.grid(row=5, column=1)

        self.ddos_time_entry.insert(0, "Time")
        self.ddos_time_entry.grid(row=5, column=2)

        tkinter.Label(self.window, text="Number od Days").grid(row=6, column=0, sticky="w")
        self.ddos_num_of_days.grid(row=6, column=1)

        tkinter.Label(self.window).grid(row=7)
        tkinter.Label(self.window, text="Select inputs for detecting SQLI:").grid(row=8, sticky="w")

        tkinter.Label(self.window, text="Date and Time").grid(row=9, column=0, sticky="w")

        self.sqli_date_entry.insert(0, "Date")
        self.sqli_date_entry.grid(row=9, column=1)

        self.sqli_time_entry.insert(0, "Time")
        self.sqli_time_entry.grid(row=9, column=2)

        tkinter.Label(self.window, text="Number of Logs").grid(row=10, column=0, sticky="w")

        self.sqli_num_of_logs_entry.grid(row=10, column=1)

        tkinter.Label(self.window).grid(row=11)
        # tkinter.Button(self.window, text="Start", command=self.tapped_start).grid(row=12, columnspan=3)
        self.start_button.grid(row=12, columnspan=3)

    def apply_log_analysis(self, option: str):
        if option == "10":
            md.detect_dos(self.ddos_date_entry.get(), self.ddos_time_entry.get(), self.ddos_num_of_days.get())
        elif option == "01":
            self.clusters = md.detect_sqli(self.sqli_date_entry.get(), self.sqli_time_entry.get(),
                                           self.sqli_num_of_logs_entry.get())
        else:
            print("Analysing logs for DDoS...*")
            md.detect_dos(self.ddos_date_entry.get(), self.ddos_time_entry.get(), self.ddos_num_of_days.get())
            print("Analysing logs for SQL Injection...*")
            self.clusters = md.detect_sqli(self.sqli_date_entry.get(), self.sqli_time_entry.get(),
                                           self.sqli_num_of_logs_entry.get())

    def tapped_start(self):
        if not self.check_val_sqli.get() and not self.check_val_ddos.get():
            messagebox.showerror("Warning", "Should choose at least one option!")
        try:
            if self.check_val_ddos.get():
                validate_date(self.ddos_date_entry.get())
                validate_time(self.ddos_time_entry.get())
                validate_number(self.ddos_num_of_days.get())
            if self.check_val_sqli.get():
                validate_date(self.sqli_date_entry.get())
                validate_time(self.sqli_time_entry.get())
                validate_number(self.sqli_num_of_logs_entry.get())
        except ValueError as e:
            messagebox.showerror("Warning", e)
        except TypeError as e:
            messagebox.showerror("Warning", e)

        if self.check_val_sqli.get() and self.check_val_ddos.get():
            self.loading('11')
        elif (not self.check_val_sqli.get()) and self.check_val_ddos.get():
            self.loading('10')
        elif self.check_val_sqli.get() and (not self.check_val_ddos.get()):
            self.loading('01')

    def loading(self, option):
        self.show_graph_button.grid_forget()
        self.start_button.config(state='disabled')
        self.progress.grid(row=13, columnspan=3)
        self.clusters = []
        start_bar_thread = threading.Thread(target=self.start_bar, args=(option,))
        start_bar_thread.start()

    def start_bar(self, option):
        self.progress.config(mode='indeterminate', maximum=100, value=0)
        self.progress.start(8)
        work_thread = threading.Thread(target=self.apply_log_analysis, args=(option,))
        work_thread.start()
        work_thread.join()
        self.progress.stop()
        self.progress.config(value=0, maximum=0)
        self.progress.grid_forget()
        self.start_button.config(state='normal')
        if self.check_val_sqli.get():
            self.show_graph_button.grid(row=13, columnspan=3)

    def show_plot(self, graph_size):
        try:
            gsize = int(graph_size)
            if len(self.clusters) > 0:
                md.show_graph(self.clusters, gsize)
        except TypeError:
            pass


def run_app():
    root = tkinter.Tk()
    App(root)
