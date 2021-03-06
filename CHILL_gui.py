# General import
import sys
import pandas as pd
import tkinter as tk
import inspect
import os
import re
import pyperclip
from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import PhotoImage
from tkinter.ttk import Combobox
from os import path
from pathlib import Path
from PIL import Image, ImageTk

# Specific functions import
import Compare_files
import Clean_spaces
import Check_series
import NPC_conversion_suite
import Randomization
import Range_deletion
import Mapping
import Pcs_subset
import Add_module
import Increased_mapped
import OVW_Analyze_overview
import OVW_Analyze_violations
import OVW_Analyze_methyl_violations
import CYANA_batch_iteration
import CYANA_test_input
import UPL_Side_chains_manager
import Average_structures
import Journal_club
import Journal_club_special


# Version
version = "Version: 0.034"

# Logos paths
logoSaS = Path.cwd() / "Logos/SaS.gif"
logochill = Path.cwd() / "Logos/Chill.png"

# Print logger used for redirect the print() in python to a window in tkinter
class PrintLogger():
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert(tk.END, text)

    def flush(self):
        pass

# Engine app to switch frames
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
        self.frames["NPCConversionSuite"] = NPCConversionSuitePage(parent=container, controller=self)
        self.frames["RandomizationPage"] = RandomizationPage(parent=container, controller=self)
        self.frames["RangeDeletionPage"] = RangeDeletionPage(parent=container, controller=self)
        self.frames["Mapping"] = MappingPage(parent=container, controller=self)
        self.frames["PcsSubset"] = PcsSubsetPage(parent=container, controller=self)
        self.frames["AddModulePage"] = AddModulePage(parent=container, controller=self)
        self.frames["IncreaseMappedPage"] = IncreaseMappedPage(parent=container, controller=self)
        self.frames["CyanaPage"] = CyanaPage(parent=container, controller=self)
        self.frames["CompareFiles"] = CompareFilesPage(parent=container, controller=self)
        self.frames["CleanSpaces"] = CleanSpacesPage(parent=container, controller=self)
        self.frames["CheckSeries"] = CheckSeriesPage(parent=container, controller=self)
        self.frames["OVWAnalyzeOverview"] = OVWAnalyzeOverview(parent=container, controller=self)
        self.frames["OVWAnalyzeViolations"] = OVWAnalyzeViolations(parent=container, controller=self)
        self.frames["OVWAnalyzemethylviolationsPage"] = OVWAnalyzemethylviolationsPage(parent=container, controller=self)
        self.frames["CYANABatchIterationPage"] = CYANABatchIterationPage(parent=container, controller=self)
        self.frames["CYANATestinputPage"] = CYANATestinputPage(parent=container, controller=self)
        self.frames["UPLSidechainsmanagerPage"] = UPLSidechainsmanagerPage(parent=container, controller=self)
        self.frames["PDBPage"] = PDBPage(parent=container, controller=self)
        self.frames["AveragestructuresPage"] = AveragestructuresPage(parent=container, controller=self)
        self.frames["WebScrapingPage"] = WebScrapingPage(parent=container, controller=self)
        self.frames["JournalClub"] = JournalClubPage(parent=container, controller=self)
        self.frames["JournalClubSpecial"] = JournalClubSpecialPage(parent=container, controller=self)


        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["BasicPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["PCSPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["NPCConversionSuite"].grid(row=0, column=0, sticky="nsew")
        self.frames["RandomizationPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["RangeDeletionPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["Mapping"].grid(row=0, column=0, sticky="nsew")
        self.frames["PcsSubset"].grid(row=0, column=0, sticky="nsew")
        self.frames["AddModulePage"].grid(row=0, column=0, sticky="nsew")
        self.frames["IncreaseMappedPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["CyanaPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["CompareFiles"].grid(row=0, column=0, sticky="nsew")
        self.frames["CleanSpaces"].grid(row=0, column=0, sticky="nsew")
        self.frames["CheckSeries"].grid(row=0, column=0, sticky="nsew")
        self.frames["OVWAnalyzeOverview"].grid(row=0, column=0, sticky="nsew")
        self.frames["OVWAnalyzeViolations"].grid(row=0, column=0, sticky="nsew")
        self.frames["OVWAnalyzemethylviolationsPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["CYANABatchIterationPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["CYANATestinputPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["UPLSidechainsmanagerPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["PDBPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["AveragestructuresPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["WebScrapingPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["JournalClub"].grid(row=0, column=0, sticky="nsew")
        self.frames["JournalClubSpecial"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Logos
        zoom = 0.2
        image = Image.open(logoSaS)
        image2 = Image.open(logochill)
        pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])
        img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
        img2 = ImageTk.PhotoImage(image2.resize((300, 600)))
        logo1 = tk.Label(self, image=img, anchor='nw')
        logo1.image = img
        logo2 = tk.Label(self, image=img2)
        logo2.image = img2
        logo2.pack(side="left", fill='both')

        # Title
        label = tk.Label(self, text="Please select a category", font=controller.title_font)
        label.pack(side='top', fill='x', pady=10)

        # Version
        global version
        labversion = tk.Label(self, text=version, anchor='se')
        labversion.place(rely=1.0, relx=1.0, x=-5, y=-25, anchor='se')
        btnversion = tk.Button(self, text="What's new?", anchor='se', command=self.get_version_log)
        btnversion.place(rely=1.0, relx=1.0, x=-5, y=0, anchor='se')

        # Catalogue
        btncatalogue = tk.Button(self, text="Function Catalogue", anchor='sw', command=self.get_catalogue)
        btncatalogue.pack(side='bottom', pady=10)
        labcatalogue = tk.Label(self, text="...or check out the functions summary", anchor='sw', font=controller.title_font)
        labcatalogue.pack(side='bottom')

        # Buttons
        btn1 = tk.Button(self, text="Basic", command=lambda: controller.show_frame("BasicPage"))
        btn2 = tk.Button(self, text="PCS", command=lambda: controller.show_frame("PCSPage"))
        btn3 = tk.Button(self, text="PDB", command=lambda: controller.show_frame("PDBPage"))
        btn4 = tk.Button(self, text="Cyana", command=lambda: controller.show_frame("CyanaPage"))
        btn5 = tk.Button(self, text="Web Scraping", command=lambda: controller.show_frame("WebScrapingPage"))
        btn1.pack(pady=10)
        btn2.pack(pady=10)
        btn3.pack(pady=10)
        btn4.pack(pady=10)
        btn5.pack(pady=10)

    def get_catalogue(self):
        # Variable
        loc = os.getcwd() + "/CHILL_catalogue.txt"
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Functions Catalogue")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=50)
        t.tag_configure('category', foreground='purple')
        t.tag_configure('function_name', foreground='red')
        # Get Text
        rloc = open(loc, 'r')
        for line in rloc:
            if "---" in line:
                t.insert('insert', line, 'category')
            elif ">" in line[0]:
                splitted = line.split(":")
                t.insert('insert', splitted[0], 'function_name')
                try:
                    t.insert('insert', splitted[1], 'description')
                except IndexError:
                    pass
            else:
                t.insert('insert', line, 'other')
        t.pack()

    def get_version_log(self):
        # Variable
        loc = os.getcwd() + "/Versions_log"
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("What's new?")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=50)
        t.tag_configure('version', foreground='purple')
        t.tag_configure('title', foreground='red')
        # Get Text
        rloc = open(loc, 'r')
        for line in rloc:
            if "VERSION" in line:
                t.insert('insert', line, 'title')
            elif re.match("v\d.\d", line):
                t.insert('insert', line, 'version')
            else:
                t.insert('insert', line, 'other')
        t.pack()

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
        btnback.pack(pady=10)
        btn1.pack(pady=10)
        btn2.pack(pady=10)
        btn3.pack(pady=10)

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
        self.out = scrolledtext.ScrolledText(self, width=100, height=18)
        self.out.pack()
        pl = PrintLogger(self.out)
        sys.stdout = pl
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

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
            Compare_files.file_compare(self.filename1, self.filename2)
            output = "Files compared."
            self.labfun.configure(text=output)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Compare_files)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class CleanSpacesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename1 = ""
        title = tk.Label(self, text="Clean spaces", font=controller.title_font)
        title.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the basic functions.", command=lambda: controller.show_frame("BasicPage"))
        btnback.pack(pady=10)
        description = tk.Label(self, text=Clean_spaces.clean_spaces.__doc__)
        description.pack(pady=10, fill='x')
        btnfile1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btnfile1.pack(pady=10)
        self.lab1 = tk.Label(self, text="No file selected")
        self.lab1.pack(pady=10)
        btnfun = tk.Button(self, text="Clean spaces", command=self.clean)
        btnfun.pack(pady=10)
        self.labfun = tk.Label(self, text="")
        self.labfun.pack(pady=10)
        self.out = scrolledtext.ScrolledText(self, width=100, height=18)
        self.out.pack(pady=10)
        pl = PrintLogger(self.out)
        sys.stdout = pl
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')


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
            #for item in res:
            #    self.out.insert('insert', item)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Clean_spaces)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

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
        self.out = scrolledtext.ScrolledText(self, width=100, height=18)
        self.out.pack()
        pl = PrintLogger(self.out)
        sys.stdout = pl
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.filename1 = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        self.lab1.configure(text=self.filename1)
        dt = pd.read_csv(self.filename1, sep='\s+', header=None)
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
            dt = pd.read_csv(self.filename1, sep='\s+', header=None)
            col = int(self.combo.get()) - 1
            try:
                dt[col] + 1
            except TypeError:
                messagebox.showerror("Error", "The column you selected does not contain only numbers.")
        t, list = Check_series.check_series(self.filename1, int(self.combo.get()))
        self.labfun.configure(text="Checked.")
        total = "Total missing elements: " + str(t) + "\n"
        self.out.delete('1.0', tk.END)
        self.out.insert('insert', total)
        for item in list:
            self.out.insert('insert', item)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Check_series)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class PCSPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="PCS functions.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the main page.", command=lambda: controller.show_frame("StartPage"))
        btnback.pack(pady=10)
        btn1 = tk.Button(self, text="NPC: conversion suite", command=lambda: controller.show_frame("NPCConversionSuite"))
        btn1.pack(pady=10)
        btn2 = tk.Button(self, text="Randomization", command=lambda: controller.show_frame("RandomizationPage"))
        btn2.pack(pady=10)
        btn3 = tk.Button(self, text="Range deletion", command=lambda: controller.show_frame("RangeDeletionPage"))
        btn3.pack(pady=10)
        btn4 = tk.Button(self, text="Mapping", command=lambda: controller.show_frame("Mapping"))
        btn4.pack(pady=10)
        btn5 = tk.Button(self, text="Get subset", command=lambda: controller.show_frame("PcsSubset"))
        btn5.pack(pady=10)
        btn6 = tk.Button(self, text="Add module", command=lambda: controller.show_frame("AddModulePage"))
        btn6.pack(pady=10)
        btn7 = tk.Button(self, text="Increase mapped", command=lambda: controller.show_frame("IncreaseMappedPage"))
        btn7.pack(pady=10)

class NPCConversionSuitePage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="NPC: conversion suite", font=controller.title_font)
        title.grid(column=1, columnspan=5, row=1)
        btnback = tk.Button(self, text="Go back to the PCS functions.", command=lambda: controller.show_frame("PCSPage"))
        btnback.grid(column=1, columnspan=5, pady=10, row=2)
        description = tk.Label(self, text=NPC_conversion_suite.general_docstring.__doc__)
        description.grid(column=1, columnspan=5, pady=10, row=3)
        # Specific
        self.file1 = ""
        self.file2 = ""
        self.file3 = ""
        # Left
        lbl1 = tk.Label(self, text="Conversion", font='Arial 16 bold')
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        lbl2 = tk.Label(self, text="Select the .npc file")
        lbl2.grid(column=1, row=5, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=6)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=6)
        lbl3 = tk.Label(self, text="Select the .seq file")
        lbl3.grid(column=1, row=7, pady=10, columnspan=2)
        btn2 = tk.Button(self, text="Choose the file", command=self.selectfile2)
        btn2.grid(column=1, row=8)
        self.labfile2 = tk.Label(self, text="No file selected")
        self.labfile2.grid(column=2, row=8)
        lblT = tk.Label(self, text="Tolerance:")
        lblT.grid(column=1, row=9, pady=10)
        self.entryT = tk.Entry(self, width=5)
        self.entryT.grid(column=2, row=9, pady=10)
        lblW = tk.Label(self, text="Weight:")
        lblW.grid(column=1, row=10, pady=10)
        self.entryW = tk.Entry(self, width=5)
        self.entryW.grid(column=2, row=10, pady=10)
        lblS = tk.Label(self, text="Sample:")
        lblS.grid(column=1, row=11, pady=10)
        self.entryS = tk.Entry(self, width=5)
        self.entryS.grid(column=2, row=11, pady=10)
        btnfunC = tk.Button(self, text="Convert", command=self.convertnpc, foreground='red')
        btnfunC.grid(column=1, row=12, pady=10, columnspan=2)
        # Middle
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=7)
        # Right
        lbl4 = tk.Label(self, text="Deletion", font='Arial 16 bold')
        lbl4.grid(column=4, row=4, pady=10, columnspan=2)
        lbl5 = tk.Label(self, text="Select the .pcs file")
        lbl5.grid(column=4, row=5, pady=10, columnspan=2)
        btn3 = tk.Button(self, text="Choose the file", command=self.selectfile3)
        btn3.grid(column=4, row=6, padx=10)
        self.labfile3 = tk.Label(self, text="No file selected")
        self.labfile3.grid(column=5, row=6)
        lblM = tk.Label(self, text="Mode:")
        lblM.grid(column=4, row=7, pady=10)
        self.comboM = Combobox(self, width=20, values=NPC_conversion_suite.modes)
        self.comboM.bind('<<ComboboxSelected>>', self.mode_action)
        self.comboM.grid(column=5, row=7, pady=10)
        btnM = tk.Button(self, text="Mode Info", command=self.show_modes_info)
        btnM.grid(column=5, row=8)
        btnfunD = tk.Button(self, text="Delete", command=self.deletenpc, foreground='red')
        btnfunD.grid(column=4, row=9, pady=10, columnspan=2)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
        # TODO: add header functionality

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("NPC files", ".npc")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def selectfile2(self):
        self.file2 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Sequence files", ".seq")])
        self.labfile2.configure(text=os.path.basename(self.file2))

    def convertnpc(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did not select any .npc file.")
        elif self.file2 == "":
            messagebox.showerror("Warning", "You did not select any .seq file.")
        elif self.entryT.get() == "":
            messagebox.showerror("Warning", "You did not select any tolerance.")
        elif self.entryS.get() == "":
            messagebox.showerror("Warning", "You did not select any sample.")
        elif self.entryW.get() == "":
            messagebox.showerror("Warning", "You did not select any weight.")
        else:
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            #pl = PrintLogger(self.out)
            #sys.stdout = pl
            newname, df = NPC_conversion_suite.conversion(self.file1, self.file2, self.entryT.get(), self.entryS.get(), self.entryW.get())
            stored = "Output stored in: " + newname
            self.lblout.configure(text=stored)
            self.out.insert('insert', df)

    def selectfile3(self):
        self.file3 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile3.configure(text=os.path.basename(self.file3))

    def mode_action(self, event):
        if self.comboM.get() == "Custom":
            def okay():
                """Clears the Journal_club.custom list, store the Entry() widget text in that list (comma separated) and closes the popup window"""
                eget = e.get().split(", ")
                NPC_conversion_suite.modeC.clear()
                for ele in eget:
                    NPC_conversion_suite.modeC.append(ele)
                win.destroy()
            win = tk.Toplevel()
            win.attributes('-topmost', 1)
            win.wm_title("Custom Atoms")
            # Label
            l = tk.Label(win, text="Insert the atoms you want to keep after the deletion, separated by a comma.")
            l.grid(row=0, column=0)
            # Entry
            e = tk.Entry(win)
            e.grid(row=1, column=0)
            # Button
            b = tk.Button(win, text="Okay", command=okay)
            b.grid(row=2, column=0)

    def show_modes_info(self):
        if self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        else:
            mode = self.comboM.get()
            keywords = NPC_conversion_suite.modes_dictionary[mode]
            pl = PrintLogger(self.out)
            sys.stdout = pl
            messagebox.showinfo("The following atoms will be kept", ", ".join(keywords))

    def deletenpc(self):
        if self.file3 == "":
            messagebox.showerror("Warning", "You did not select any file.")
        elif self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        else:
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            newname, df = NPC_conversion_suite.deletion(self.file3, self.comboM.get())
            stored = "Output stored in: " + newname
            self.lblout.configure(text=stored)
            self.out.insert('insert', df)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(NPC_conversion_suite)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class RandomizationPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Randomization", font=controller.title_font)
        title.grid(column=1, columnspan=2, row=1)
        btnback = tk.Button(self, text="Go back to the PCS functions.", command=lambda: controller.show_frame("PCSPage"))
        btnback.grid(column=1, columnspan=2, pady=10, row=2)
        description = tk.Label(self, text=Randomization.randomization.__doc__)
        description.grid(column=1, columnspan=2, pady=10, row=3)
        # Specific
        self.file1 = ""
        # Left
        lbl1 = tk.Label(self, text="Select the .pcs file")
        lbl1.grid(column=1, row=4, pady=10)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=1, row=6)
        lbl2 = tk.Label(self, text="Select the % of pcs to keep.")
        lbl2.grid(column=1, row=7, pady=10)
        self.entryP = tk.Entry(self, width=5)
        self.entryP.grid(column=1, row=8, pady=10)
        btnfun = tk.Button(self, text="Randomize", command=self.randomize_pcs, foreground='red')
        btnfun.grid(column=1, row=9, pady=10)
        # Right
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=2, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=2, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def randomize_pcs(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did not select any pcs file.")
        elif self.entryP.get() == "":
            messagebox.showerror("Warning", "You did not input any %.")
        else:
            try:
                val = int(self.entryP.get())
            except ValueError:
                messagebox.showerror("Warning", "Please input a numeric value.")
            try:
                int(self.entryP.get()) + 1
            except TypeError:
                messagebox.showerror("Warning", "Please input a numeric value between 100 and 0.")
            if int(self.entryP.get()) > 100 or int(self.entryP.get()) <= 0:
                messagebox.showerror("Warning", "Please input a numeric value between 100 and 0.")
            else:
                self.out.delete('1.0', tk.END)
                self.lblout.configure(text="")
                pl = PrintLogger(self.out)
                sys.stdout = pl
                newname, df = Randomization.randomization(self.file1, (int(self.entryP.get())/100))
                stored = "Output stored in: " + newname
                self.lblout.configure(text=stored)
                self.out.insert('insert', df)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Randomization)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class RangeDeletionPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Range deletion", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the PCS functions.", command=lambda: controller.show_frame("PCSPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=Range_deletion.pcs_range_deletion.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        self.header = 0
        # Left
        lbl1 = tk.Label(self, text="Select the .pcs file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5)
        lbl2 = tk.Label(self, text="Select the limits of the deletion (included).")
        lbl2.grid(column=1, row=6, pady=10, columnspan=2)
        lbl3 = tk.Label(self, text="Column")
        lbl3.grid(column=1, row=7, pady=10)
        self.comboC = Combobox(self, width=10, values=["Residue Number", "PCS", "Sample"])
        self.comboC.bind('<<ComboboxSelected>>', self.get_limits)
        self.comboC.grid(column=2, row=7, pady=10)
        self.comboC['state'] = 'disabled'
        lbl4 = tk.Label(self, text="Start")
        lbl4.grid(column=1, row=8, pady=10)
        self.comboMin = Combobox(self, width=5, values="")
        self.comboMin.grid(column=2, row=8, pady=10)
        self.comboMin['state'] = 'disabled'
        lbl5 = tk.Label(self, text="End")
        lbl5.grid(column=1, row=9, pady=10)
        self.comboMax = Combobox(self, width=5, values="")
        self.comboMax.grid(column=2, row=9, pady=10)
        self.comboMax['state'] = 'disabled'
        self.CheckVar1 = tk.IntVar()
        chk1 = tk.Checkbutton(self, text="inverse", variable=self.CheckVar1, onvalue=1, offvalue=0)
        chk1.grid(column=2, row=10, pady=10)
        btnfun = tk.Button(self, text="Delete", command=self.delete_range, foreground='red')
        btnfun.grid(column=1, row=11, pady=10, columnspan=2)
        # Right
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile1.configure(text=os.path.basename(self.file1))
        self.comboC['state'] = 'enabled'

    def get_limits(self, event):
        with open(self.file1) as f:
            if f.readline().strip()[:8] == "#Sample " or f.readline().strip()[:8] == "# Sample":
                self.header = 1
        if self.header == 1:
            mydf = pd.read_csv(self.file1, sep="\s+", header=2,
                               names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
        else:
            mydf = pd.read_csv(self.file1, sep="\s+", names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
        elements = round(mydf[self.comboC.get()], 3).drop_duplicates().sort_values().to_list()
        self.comboMin['values'] = elements
        self.comboMax['values'] = elements
        self.comboMin['state'] = 'enabled'
        self.comboMax['state'] = 'enabled'

    def delete_range(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did not select any pcs file.")
        elif self.comboMin.get() == "" or self.comboMax.get() == "":
            messagebox.showerror("Warning", "You did not select the limits.")
        else:
            pl = PrintLogger(self.out)
            sys.stdout = pl
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            if self.CheckVar1.get() == 1:
                newname, df = Range_deletion.pcs_range_deletion(self.file1, float(self.comboMin.get()), float(self.comboMax.get()), self.comboC.get(), header=self.header, inverse="on")
            else:
                newname, df = Range_deletion.pcs_range_deletion(self.file1, float(self.comboMin.get()),float(self.comboMax.get()), self.comboC.get(),header=self.header)
            stored = "Output stored in: " + newname
            self.lblout.configure(text=stored)
            self.out.insert('insert', df)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Range_deletion)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class MappingPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Mapping", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the PCS functions.", command=lambda: controller.show_frame("PCSPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=Mapping.mapping.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        self.file2 = ""
        # Left
        lbl1 = tk.Label(self, text="Select the 'key' .pcs file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5)
        lbl2 = tk.Label(self, text="Select the 'map' .pcs file")
        lbl2.grid(column=1, row=6, pady=10, columnspan=2)
        btn2 = tk.Button(self, text="Choose the file", command=self.selectfile2)
        btn2.grid(column=1, row=7, pady=10)
        self.labfile2 = tk.Label(self, text="No file selected")
        self.labfile2.grid(column=2, row=7)
        btnfun = tk.Button(self, text="Map", command=self.do_mapping, foreground='red')
        btnfun.grid(column=1, row=11, pady=10, columnspan=2)
        # Right
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def selectfile2(self):
        self.file2 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile2.configure(text=os.path.basename(self.file2))

    def do_mapping(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did not select any 'key' .pcs file.")
        elif self.file2 == "":
            messagebox.showerror("Warning", "You did not select any 'map' .pcs file.")
        else:
            pl = PrintLogger(self.out)
            sys.stdout = pl
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            newname, df = Mapping.mapping(self.file1, self.file2)
            stored = "Output stored in: " + newname
            self.lblout.configure(text=stored)
            self.out.insert('insert', df)



    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Mapping)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class PcsSubsetPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Get subset", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the PCS functions.", command=lambda: controller.show_frame("PCSPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=Pcs_subset.pcs_subset.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        # Left
        lbl1 = tk.Label(self, text="Select the .pcs file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5)
        lblM = tk.Label(self, text="Mode:")
        lblM.grid(column=1, row=6, pady=10)
        self.comboM = Combobox(self, width=15, values=["Percentage", "Integer"])
        self.comboM.bind('<<ComboboxSelected>>', self.mode_action)
        self.comboM['state'] = 'disabled'
        self.comboM.grid(column=2, row=6, pady=10)
        lblV = tk.Label(self, text="Subset value:")
        lblV.grid(column=1, row=7, pady=10)
        self.entryV = tk.Entry(self, width=5)
        self.entryV['state'] = 'disabled'
        self.entryV.grid(column=2, row=7, pady=10)
        lblS = tk.Label(self, text="Seed:")
        lblS.grid(column=1, row=8, pady=10)
        self.entryS = tk.Entry(self, width=5)
        self.entryS['state'] = 'disabled'
        self.entryS.grid(column=2, row=8, pady=10)
        btnfun = tk.Button(self, text="Get subset", command=self.get_subset, foreground='red')
        btnfun.grid(column=1, row=9, pady=10, columnspan=2)
        # Right
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile1.configure(text=os.path.basename(self.file1))
        self.comboM['state'] = 'enabled'

    def mode_action(self, event):
        self.entryV['state'] = 'normal'
        self.entryS['state'] = 'normal'


    def get_subset(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did not select any pcs file.")
        elif self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        elif self.entryV.get() == "":
            messagebox.showerror("Warning", "You did not select any subset value.")
        elif self.comboM.get() == "Percentage" and not 0 < int(self.entryV.get()) <= 100:
            messagebox.showerror("Warning", "In percentage mode insert a subset value between 1 and 100.")
        elif self.comboM.get() == "Integer" and (float(self.entryV.get()).is_integer() == False or int(self.entryV.get()) < 1):
            messagebox.showerror("Warning", "In integer mode insert an integer as subset value (min 1).")
        else:
            pl = PrintLogger(self.out)
            sys.stdout = pl
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            if self.entryS.get() == "":
                newname, df = Pcs_subset.pcs_subset(self.file1, int(self.entryV.get()), self.comboM.get())
            else:
                newname, df = Pcs_subset.pcs_subset(self.file1, int(self.entryV.get()), self.comboM.get(), int(self.entryS.get()))
            stored = "Output stored in: " + newname
            self.lblout.configure(text=stored)
            self.out.insert('insert', df)


    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Pcs_subset)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class AddModulePage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Add module", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the PCS functions.",
                            command=lambda: controller.show_frame("PCSPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=Add_module.add_module.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        self.file2 = ""
        # Left
        lbl1 = tk.Label(self, text="Select the 'key' .pcs file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5)
        lbl2 = tk.Label(self, text="Select the 'map' .pcs file")
        lbl2.grid(column=1, row=6, pady=10, columnspan=2)
        btn2 = tk.Button(self, text="Choose the file", command=self.selectfile2)
        btn2.grid(column=1, row=7, pady=10)
        self.labfile2 = tk.Label(self, text="No file selected")
        self.labfile2.grid(column=2, row=7)
        lblM = tk.Label(self, text="Module:")
        lblM.grid(column=1, row=8, pady=10)
        self.comboM = Combobox(self, width=15, values=["Y", "M1", "M2", "M3", "M4", "A"])
        self.comboM.grid(column=2, row=8, pady=10)
        self.CheckVar1 = tk.IntVar()
        chk1 = tk.Checkbutton(self, text="Check sequence integrity", variable=self.CheckVar1, onvalue=1, offvalue=0)
        chk1.grid(column=2, row=9, pady=10)
        btnfun = tk.Button(self, text="Add module", command=self.do_add_module, foreground='red')
        btnfun.grid(column=1, row=10, pady=10, columnspan=2)
        # Right
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__),
                                                filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def selectfile2(self):
        self.file2 = filedialog.askopenfilename(initialdir=path.dirname(__file__),
                                                filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile2.configure(text=os.path.basename(self.file2))

    def do_add_module(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did not select any 'key' .pcs file.")
        elif self.file2 == "":
            messagebox.showerror("Warning", "You did not select any 'map' .pcs file.")
        elif self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any module.")
        else:
            pl = PrintLogger(self.out)
            sys.stdout = pl
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            if self.CheckVar1.get() == 1:
                newname, df = Add_module.add_module(self.file1, self.file2, self.comboM.get(), Test1=1)
            else:
                newname, df = Add_module.add_module(self.file1, self.file2, self.comboM.get())
            stored = "Output stored in: " + newname
            self.lblout.configure(text=stored)
            self.out.insert('insert', df)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Add_module)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class IncreaseMappedPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Increase mapped", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the PCS functions.",
                            command=lambda: controller.show_frame("PCSPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=Increased_mapped.increase_mapped.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        self.file2 = ""
        # Left
        lbl1 = tk.Label(self, text="Select the 'map' .pcs file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5)
        lbl2 = tk.Label(self, text="Select the 'mapped' .pcs file")
        lbl2.grid(column=1, row=6, pady=10, columnspan=2)
        btn2 = tk.Button(self, text="Choose the file", command=self.selectfile2)
        btn2.grid(column=1, row=7, pady=10)
        self.labfile2 = tk.Label(self, text="No file selected")
        self.labfile2.grid(column=2, row=7)
        lblM = tk.Label(self, text="Mode:")
        lblM.grid(column=1, row=8, pady=10)
        self.comboM = Combobox(self, width=15, values=["Percentage", "Integer"])
        self.comboM.bind('<<ComboboxSelected>>', self.mode_action)
        self.comboM.grid(column=2, row=8, pady=10)
        lblV = tk.Label(self, text="Subset value:")
        lblV.grid(column=1, row=9, pady=10)
        self.entryV = tk.Entry(self, width=5)
        self.entryV['state'] = 'disabled'
        self.entryV.grid(column=2, row=9, pady=10)
        lblS = tk.Label(self, text="Seed:")
        lblS.grid(column=1, row=10, pady=10)
        self.entryS = tk.Entry(self, width=5)
        self.entryS['state'] = 'disabled'
        self.entryS.grid(column=2, row=10, pady=10)
        #self.CheckVar1 = tk.IntVar()
        #chk1 = tk.Checkbutton(self, text="Check sequence integrity", variable=self.CheckVar1, onvalue=1, offvalue=0)
        #chk1.grid(column=2, row=9, pady=10)
        btnfun = tk.Button(self, text="Add module", command=self.do_increase_mapped, foreground='red')
        btnfun.grid(column=1, row=11, pady=10, columnspan=2)
        # Right
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__),
                                                filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def selectfile2(self):
        self.file2 = filedialog.askopenfilename(initialdir=path.dirname(__file__),
                                                filetypes=[("Pseudocontact shift files", ".pcs")])
        self.labfile2.configure(text=os.path.basename(self.file2))

    def mode_action(self, event):
        self.entryV['state'] = 'normal'
        self.entryS['state'] = 'normal'

    def do_increase_mapped(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did not select any 'map' .pcs file.")
        elif self.file2 == "":
            messagebox.showerror("Warning", "You did not select any 'mapped' .pcs file.")
        elif self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        elif self.entryV.get() == "":
            messagebox.showerror("Warning", "You did not select any increase value.")
        elif self.comboM.get() == "Percentage" and not 0 < int(self.entryV.get()) <= 100:
            messagebox.showerror("Warning", "In percentage mode insert an increase value between 1 and 100.")
        elif self.comboM.get() == "Integer" and (
                float(self.entryV.get()).is_integer() == False or int(self.entryV.get()) < 1):
            messagebox.showerror("Warning", "In integer mode insert an integer as subset value (min 1).")
        else:
            pl = PrintLogger(self.out)
            sys.stdout = pl
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            if self.entryS.get() == "":
                newname, df = Increased_mapped.increase_mapped(self.file1, self.file2, int(self.entryV.get()), self.comboM.get())
            else:
                newname, df = Increased_mapped.increase_mapped(self.file1, self.file2,
                                                               int(self.entryV.get()), self.comboM.get(), seed=int(self.entryS.get()))
            stored = "Output stored in: " + newname
            self.lblout.configure(text=stored)
            self.out.insert('insert', df)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Increased_mapped)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class CyanaPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Cyana functions.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the main page", command=lambda: controller.show_frame("StartPage"))
        btnback.pack(pady=10)
        btn1 = tk.Button(self, text="OVW: Analyze overview", command=lambda: controller.show_frame("OVWAnalyzeOverview"))
        btn1.pack(pady=10)
        btn2 = tk.Button(self, text="OVW: Analyze violations",command=lambda: controller.show_frame("OVWAnalyzeViolations"))
        btn2.pack(pady=10)
        btn3 = tk.Button(self, text="OVW: Analyze methyl violations", command=lambda: controller.show_frame("OVWAnalyzemethylviolationsPage"))
        btn3.pack(pady=10)
        btn4 = tk.Button(self, text="CYANA: Batch iteration",command=lambda: controller.show_frame("CYANABatchIterationPage"))
        btn4.pack(pady=10)
        btn5 = tk.Button(self, text="CYANA: Test input",command=lambda: controller.show_frame("CYANATestinputPage"))
        btn5.pack(pady=10)
        btn6 = tk.Button(self, text="UPL: Side chains manager",command=lambda: controller.show_frame("UPLSidechainsmanagerPage"))
        btn6.pack(pady=10)

class OVWAnalyzeOverview(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="OVW: Analyze overview", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the cyana functions.", command=lambda: controller.show_frame("CyanaPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=OVW_Analyze_overview.general_docstring.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.filelist1 = ""
        self.filelist2 = ""
        self.filelist3 = ""
        # Column 1
        lbl1 = tk.Label(self, text="Target Function")
        lbl1.grid(column=1, row=4)
        btn1 = tk.Button(self, text="Choose the files", command=self.selectlist1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=1, row=6, pady=10)
        btnfun1 = tk.Button(self, text="Start", command=self.get_tf)
        btnfun1.grid(column=1, row=7, pady=10)
        self.out1 = scrolledtext.ScrolledText(self, width=50, height=18)
        self.out1.grid(column=1, row=8, pady=10)
        # Column 2
        lbl2 = tk.Label(self, text="RMSD")
        lbl2.grid(column=2, row=4)
        btn2 = tk.Button(self, text="Choose the files", command=self.selectlist2)
        btn2.grid(column=2, row=5, pady=10)
        self.labfile2 = tk.Label(self, text="No file selected")
        self.labfile2.grid(column=2, row=6, pady=10)
        btnfun2 = tk.Button(self, text="Start", command=self.get_rmsd)
        btnfun2.grid(column=2, row=7, pady=10)
        self.out2 = scrolledtext.ScrolledText(self, width=80, height=18)
        self.out2.grid(column=2, row=8, pady=10)
        # Column 3
        lbl3 = tk.Label(self, text="Violations")
        lbl3.grid(column=3, row=4)
        btn3 = tk.Button(self, text="Choose the files", command=self.selectlist3)
        btn3.grid(column=3, row=5, pady=10)
        self.labfile3 = tk.Label(self, text="No file selected")
        self.labfile3.grid(column=3, row=6, pady=10)
        btnfun3 = tk.Button(self, text="Start", command=self.get_violations)
        btnfun3.grid(column=3, row=7, pady=10)
        self.out3 = scrolledtext.ScrolledText(self, width=50, height=18)
        self.out3.grid(column=3, row=8, pady=10, padx=10)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    # TODO: add copy file list button

    def selectlist1(self):
        fullfilelist1 = filedialog.askopenfilenames(initialdir=path.dirname(__file__), filetypes=[("Overview files", ".ovw")])
        self.filelist1 = list(fullfilelist1)
        labeltext = "Selected " + str(len(self.filelist1)) + " files."
        self.labfile1.configure(text=labeltext)

    def selectlist2(self):
        fullfilelist2 = filedialog.askopenfilenames(initialdir=path.dirname(__file__), filetypes=[("Overview files", ".ovw")])
        self.filelist2 = list(fullfilelist2)
        labeltext = "Selected " + str(len(self.filelist2)) + " files."
        self.labfile2.configure(text=labeltext)

    def selectlist3(self):
        fullfilelist3 = filedialog.askopenfilenames(initialdir=path.dirname(__file__), filetypes=[("Overview files", ".ovw")])
        self.filelist3 = list(fullfilelist3)
        labeltext = "Selected " + str(len(self.filelist3)) + " files."
        self.labfile3.configure(text=labeltext)

    def get_tf(self):
        if not self.filelist1:
            messagebox.showerror("Warning", "You did not select any file.")
        pl = PrintLogger(self.out1)
        sys.stdout = pl
        for ele in self.filelist1:
            OVW_Analyze_overview.get_tf(ele)

    def get_rmsd(self):
        if not self.filelist2:
            messagebox.showerror("Warning", "You did not select any file.")
        pl = PrintLogger(self.out2)
        sys.stdout = pl
        for ele in self.filelist2:
            OVW_Analyze_overview.get_rmsd(ele)

    def get_violations(self):
        if not self.filelist3:
            messagebox.showerror("Warning", "You did not select any file.")
        pl = PrintLogger(self.out3)
        sys.stdout = pl
        for ele in self.filelist3:
            OVW_Analyze_overview.get_violations(ele)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(OVW_Analyze_overview)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class OVWAnalyzeViolations(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="OVW: Analyze violations", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the cyana functions.", command=lambda: controller.show_frame("CyanaPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=OVW_Analyze_violations.general_docstring.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        self.df = pd.DataFrame()
        # Column 1
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=4, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=1, row=5, pady=10)
        labtype = tk.Label(self, text="Type:")
        labtype.grid(column=1, row=6, pady=10)
        self.comboT = Combobox(self, width=30)
        self.comboT.grid(column=1, row=7, pady=10)
        labmode = tk.Label(self, text="Mode:")
        labmode.grid(column=1, row=8, pady=10)
        self.comboM = Combobox(self, width=30, values=OVW_Analyze_violations.modes)
        self.comboM.grid(column=1, row=9, pady=10)
        labcolor = tk.Label(self, text="Color:")
        labcolor.grid(column=1, row=10, pady=10)
        self.comboC = Combobox(self, width=30, values=OVW_Analyze_violations.colors)
        self.comboC.grid(column=1, row=11, pady=10)
        btnfun = tk.Button(self, text="Generate macro", command=self.generate_macro)
        btnfun.grid(column=1, row=12, pady=10)
        # Column 2
        self.labinstruction = tk.Label(self, text="")
        self.labinstruction.grid(column=2, row=4, columnspan=2, pady=10)
        self.out = scrolledtext.ScrolledText(self, width=100, height=18, font='Lucida')
        self.out.grid(row=5, column=2, rowspan=50, padx=50)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__))
        self.labfile1.configure(text=os.path.basename(self.file1))
        types, self.df = OVW_Analyze_violations.get_type(self.file1)
        self.comboT['values'] = types

    def generate_macro(self):
        if self.comboT.get() == "":
            messagebox.showerror("Warning", "You did not select any type.")
        elif self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        elif self.comboC.get() == "":
            messagebox.showerror("Warning", "You did not select any color.")
        else:
            self.labinstruction.configure(text="Instruction: open PyMOL, load the .pdb, copy-paste the macro and press enter.")
            pl = PrintLogger(self.out)
            sys.stdout = pl
            self.out.delete('1.0', tk.END)
            OVW_Analyze_violations.macro_violations(self.df, self.comboT.get(), self.comboM.get(), self.comboC.get())

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(OVW_Analyze_violations)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class OVWAnalyzemethylviolationsPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="OVW: Analyze methyl violations", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the cyana functions.", command=lambda: controller.show_frame("CyanaPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=OVW_Analyze_methyl_violations.violations_upl_metprot.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        # Column 1
        lbl1 = tk.Label(self, text="Select the Cyana batch file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5, pady=10)
        lblT = tk.Label(self, text="Violation type:")
        lblT.grid(column=1, row=6, pady=10)
        self.comboT = Combobox(self, width=17, values=["Upper", "VdW"])
        self.comboT.grid(column=2, row=6, pady=10)
        lblA = tk.Label(self, text="Atoms to monitor:")
        lblA.grid(column=1, row=7, pady=10)
        self.comboA = Combobox(self, width=17, values=["HB", "HG", "HD", "HB, HG, HD", "HA, HB, HG, HD, HE, CG, CD", "All methyl protons"])
        self.comboA.grid(column=2, row=7, pady=10)
        lblM = tk.Label(self, text="Mode:")
        lblM.grid(column=1, row=8, pady=10)
        self.comboM = Combobox(self, width=17, values=["single", "double"])
        self.comboM.grid(column=2, row=8, pady=10)
        self.CheckVar1 = tk.IntVar()
        chk1 = tk.Checkbutton(self, text="Inverse", variable=self.CheckVar1, onvalue=1, offvalue=0)
        chk1.grid(column=2, row=9, pady=10)
        btnfun = tk.Button(self, text="Test input", command=self.analyze_methyl, foreground='red')
        btnfun.grid(column=1, row=10, pady=10, columnspan=2)
        # Column 2
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Cyana Overview", ".ovw")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def analyze_methyl(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did input any file.")
        elif self.comboT.get() == "":
            messagebox.showerror("Warning", "You did input any violation type.")
        elif self.comboA.get() == "":
            messagebox.showerror("Warning", "You did input any atoms.")
        elif self.comboM.get() == "":
            messagebox.showerror("Warning", "You did input any mode.")
        else:
            pl = PrintLogger(self.out)
            sys.stdout = pl
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            if self.CheckVar1.get() == 1:
                newname, df = OVW_Analyze_methyl_violations.violations_upl_metprot(self.file1, self.comboT.get(), self.comboA.get(), self.comboM.get(), remaining='on')
            else:
                newname, df = OVW_Analyze_methyl_violations.violations_upl_metprot(self.file1, self.comboT.get(), self.comboA.get(), self.comboM.get())
            stored = "Output stored in : " + str(newname)
            self.lblout.configure(text=stored)
            self.out.insert('insert', df)


    def show_source_code(self):
        # Variable
        loc = inspect.getfile(OVW_Analyze_methyl_violations)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class CYANABatchIterationPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="CYANA: Batch iteration", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the cyana functions.", command=lambda: controller.show_frame("CyanaPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=CYANA_batch_iteration.plus_one_iteration.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        # Column 1
        lbl1 = tk.Label(self, text="Select the Cyana batch file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5, pady=10)
        lblV = tk.Label(self, text="Starting run value:")
        lblV.grid(column=1, row=6, pady=10)
        self.entryV = tk.Entry(self, width=20)
        self.entryV.grid(column=2, row=6, pady=10)
        lblF = tk.Label(self, text="First line of a new run:")
        lblF.grid(column=1, row=7, pady=10)
        self.entryF = tk.Entry(self, width=20)
        self.entryF.grid(column=2, row=7, pady=10)
        lblL = tk.Label(self, text="Log line:")
        lblL.grid(column=1, row=8, pady=10)
        self.entryL = tk.Entry(self, width=20)
        self.entryL.grid(column=2, row=8, pady=10)
        lblO = tk.Label(self, text="Overview line:")
        lblO.grid(column=1, row=9, pady=10)
        self.entryO = tk.Entry(self, width=20)
        self.entryO.grid(column=2, row=9, pady=10)
        # Default variables
        self.entryV.insert('0', 1)
        self.entryF.insert('0', '/home/ubuntu/programs/cyana-3.98.')
        self.entryL.insert('0', 'Zoolander_OVW_1_log.txt')
        self.entryO.insert('0', 'overview Zoolander_OVW_1.ovw structures=10 range=3-238 pdb')
        btnfun = tk.Button(self, text="Perform iteration", command=self.perform_iteration, foreground='red')
        btnfun.grid(column=1, row=10, pady=10, columnspan=2)
        # Column 2
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Bash", ".sh")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def perform_iteration(self):
        if self.entryV.get() == "":
            messagebox.showerror("Warning", "You did input any starting run value.")
        elif self.entryF.get() == "":
            messagebox.showerror("Warning", "You did input any first line of a new run.")
        elif self.entryL.get() == "":
            messagebox.showerror("Warning", "You did input any log line.")
        elif self.entryO.get() == "":
            messagebox.showerror("Warning", "You did input any overview line.")
        elif float(self.entryV.get()).is_integer() == False or int(self.entryV.get()) < 1:
            messagebox.showerror("Warning", "In integer mode insert an integer as subset value (min 1).")
        else:
            newname = CYANA_batch_iteration.plus_one_iteration(self.file1, int(self.entryV.get()), self.entryF.get(), self.entryL.get(), self.entryO.get())
            stored = "Output stored in: " + newname
            self.lblout.configure(text=stored)
            r = open(newname)
            for line in r:
                self.out.insert('insert', line)


    def show_source_code(self):
        # Variable
        loc = inspect.getfile(CYANA_batch_iteration)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class CYANATestinputPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="CYANA: Test input", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the cyana functions.", command=lambda: controller.show_frame("CyanaPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=CYANA_test_input.cyana_test.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        # Column 1
        lbl1 = tk.Label(self, text="Select the Cyana batch file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5, pady=10)
        btnfun = tk.Button(self, text="Test input", command=self.test_input, foreground='red')
        btnfun.grid(column=1, row=6, pady=10, columnspan=2)
        # Column 2
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Bash", ".sh")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def test_input(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did input any file.")
        else:
            newfile, counter = CYANA_test_input.cyana_test(self.file1)
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            stored = "Runs found : " + str(counter)
            self.lblout.configure(text=stored)
            self.out.insert('insert', 'Macro created: %s\n' %newfile)


    def show_source_code(self):
        # Variable
        loc = inspect.getfile(CYANA_test_input)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class UPLSidechainsmanagerPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="UPL: Side chains manager", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the cyana functions.", command=lambda: controller.show_frame("CyanaPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=UPL_Side_chains_manager.general_docstring.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Specific
        self.file1 = ""
        # Column 1
        lbl1 = tk.Label(self, text="Select the .upl file")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectfile1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5, pady=10)
        lblF = tk.Label(self, text="Function:")
        lblF.grid(column=1, row=6, pady=10)
        self.comboF = Combobox(self, width=17, values=["Remove side chains", "Remove inter side chains", "Remove inter side chains (backbone)"])
        self.comboF.grid(column=2, row=6, pady=10)
        btnfun = tk.Button(self, text="Process", command=self.process_upl)
        btnfun.grid(column=1, row=7, pady=10, columnspan=2)
        # Column 2
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectfile1(self):
        self.file1 = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=[("Upper distances", ".upl")])
        self.labfile1.configure(text=os.path.basename(self.file1))

    def process_upl(self):
        if self.file1 == "":
            messagebox.showerror("Warning", "You did input any file.")
        elif self.comboF.get() == "":
            messagebox.showerror("Warning", "You did input any function.")
        else:
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            if self.comboF.get() == "Remove side chains":
                newname, dt = UPL_Side_chains_manager.remove_sidechains(self.file1)
            elif self.comboF.get() == "Remove inter side chains":
                newname, dt = UPL_Side_chains_manager.remove_inter_sidechains(self.file1)
            elif self.comboF.get() == "Remove inter side chains (backbone)":
                newname, dt = UPL_Side_chains_manager.remove_inter_sidechains_with_backbone(self.file1)
            stored = "Output stored in: " + str(newname)
            self.lblout.configure(text=stored)
            self.out.insert('insert', dt)


    def show_source_code(self):
        # Variable
        loc = inspect.getfile(UPL_Side_chains_manager)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class PDBPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="PDB functions.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the main page", command=lambda: controller.show_frame("StartPage"))
        btnback.pack(pady=10)
        btn1 = tk.Button(self, text="Average structures", command=lambda: controller.show_frame("AveragestructuresPage"))
        btn1.pack(pady=10)

class AveragestructuresPage(tk.Frame):

    def __init__(self, parent, controller):
        # General
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Average structures", font=controller.title_font)
        title.grid(column=1, columnspan=5, row=1)
        btnback = tk.Button(self, text="Go back to the PDB functions.", command=lambda: controller.show_frame("PDBPage"))
        btnback.grid(column=1, columnspan=5, pady=10, row=2)
        description = tk.Label(self, text=Average_structures.general_docstring.__doc__)
        description.grid(column=1, columnspan=5, pady=10, row=3)
        # Specific
        self.filelist1 = ""
        # Column 1
        lbl1 = tk.Label(self, text="Select the PDB files")
        lbl1.grid(column=1, row=4, pady=10, columnspan=2)
        btn1 = tk.Button(self, text="Choose the file", command=self.selectlist1)
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=2, row=5, pady=10)
        self.CheckVar1 = tk.IntVar()
        chk1 = tk.Checkbutton(self, text="Only CA", variable=self.CheckVar1, onvalue=1, offvalue=0)
        chk1.grid(column=2, row=6, pady=10)
        btnfun = tk.Button(self, text="Average structures", command=self.average_structures, foreground='red')
        btnfun.grid(column=1, row=7, pady=10, columnspan=2)
        # Column 2
        self.lblout = tk.Label(self, text="")
        self.lblout.grid(column=3, row=4)
        self.out = scrolledtext.ScrolledText(self, width=70, height=18, font='Lucida')
        self.out.grid(column=3, row=5, rowspan=5)
        # Source
        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def selectlist1(self):
        fullfilelist1 = filedialog.askopenfilenames(initialdir=path.dirname(__file__),
                                                    filetypes=[("Protein Database", ".pdb")])
        self.filelist1 = list(fullfilelist1)
        labeltext = "Selected " + str(len(self.filelist1)) + " files."
        self.labfile1.configure(text=labeltext)

    def average_structures(self):
        if self.filelist1 == "":
            messagebox.showerror("Warning", "You did not input any file.")
        elif len(self.filelist1) == 1:
            messagebox.showerror("Warning", "You selected only 1 file.")
        else:
            pl = PrintLogger(self.out)
            sys.stdout = pl
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            test = Average_structures.atom_number_test(self.filelist1)
            if test == False:
                messagebox.showerror("Error", "Your PDB files contain different atoms and/or order.")
            else:
                dx, dy, dz = Average_structures.get_dictionaries(self.filelist1)
                ax = Average_structures.average_dict_values(dx)
                ay = Average_structures.average_dict_values(dy)
                az = Average_structures.average_dict_values(dz)
                if self.CheckVar1.get() == 1:
                    newname, ppdb = Average_structures.map_dataframe(self.filelist1[0], ax, ay, az, remove_non_ca=1)
                else:
                    newname, ppdb = Average_structures.map_dataframe(self.filelist1[0], ax, ay, az, remove_non_ca=0)
                stored = "Output stored in : " + str(newname)
                self.lblout.configure(text=stored)
                r = open(newname, 'r')
                for line in r:
                    self.out.insert('insert', line)

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Average_structures)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class WebScrapingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Web scraping functions.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the main page", command=lambda: controller.show_frame("StartPage"))
        btnback.pack(pady=10)
        btn1 = tk.Button(self, text="Journal Club", command=lambda: controller.show_frame("JournalClub"))
        btn1.pack(pady=10)
        btn2 = tk.Button(self, text="Journal Club Special", command=lambda: controller.show_frame("JournalClubSpecial"))
        btn2.pack(pady=10)

class JournalClubPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Journal Club", font=controller.title_font)
        title.grid(column=1, columnspan=5)
        btnback = tk.Button(self, text="Go back to the web scraping functions.", command=lambda: controller.show_frame("WebScrapingPage"))
        btnback.grid(column=1, columnspan=5, pady=10)
        description = tk.Label(self, text=Journal_club.general_docstring.__doc__, justify='left')
        description.grid(column=1, columnspan=5, pady=10)

        lblcomboM = tk.Label(self, text="Select the mode:")
        lblcomboM.grid(column=1, row=4, padx=10)
        self.comboM = Combobox(self, width=30, values=Journal_club.modes)
        self.comboM.bind('<<ComboboxSelected>>', self.mode_action)
        self.comboM.grid(column=1, row=5, padx=10)

        lblcomboJ = tk.Label(self, text="Select the journal:")
        lblcomboJ.grid(column=1, row=6, padx=10)
        self.comboJ = Combobox(self, values=Journal_club.journals, width=30)
        self.comboJ.bind('<<ComboboxSelected>>', self.get_journal)
        self.comboJ.grid(column=1, row=7, padx=10)

        lblcomboV = tk.Label(self, text="Select the volume:")
        lblcomboV.grid(column=1, row=8, padx=10)
        self.comboV = Combobox(self, width=30)
        self.comboV.bind('<<ComboboxSelected>>', self.get_issue)
        self.comboV.grid(column=1, row=9, padx=10)

        lblcomboI = tk.Label(self, text="Select the issue:")
        lblcomboI.grid(column=1, row=10, padx=10)
        self.comboI = Combobox(self, width=30)
        self.comboI.bind('<<ComboboxSelected>>', self.get_articles)
        self.comboI.grid(column=1, row=11, padx=10)

        btnM = tk.Button(self, text="Mode Info", command=self.show_keywords, foreground='red')
        btnM.grid(column=1, row=12, padx=10, pady=10)

        self.lblout = tk.Label(self, text="")
        self.lblout.grid(row=4, column=2, padx=50, sticky='w')
        self.out = scrolledtext.ScrolledText(self, width=100, height=15, font='Lucida')
        self.out.grid(row=5, column=2, rowspan=50, padx=50)
        self.out.tag_config('link', foreground='blue')
        self.out.tag_configure("keyword", foreground="#b22222")

        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def mode_action(self, event):
        if self.comboM.get() == "Custom":
            def okay():
                """Clears the Journal_club.custom list, store the Entry() widget text in that list (comma separated) and closes the popup window"""
                eget = e.get().split(", ")
                Journal_club.custom.clear()
                for ele in eget:
                    Journal_club.custom.append(ele)
                win.destroy()
            win = tk.Toplevel()
            win.attributes('-topmost', 1)
            win.wm_title("Custom Keywords")
            # Label
            l = tk.Label(win, text="Insert your keywords separated by a comma.")
            l.grid(row=0, column=0)
            # Entry
            e = tk.Entry(win)
            e.grid(row=1, column=0)
            # Button
            b = tk.Button(win, text="Okay", command=okay)
            b.grid(row=2, column=0)
        elif self.comboM.get() == "Impact Factors":
            # block user from doing the wrong thing
            self.comboJ['state'] = 'disabled'
            self.comboV['state'] = 'disabled'
            self.comboI['state'] = 'disabled'
            # loop to list impact factors
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            for journal, factor in sorted(Journal_club.impact_factor_dictionary.items(), key=lambda p: p[1], reverse=True):
                self.out.insert('insert', str(journal) + " - " + str(factor) + "\n")
        else:
            self.comboJ['state'] = 'enabled'
            self.comboV['state'] = 'enabled'
            self.comboI['state'] = 'enabled'

    def show_keywords(self):
        if self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        elif self.comboM.get() == "All":
            messagebox.showinfo("All", "List all articles.")
        elif self.comboM.get() == "Impact Factors":
            messagebox.showinfo("Impact Factors", "List in descending order the impact factors.")
        else:
            mode = self.comboM.get()
            keywords = Journal_club.modes_dictionary[mode]
            messagebox.showinfo(mode, ", ".join(keywords))

    def get_journal(self, event):
        self.comboV.set('')
        self.comboV['state'] = "enabled"
        self.comboI.set('')
        self.comboI['state'] = "enabled"
        if self.comboJ.get() == "Nature":
            volumes = Journal_club.get_volumes_nature(Journal_club.volumes_url["Nature"])
            self.comboV['state'] = "enabled"
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Nature Biotechnology":
            volumes = Journal_club.get_volumes_nature_biotechnology(Journal_club.volumes_url["Nature Biotechnology"])
            self.comboV['state'] = "enabled"
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Nature Methods":
            volumes = Journal_club.get_volumes_nature_methods(Journal_club.volumes_url["Nature Methods"])
            self.comboV['state'] = "enabled"
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Nature Protocols":
            volumes = Journal_club.get_volumes_nature_protocols(Journal_club.volumes_url["Nature Protocols"])
            self.comboV['state'] = "enabled"
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Nature Reviews Drug Discovery":
            volumes = Journal_club.get_volumes_nature_nrd(Journal_club.volumes_url["Nature Reviews Drug Discovery"])
            self.comboV['state'] = "enabled"
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Nature Structural and Molecular Biology":
            volumes = Journal_club.get_volumes_nature_nsmb(Journal_club.volumes_url["Nature Structural and Molecular Biology"])
            self.comboV['state'] = "enabled"
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Biophysical Journal":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_biophysj(Journal_club.volumes_url["Biophysical Journal"])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Proteins":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_proteins(Journal_club.volumes_url["Proteins"])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "EMBO":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_EMBO(Journal_club.volumes_url["EMBO"])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Cell":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_cell(Journal_club.volumes_url["Cell"])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Cell - Structure":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_cell_structure(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Journal of Magnetic Resonance":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_jmr(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "BBA - biomembranes":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_bba_biomembranes(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == 'Protein expression and purification':
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_peap(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == 'Current opinion in structural biology':
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_cosb(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == 'Current opinion in chemical biology':
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_cocb(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == 'Chemistry & biology':
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_chemistry_and_biology(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == 'Journal of molecular biology':
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_jmb(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == 'Methods in enzymology':
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_methods_enzymology(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == 'Progress in NMR spectroscopy':
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_progress_nmr(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Angewandte":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_angewandte(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "FEBS letters":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_febs_letters(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Biopolymers":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_biopolymers(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Annual Reviews of Biochemistry":
            self.comboV['state'] = "enabled"
            volumes = Journal_club.get_volumes_arb(Journal_club.volumes_url["Annual Reviews of Biochemistry"])
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Annual Reviews of Biophysics":
            self.comboV['state'] = "enabled"
            volumes = Journal_club.get_volumes_arbf(Journal_club.volumes_url["Annual Reviews of Biophysics"])
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Journal of Biomolecular NMR":
            self.comboV['state'] = "disabled"
            volumes = Journal_club.get_issues_jbnmr(Journal_club.volumes_url["Journal of Biomolecular NMR"])
            self.comboI['values'] = volumes
        elif self.comboJ.get() == "Protein Science":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_protein_science(Journal_club.volumes_url["Protein Science"])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "ACS - Biochemistry":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_acs_biochemistry(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "ACS - Chemical Biology":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_acs_chemicalbiology(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "ACS - Chemical Reviews":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_acs_chemicalreviews(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "ACS - Journal of Medicinal Chemistry":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_acs_medicinalchemistry(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Journal of the American Chemical Society (JACS)":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_jacs(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Journal of Biological Chemistry":
            volumes = Journal_club.get_volumes_jbc(Journal_club.volumes_url[self.comboJ.get()])
            self.comboV['state'] = "enabled"
            self.comboV['values'] = volumes
        elif self.comboJ.get() == "Trends in Pharmacological Sciences":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_tips(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Trends in Biochemical Sciences":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_tibs(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Trends in Biotechnology":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_trends_biotechnology(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Molecular Cell":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_molecular_cell(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "PNAS":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_pnas(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Science (AAAS)":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_science(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Science Advances":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_science_advances(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Science Immunology":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_science_immunology(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Science Robotics":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_science_robotics(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Science Signaling":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_science_signaling(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Science Translational Medicine":
            self.comboV['state'] = "disabled"
            issues = Journal_club.get_issues_science_translational_medicine(Journal_club.volumes_url[self.comboJ.get()])
            self.comboI['values'] = issues

    def get_issue(self, event):
        self.comboI.set('')
        self.comboI['state'] = "enabled"
        if self.comboJ.get() == "Nature":
            volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
            issues = Journal_club.get_issue_nature(volume_link)
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Nature Biotechnology":
            volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
            issues = Journal_club.get_issue_nature_biotechnology(volume_link)
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Nature Methods":
            volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
            issues = Journal_club.get_issue_nature_methods(volume_link)
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Nature Protocols":
            volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
            issues = Journal_club.get_issue_nature_protocols(volume_link)
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Nature Reviews Drug Discovery":
            volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
            issues = Journal_club.get_issue_nature_nrd(volume_link)
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Nature Structural and Molecular Biology":
            volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
            issues = Journal_club.get_issue_nature_nsmb(volume_link)
            self.comboI['values'] = issues
        elif self.comboJ.get() == "Annual Reviews of Biochemistry":
            self.comboI['state'] = "disabled"
            self.get_articles("event")
        elif self.comboJ.get() == "Annual Reviews of Biophysics":
            self.comboI['state'] = "disabled"
            self.get_articles("event")
        elif self.comboJ.get() == "Journal of Biological Chemistry":
            volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
            issues = Journal_club.get_issues_jbc(volume_link)
            self.comboI['values'] = issues

    def get_articles(self, event):
        global issue_link
        if self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        else:
            if self.comboI.get() == "":
                pass
            else:
                issue_link = Journal_club.issues_dictionary[self.comboI.get()]
            if self.comboJ.get() == "Nature":
                articles = Journal_club.nature(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Biophysical Journal":
                articles = Journal_club.biophysj(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Proteins":
                articles = Journal_club.proteins_(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "EMBO":
                articles = Journal_club.EMBO(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Cell":
                articles = Journal_club.cell_(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Cell - Structure":
                articles = Journal_club.cell_structure(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Angewandte":
                articles = Journal_club.angewandte(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Biopolymers":
                articles = Journal_club.biopolymers(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "FEBS letters":
                articles = Journal_club.febs_letters(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Protein Science":
                articles = Journal_club.protein_science(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Nature Methods":
                articles = Journal_club.nature_methods(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Nature Protocols":
                articles = Journal_club.nature_protocols(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Nature Biotechnology":
                articles = Journal_club.nature_biotechnology(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Nature Reviews Drug Discovery":
                articles = Journal_club.nature_nrd(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Nature Structural and Molecular Biology":
                articles = Journal_club.nature_nsmb(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Annual Reviews of Biochemistry":
                volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
                articles = Journal_club.arb(volume_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Annual Reviews of Biophysics":
                volume_link = Journal_club.volumes_dictionary[self.comboV.get()]
                articles = Journal_club.arbf(volume_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Journal of Biomolecular NMR":
                articles = Journal_club.jbnmr(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "ACS - Biochemistry":
                articles = Journal_club.acs_biochemistry(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "ACS - Chemical Biology":
                articles = Journal_club.acs_chemicalbiology(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Journal of Magnetic Resonance":
                articles = Journal_club.jmr(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == 'BBA - biomembranes':
                articles = Journal_club.bba_biomembranes(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == 'Protein expression and purification':
                articles = Journal_club.peap(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == 'Current opinion in structural biology':
                articles = Journal_club.cosb(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == 'Current opinion in chemical biology':
                articles = Journal_club.cocb(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == 'Chemistry & biology':
                articles = Journal_club.chemistry_and_biology(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == 'Journal of molecular biology':
                articles = Journal_club.jmb(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == 'Methods in enzymology':
                articles = Journal_club.methods_enzymology(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Progress in NMR spectroscopy":
                articles = Journal_club.progress_nmr(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "ACS - Chemical Reviews":
                articles = Journal_club.acs_chemicalreviews(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "ACS - Journal of Medicinal Chemistry":
                articles = Journal_club.acs_medicinalchemistry(issue_link,
                                                            Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Journal of the American Chemical Society (JACS)":
                articles = Journal_club.jacs(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Journal of Biological Chemistry":
                articles = Journal_club.jbc(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Trends in Pharmacological Sciences":
                articles = Journal_club.tips(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Trends in Biochemical Sciences":
                articles = Journal_club.tibs(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Trends in Biotechnology":
                articles = Journal_club.trends_biotechnology(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Molecular Cell":
                articles = Journal_club.molecular_cell(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "PNAS":
                articles = Journal_club.pnas(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Science (AAAS)":
                articles = Journal_club.science_(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Science Advances":
                articles = Journal_club.science_advances(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Science Immunology":
                articles = Journal_club.science_immunology(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Science Robotics":
                articles = Journal_club.science_robotics(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Science Signaling":
                articles = Journal_club.science_signaling(issue_link, Journal_club.modes_dictionary[self.comboM.get()])
            elif self.comboJ.get() == "Science Translational Medicine":
                articles = Journal_club.science_translational_medicine(issue_link, Journal_club.modes_dictionary[self.comboM.get()])

            total = "Total articles found: " + str(round(len(articles)/2)) + "\n"
            self.lblout.configure(text=total)
            self.out.delete('1.0', tk.END)
            for line in articles:
                if "http" in line:
                    self.out.insert('insert', line+"\n\n", 'link')
                else:
                    self.out.insert('insert', line + "\n", 'name')
                    # cool loop to highlight triggering keywords
                    if self.comboM.get() != "All":
                        for word in line.split():
                            matches = [x for x in Journal_club.modes_dictionary[self.comboM.get()] if x in word]
                            self.out.mark_set("matchStart", "1.0")
                            self.out.mark_set("matchEnd", "1.0")
                            count = tk.IntVar()
                            for x in matches:
                                while True:
                                    index = self.out.search(x, "matchEnd", "end", count=count)
                                    if index == "":
                                        break  # no match was found
                                    self.out.mark_set("matchStart", index)
                                    self.out.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                                    self.out.tag_add("keyword", "matchStart", "matchEnd")

    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Journal_club)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()

class JournalClubSpecialPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Journal Club Special", font=controller.title_font)
        title.grid(column=1, columnspan=5)
        btnback = tk.Button(self, text="Go back to the web scraping functions.", command=lambda: controller.show_frame("WebScrapingPage"))
        btnback.grid(column=1, columnspan=5, pady=10)
        description = tk.Label(self, text=Journal_club_special.general_docstring.__doc__, justify='left')
        description.grid(column=1, columnspan=5, pady=10)

        lblcomboM = tk.Label(self, text="Select the mode:")
        lblcomboM.grid(column=1, row=4, padx=10)
        self.comboM = Combobox(self, width=30, values=Journal_club_special.modes)
        self.comboM.bind('<<ComboboxSelected>>', self.mode_action)
        self.comboM.grid(column=1, row=5, padx=10)

        lblcomboT = tk.Label(self, text="Select the time range:")
        lblcomboT.grid(column=1, row=6, padx=10)
        self.comboT = Combobox(self, width=30, values=Journal_club_special.Time_range_list)
        self.comboT.grid(column=1, row=7, padx=10)

        lblcomboJ = tk.Label(self, text="Select the journal:")
        lblcomboJ.grid(column=1, row=8, padx=10)
        self.comboJ = Combobox(self, values=Journal_club_special.journals, width=30)
        self.comboJ.bind('<<ComboboxSelected>>', self.start_search)
        self.comboJ.grid(column=1, row=9, padx=10)

        btnM = tk.Button(self, text="Mode Info", command=self.show_keywords, foreground='red')
        btnM.grid(column=1, row=10, padx=10, pady=10)

        self.lblout = tk.Label(self, text="")
        self.lblout.grid(row=4, column=2, columnspan=2, padx=50, sticky='w')
        self.out = scrolledtext.ScrolledText(self, width=100, height=14, font='Lucida')
        self.out.grid(row=5, column=2, rowspan=50, columnspan=2, padx=50)
        self.out.tag_config('link', foreground='blue')
        self.out.tag_configure("keyword", foreground="#b22222")
        self.lblout2 = tk.Label(self, text="")
        self.lblout2.grid(row=56, column=2, padx=50, pady=10, sticky='w')
        self.btnout2 = tk.Button(self, text="Copy URL", command=self.copy_url, foreground='red')

        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

    def mode_action(self, event):
        if self.comboM.get() == "Custom":
            def okay():
                """Clears the Journal_club_special.custom list, store the Entry() widget text in that list (comma separated) and closes the popup window"""
                eget = e.get().split(", ")
                Journal_club_special.custom.clear()
                for ele in eget:
                    Journal_club_special.custom.append(ele)
                win.destroy()
            win = tk.Toplevel()
            win.attributes('-topmost', 1)
            win.wm_title("Custom Keywords")
            # Label
            l = tk.Label(win, text="Insert your keywords separated by a comma.")
            l.grid(row=0, column=0)
            # Entry
            e = tk.Entry(win)
            e.grid(row=1, column=0)
            # Button
            b = tk.Button(win, text="Okay", command=okay)
            b.grid(row=2, column=0)
        elif self.comboM.get() == "Impact Factors":
            # loop to list impact factors
            self.out.delete('1.0', tk.END)
            self.lblout.configure(text="")
            for journal, factor in sorted(Journal_club_special.impact_factor_dictionary.items(), key=lambda p: p[1], reverse=True):
                self.out.insert('insert', str(journal) + " - " + str(factor) + "\n")
        else:
            self.comboJ['state'] = 'enabled'

    def show_keywords(self):
        if self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        elif self.comboM.get() == "Impact Factors":
            messagebox.showinfo("Impact Factors", "List in descending order the impact factors.")
        else:
            mode = self.comboM.get()
            keywords = Journal_club_special.modes_dictionary[mode]
            messagebox.showinfo(mode, ", ".join(keywords))

    def start_search(self, event):
        if self.comboM.get() == "":
            messagebox.showerror("Warning", "You did not select any mode.")
        elif self.comboT.get() == "":
            messagebox.showerror("Warning", "You did not select any time range.")
        else:
            url = Journal_club_special.construct_url(Journal_club_special.Journals_dictionary[self.comboJ.get()], Journal_club_special.modes_dictionary[self.comboM.get()], self.comboT.get())
            articles = Journal_club_special.get_article(url)
            total = "Total articles found: " + str(round(len(articles) / 2)) + "\n"
            self.lblout.configure(text=total)
            self.out.delete('1.0', tk.END)
            for line in articles:
                if "http" in line:
                    self.out.insert('insert', line + "\n\n", 'link')
                else:
                    self.out.insert('insert', line + "\n", 'name')
                    # cool loop to highlight triggering keywords
                    if self.comboM.get() != "All":
                        for word in line.split():
                            matches = [x for x in Journal_club.modes_dictionary[self.comboM.get()] if x in word]
                            self.out.mark_set("matchStart", "1.0")
                            self.out.mark_set("matchEnd", "1.0")
                            count = tk.IntVar()
                            for x in matches:
                                while True:
                                    index = self.out.search(x, "matchEnd", "end", count=count)
                                    if index == "":
                                        break  # no match was found
                                    self.out.mark_set("matchStart", index)
                                    self.out.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                                    self.out.tag_add("keyword", "matchStart", "matchEnd")
            # Check for the 20 results per page limit
            limit = Journal_club_special.get_limit(url)
            if limit >= 20:
                self.lblout2.configure(text='WARNING: 20 articles per page limit reached. Copy-paste the URL in a browser to visualize the full list.', foreground='DarkOrange1')
                self.btnout2.grid(column=3, row=56, pady=10, padx=50)
            else:
                self.lblout2.configure(text='')
                self.btnout2.grid_forget()
                self.btnout2.configure(text="Copy URL")

    def copy_url(self):
        url = Journal_club_special.construct_url(Journal_club_special.Journals_dictionary[self.comboJ.get()], Journal_club_special.modes_dictionary[self.comboM.get()], self.comboT.get())
        pyperclip.copy(url)
        self.btnout2.configure(text="Copied!")


    def show_source_code(self):
        # Variable
        loc = inspect.getfile(Journal_club_special)
        # Window
        win = tk.Toplevel()
        win.attributes('-topmost', 1)
        win.wm_title("Source Code")
        # Scrolled Text
        t = scrolledtext.ScrolledText(win, width=200, height=36)
        t.tag_config('import', foreground='dark orange')
        t.tag_config('def', foreground='dark goldenrod')
        t.tag_config('comment', foreground='gray40')
        t.tag_config('rest', foreground='black')
        t.tag_config('flow_control', foreground='DarkOrange2')
        t.tag_config('docstring', foreground='sea green')
        t.tag_config('print', foreground='deep sky blue')
        # Get Source Code
        rloc = open(loc, 'r')
        for line in rloc:
            if "import" in str(line)[:6]:
                t.insert('insert', line, 'import')
            elif "from" in str(line)[:4]:
                t.insert('insert', line, 'import')
            elif "def" in str(line)[:3]:
                t.insert('insert', line, 'def')
            elif "#" in str(line):
                t.insert('insert', line, 'comment')
            elif '"""' in str(line):
                t.insert('insert', line, 'docstring')
            elif "if" in str(line).strip()[:2] or "for" in str(line).strip()[:3] or "return" in str(line).strip()[:6]:
                t.insert('insert', line, 'flow_control')
            elif "print(" in str(line):
                t.insert('insert', line, 'print')
            else:
                t.insert('insert', line, 'rest')
        t.pack()



# Start
if __name__ == "__main__":
    start = App()
    start.mainloop()


#TODO: implement all premade functions

#TODO: IDEAS
#       1-logo Asimov
#       2-lunch conversation topic generator (BBC mixing)

