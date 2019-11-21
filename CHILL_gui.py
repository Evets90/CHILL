# general import
import sys
import pandas as pd
import tkinter as tk
import inspect
import os
from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import PhotoImage
from tkinter.ttk import Combobox
from os import path
from pathlib import Path
from PIL import Image, ImageTk

# specific functions import
import Compare_files
import Clean_spaces
import Check_series
import Journal_club
import OVW_Analyze_overview

# version
version = "Version: 0.017"

# logos paths
logoSaS = Path.cwd() / "Logos/SaS.gif"
logochill = Path.cwd() / "Logos/Chill.png"

# print logger used for redirect the print() in python to a window in tkinter
class PrintLogger():
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert(tk.END, text)

    def flush(self):
        pass

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
        self.frames["CyanaPage"] = CyanaPage(parent=container, controller=self)
        self.frames["CompareFiles"] = CompareFilesPage(parent=container, controller=self)
        self.frames["CleanSpaces"] = CleanSpacesPage(parent=container, controller=self)
        self.frames["CheckSeries"] = CheckSeriesPage(parent=container, controller=self)
        self.frames["OVWAnalyzeOverview"] = OVWAnalyzeOverview(parent=container, controller=self)
        self.frames["WebScrapingPage"] = WebScrapingPage(parent=container, controller=self)
        self.frames["JournalClub"] = JournalClubPage(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["BasicPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["PCSPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["CyanaPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["CompareFiles"].grid(row=0, column=0, sticky="nsew")
        self.frames["CleanSpaces"].grid(row=0, column=0, sticky="nsew")
        self.frames["CheckSeries"].grid(row=0, column=0, sticky="nsew")
        self.frames["OVWAnalyzeOverview"].grid(row=0, column=0, sticky="nsew")
        self.frames["WebScrapingPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["JournalClub"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # logos
        zoom = 0.2
        image = Image.open(logoSaS)
        image2 = Image.open(logochill)
        pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])
        img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
        img2 = ImageTk.PhotoImage(image2.resize((300, 600)))
        logo1 = tk.Label(self, image=img, anchor='nw')
        logo1.image = img
        #logo1.pack(side="top", fill='x')
        logo2 = tk.Label(self, image=img2)
        logo2.image = img2
        logo2.pack(side="left", fill='both')

        # title
        label = tk.Label(self, text="Please select a category", font=controller.title_font)
        label.pack(side='top', fill='x', pady=10)

        # version
        global version
        labversion = tk.Label(self, text=version, anchor='se')
        labversion.pack(side='bottom', fill='both')

        # buttons
        btn1 = tk.Button(self, text="Basic", command=lambda: controller.show_frame("BasicPage"))
        btn2 = tk.Button(self, text="PCS", command=lambda: controller.show_frame("PCSPage"))
        btn3 = tk.Button(self, text="Cyana", command=lambda: controller.show_frame("CyanaPage"))
        #btn4 = tk.Button(self, text="Chemical shifts", command=lambda: controller.show_frame("PCSPage"))
        #btn5 = tk.Button(self, text="Cyana", command=lambda: controller.show_frame("PCSPage"))
        btn6 = tk.Button(self, text="Web Scraping", command=lambda: controller.show_frame("WebScrapingPage"))

        btn1.pack(pady=10)
        btn2.pack(pady=10)
        btn3.pack(pady=10)
        btn6.pack(pady=10)
        #btn4.pack()
        #btn5.pack()

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
        btnback.pack()

class CyanaPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Cyana functions.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the main page", command=lambda: controller.show_frame("StartPage"))
        btn1 = tk.Button(self, text="OVW: Analyze overview", command=lambda: controller.show_frame("OVWAnalyzeOverview"))
        btnback.pack()
        btn1.pack(pady=10)

class OVWAnalyzeOverview(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename1 = ""
        self.filename2 = ""
        title = tk.Label(self, text="OVW: Analyze overview", font=controller.title_font)
        title.grid(column=1, columnspan=3, row=1)
        btnback = tk.Button(self, text="Go back to the cyana functions.", command=lambda: controller.show_frame("CyanaPage"))
        btnback.grid(column=1, columnspan=3, pady=10, row=2)
        description = tk.Label(self, text=OVW_Analyze_overview.general_docstring.__doc__)
        description.grid(column=1, columnspan=3, pady=10, row=3)
        # Column 1
        lbl1 = tk.Label(self, text="Target Function")
        lbl1.grid(column=1, row=4)
        btn1 = tk.Button(self, text="Choose the files")
        btn1.grid(column=1, row=5, pady=10)
        self.labfile1 = tk.Label(self, text="No file selected")
        self.labfile1.grid(column=1, row=6, pady=10)
        btnfun1 = tk.Button(self, text="Start")
        btnfun1.grid(column=1, row=7, pady=10)
        self.out1 = scrolledtext.ScrolledText(self, width=50, height=18)
        self.out1.grid(column=1, row=8, pady=10)
        # Column 2
        lbl2 = tk.Label(self, text="RMSD")
        lbl2.grid(column=2, row=4)
        btn2 = tk.Button(self, text="Choose the files")
        btn2.grid(column=2, row=5, pady=10)
        self.labfile2 = tk.Label(self, text="No file selected")
        self.labfile2.grid(column=2, row=6, pady=10)
        btnfun2 = tk.Button(self, text="Start")
        btnfun2.grid(column=2, row=7, pady=10)
        self.out2 = scrolledtext.ScrolledText(self, width=50, height=18)
        self.out2.grid(column=2, row=8, pady=10)
        # Column 3
        lbl3 = tk.Label(self, text="Violations")
        lbl3.grid(column=3, row=4)
        btn3 = tk.Button(self, text="Choose the files")
        btn3.grid(column=3, row=5, pady=10)
        self.labfile3 = tk.Label(self, text="No file selected")
        self.labfile3.grid(column=3, row=6, pady=10)
        btnfun3 = tk.Button(self, text="Start")
        btnfun3.grid(column=3, row=7, pady=10)
        self.out3 = scrolledtext.ScrolledText(self, width=50, height=18)
        self.out3.grid(column=3, row=8, pady=10, padx=10)


        btnsource = tk.Button(self, text="Page Source Code", command=self.show_source_code)
        btnsource.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

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

class WebScrapingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Web scraping functions.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btnback = tk.Button(self, text="Go back to the main page", command=lambda: controller.show_frame("StartPage"))
        btn1 = tk.Button(self, text="Journal Club", command=lambda: controller.show_frame("JournalClub"))
        btnback.pack()
        btn1.pack()

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
        self.out = scrolledtext.ScrolledText(self, width=100, height=18, font='Lucida')
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




# start
if __name__ == "__main__":
    start = App()
    start.mainloop()


#TODO: add test_files
#TODO: implement the super cool terminal (new look + modify subfunctions)
#TODO: implement all premade functions

#TODO: IDEAS
#       1-logo Asimov
