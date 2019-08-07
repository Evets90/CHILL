# general import
import pandas as pd
import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.ttk import Combobox
from os import path

# specific functions import
import Compare_files
import Clean_spaces
import Check_series

# engine app to switch frames
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("CHILL")
        self.geometry('1280x720')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # frames list
        self.frames = {}
        self.frames["StartPage"] = StartPage(parent=container, controller=self)
        self.frames["BasicPage"] = BasicPage(parent=container, controller=self)
        self.frames["PCSPage"] = PCSPage(parent=container, controller=self)
        self.frames["CompareFiles"] = CompareFilesPage(parent=container, controller=self)
        self.frames["CleanSpaces"] = CleanSpacesPage(parent=container, controller=self)
        self.frames["CheckSeries"] = CheckSeriesPage(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["BasicPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["PCSPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["CompareFiles"].grid(row=0, column=0, sticky="nsew")
        self.frames["CleanSpaces"].grid(row=0, column=0, sticky="nsew")
        self.frames["CheckSeries"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to CHILL (Computer-Human Interface to Learn Laziness). Please select a category", font=controller.title_font)
        label.pack(side='top', fill='x', pady=10)

        btn1 = tk.Button(self, text="Basic", command=lambda: controller.show_frame("BasicPage"))
        btn2 = tk.Button(self, text="PCS", command=lambda: controller.show_frame("PCSPage"))
        #btn3 = tk.Button(self, text="Chemical shifts", command=lambda: controller.show_frame("PCSPage"))
        #btn4 = tk.Button(self, text="Cyana", command=lambda: controller.show_frame("PCSPage"))

        btn1.pack()
        btn2.pack()
        #btn3.pack()
        #btn4.pack()

class BasicPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Basic functions.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the main page", command=lambda: controller.show_frame("StartPage"))
        btn1 = tk.Button(self, text="Compare files", command=lambda: controller.show_frame("CompareFiles"))
        btn2 = tk.Button(self, text="Clean spaces", command=lambda: controller.show_frame("CleanSpaces"))
        btn3 = tk.Button(self, text="Check series", command=lambda: controller.show_frame("CheckSeries"))
        btnback.pack()
        btn1.pack()
        btn2.pack()
        btn3.pack()

class CompareFilesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename1 = ""
        self.filename2 = ""
        title = tk.Label(self, text="Compare Files", font=controller.title_font)
        title.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the basic functions.", command=lambda: controller.show_frame("BasicPage"))
        btnback.pack()
        description = tk.Label(self, text=Compare_files.file_compare.__doc__)
        description.pack(fill="x", pady=10)
        btnfile1 = tk.Button(self, text="Choose the first file", command=self.selectfile1)
        btnfile1.pack()
        self.lab1 = tk.Label(self, text="No file selected")
        self.lab1.pack(pady=10)
        btnfile2 = tk.Button(self, text="Choose the second file", command=self.selectfile2)
        btnfile2.pack()
        self.lab2 = tk.Label(self, text="No file selected")
        self.lab2.pack(pady=10)
        btnfun = tk.Button(self, text="Compare Files", command=self.compare)
        btnfun.pack()
        self.labfun = tk.Label(self, text="")
        self.labfun.pack(pady=10)
        self.out = scrolledtext.ScrolledText(self, width=40, height=10)
        self.out.pack()

    def selectfile1(self):
        self.filename1 = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        self.lab1.configure(text=self.filename1)

    def selectfile2(self):
        self.filename2 = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        self.lab2.configure(text=self.filename2)

    def compare(self):
        if self.filename1 == "":
            messagebox.showerror("Warning", "You did not select any file 1.")
        elif self.filename2 == "":
            messagebox.showerror("Warning", "You did not select any file 2.")
        else:
            res = Compare_files.file_compare(self.filename1, self.filename2)
            output = "Files compared. Output is stored in " + path.splitext(self.filename1)[0] + "_compare_output.txt"
            self.labfun.configure(text=output)
            for item in res:
                self.out.insert('insert', item)

class CleanSpacesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename1 = ""
        title = tk.Label(self, text="Clean spaces", font=controller.title_font)
        title.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the basic functions.", command=lambda: controller.show_frame("BasicPage"))
        btnback.pack()
        description = tk.Label(self, text=Clean_spaces.clean_spaces.__doc__)
        description.pack(fill="x", pady=10)
        btnfile1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btnfile1.pack()
        self.lab1 = tk.Label(self, text="No file selected")
        self.lab1.pack(pady=10)
        btnfun = tk.Button(self, text="Clean spaces", command=self.clean)
        btnfun.pack()
        self.labfun = tk.Label(self, text="")
        self.labfun.pack(pady=10)
        self.out = scrolledtext.ScrolledText(self, width=40, height=10)
        self.out.pack()

    def selectfile1(self):
        self.filename1 = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        self.lab1.configure(text=self.filename1)

    def clean(self):
        if self.filename1 == "":
            messagebox.showerror("Warning", "You did not select any file.")
        else:
            res = Clean_spaces.clean_spaces(self.filename1)
            output = "File cleaned. Output is stored in " + path.splitext(self.filename1)[0] + "_clean.txt"
            self.labfun.configure(text=output)
            for item in res:
                self.out.insert('insert', item)

class CheckSeriesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename1 = ""
        title = tk.Label(self, text="Check series", font=controller.title_font)
        title.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the basic functions.", command=lambda: controller.show_frame("BasicPage"))
        btnback.pack()
        description = tk.Label(self, text=Check_series.check_series.__doc__)
        description.pack(fill="x", pady=10)
        btnfile1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btnfile1.pack()
        self.lab1 = tk.Label(self, text="No file selected")
        self.lab1.pack(pady=10)
        lblcombo = tk.Label(self, text="Column:")
        lblcombo.pack()
        self.combo = Combobox(self)
        self.combo.pack(pady=10)
        btnfun = tk.Button(self, text="Check series", command=self.check)
        btnfun.pack()
        self.labfun = tk.Label(self, text="")
        self.labfun.pack(pady=10)
        self.out = scrolledtext.ScrolledText(self, width=40, height=10)
        self.out.pack()

    def selectfile1(self):
        self.filename1 = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        self.lab1.configure(text=self.filename1)
        dt = pd.read_csv(self.filename1, sep=' ', header=None)
        colnum = []
        for num in range(0, int(len(dt.columns))):
            colnum.append(num+1)
        self.combo['values'] = colnum

    def check(self):
        if self.filename1 == "":
            messagebox.showerror("Warning", "You did not select any file.")
        elif self.combo.get() == "":
            messagebox.showerror("Warning", "You did not select any column.")
        else:
            dt = pd.read_csv(self.filename1, sep=' ', header=None)
            col = int(self.combo.get()) - 1
            try:
                dt[col] + 1
            except TypeError:
                messagebox.showerror("Error", "The column you selected does not contain only numbers.")
        t, list = Check_series.check_series(self.filename1, int(self.combo.get()))
        self.labfun.configure(text="Checked.")
        total = "Total missing elements: " + str(t) + "\n"
        self.out.insert('insert', total)
        for item in list:
            self.out.insert('insert', item)

class PCSPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="PCS functions.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the main page.", command=lambda: controller.show_frame("StartPage"))
        btnback.pack()

# start
if __name__ == "__main__":
    start = App()
    start.mainloop()