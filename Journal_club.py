import requests
import re
import urllib.request
import time
from bs4 import BeautifulSoup

def general_docstring():
    """This page is to perform a quick scan of some scientific journals to get a sub-list based on a certain keyword in the title. You need to select a mode, then a journal, volume and issue.

    MODES
    Standard: standard set of keywords obtained from analysis of internal journal clubs.
                Best suited for: standard search
    Loose: search of non specific words such as "protein" or "amino acid".
                Best suited for: search in a journal outside of the structural biology field.
    All: list all the articles in the selected issue.
                Best suited for: completionists?
    Funny: search for funny articles.
                Best suited for: it's 11 pm and I am still in the office.

    For more info, select a mode and click on the "Mode Info" button.

    """
    # just to a have a general docstring
    pass


# keywords lists
journals = ['Nature', 'Biophysical Journal', 'Proteins', "EMBO", "Cell", "Angewandte", "Nature Methods", "Nature Protocols", "Nature Biotechnology", "Nature Structural and Molecular Biology", "Nature Reviews Drug Discovery"]
modes = ['Standard', 'Loose', 'All', 'Funny']
standard = ['Membranes', 'Sleep', 'protein']
loose = ['protein', 'response']
funny = ['Marvel', 'Thanos', 'Batman', 'fun', 'joke']

# dictionaries
volumes_url = {"Nature": "https://www.nature.com/nature/volumes", "Biophysical Journal": "https://www.cell.com/biophysj/archive", "Proteins": "https://onlinelibrary.wiley.com/loi/10970134", "EMBO": "https://www.embopress.org/loi/14602075", "Cell": "https://www.cell.com/cell/archive", "Angewandte": "https://onlinelibrary.wiley.com/loi/15213773", "Nature Methods" : "https://www.nature.com/nmeth/volumes", "Nature Protocols": "https://www.nature.com/nprot/volumes", "Nature Biotechnology": "https://www.nature.com/nbt/volumes", "Nature Structural and Molecular Biology": "https://www.nature.com/nsmb/volumes", "Nature Reviews Drug Discovery": "https://www.nature.com/nrd/volumes"}
modes_dictionary = {"Standard": standard, "Loose": loose, "Funny": funny, "All": "all"}
volumes_dictionary = {}
issues_dictionary = {}

# selection regular expressions
regex_angewandte_issue_title = "href=\"(.*?)\">(.*?)</a>"
regex_angewandte_issue_link = "href=\"(.*?)\""
regex_angewandte_article_title = "h2>(.*?)\s*</h2"
regex_angewandte_article_link = "href=\"(.*?)\""

regex_biophysj_issue_title = ">(.*?)<"
regex_biophysj_issue_link = "=\"/(.*?)\">"
regex_biophysj_article_title = ">(.*?)<"
regex_biophysj_article_link = "=\"(.*?)\">"

regex_cell_issue_title = "<strong> (.*?) </strong> (.*?)</a>"
regex_cell_issue_link = "href=\"(.*?)\">"
regex_cell_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_cell_article_link = "href=\"(.*?)\">"

regex_EMBO_issue_title = "\">(.*?)<"
regex_EMBO_issue_link = "href=\"(.*?)\""
regex_EMBO_article_title = "h5>(.*?)\s*</h5"
regex_EMBO_article_link = "href=\"(.*?)\">"

regex_proteins_issue_title = "\">(.*?)<"
regex_proteins_issue_link = "href=\"(.*?)\""
regex_proteins_article_title = "2>(.*?)</"
regex_proteins_article_link = "href=\"(.*?)\">"


regex_nature_volumes_numbers = ">(.*?)<"
regex_nature_volumes_link = "href=\"(.*?)\">"
regex_nature_issues_numbers = ">(.*?)<"
regex_nature_issues_link = "href=\"(.*?)\">"
regex_nature_article_title = "(.*?)<"
regex_nature_article_link = "href=\"(.*?)\""

regex_nature_methods_volumes_title = ">(.*?)<"
regex_nature_methods_volumes_link = "href=\"(.*?)\">"
regex_nature_methods_issues_title = "\">(.*?)<"
regex_nature_methods_issues_link = "href=\"(.*?)\">"
regex_nature_methods_article_title = ">\s*(.*?)\s*<"
regex_nature_methods_article_link = "href=\"(.*?)\""

# sorts
journals.sort()
modes.sort()
standard.sort()
loose.sort()
funny.sort()

def get_issues_angewandte(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h4", class_="parent-item")
    selected = []
    for ele in mydivs:
        title = "".join(list(zip(re.findall(regex_angewandte_issue_title, str(ele))[0]))[1])
        link = "https://onlinelibrary.wiley.com" + re.findall(regex_angewandte_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def angewandte(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issue-item__title visitable")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_angewandte_article_title, str(ele))[0]
            link = "https://onlinelibrary.wiley.com" + re.findall(regex_angewandte_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_angewandte_article_title, str(ele))[0]
            link = "https://onlinelibrary.wiley.com" + re.findall(regex_angewandte_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_biophysj(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issueLinkCon")
    selected = []
    reconstructed = []
    # reconstruction loop
    for element in mydivs:
        title_split = re.findall(regex_biophysj_issue_title, str(element))
        title = title_split[1] + "-" + title_split[2]
        title = title.strip()
        link = re.findall(regex_biophysj_issue_link, str(element))[0]
        line = title + " (http://www.cell.com/" + link + ")"
        selected.append(line)
        reconstructed.append(title)
        issues_dictionary[title] = "http://www.cell.com/" + link
    return reconstructed
def biophysj(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for h3 elements with the correct class
    mydivs = soup.findAll("h3", class_="toc__item__title")
    print(f"Total articles found: {len(mydivs)}")
    selected = []
    # selection loop
    for x in mydivs:
        if mode == "all":
            title = re.findall(regex_biophysj_article_title, str(x))[1]
            link = re.findall(regex_biophysj_article_link, str(x))[1]
            linkfull = "www.cell.com" + link
            selected.append(title)
            selected.append(linkfull)
        elif any(a in str(x) for a in mode):
            title = re.findall(regex_biophysj_article_title, str(x))[1]
            link = re.findall(regex_biophysj_article_link, str(x))[1]
            linkfull = "www.cell.com" + link
            selected.append(title)
            selected.append(linkfull)
    return selected

def get_issues_cell(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issueLinkCon")
    selected = []
    for ele in mydivs:
        title = " - ".join(re.findall(regex_cell_issue_title, str(ele))[0])
        link = "https://www.cell.com" + re.findall(regex_cell_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def cell_(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h3", class_="toc__item__title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_cell_article_title, str(ele))[0]))[1])
            link = "https://www.embopress.org" + re.findall(regex_cell_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_cell_article_title, str(ele))[0]))[1])
            link = "https://www.embopress.org" + re.findall(regex_cell_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_EMBO(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("div", class_="parent-item")
    selected = []
    for ele in mydivs:
        title = re.findall(regex_EMBO_issue_title, str(ele))[-1]
        link = "https://www.embopress.org" + re.findall(regex_EMBO_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def EMBO(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issue-item__title visitable")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_EMBO_article_title, str(ele))[0]
            link = "https://www.embopress.org" + re.findall(regex_EMBO_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_EMBO_article_title, str(ele))[0]
            link = "https://www.embopress.org" + re.findall(regex_EMBO_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_proteins(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h4")
    selected = []
    for ele in mydivs:
        title = re.findall(regex_proteins_issue_title, str(ele))[1]
        link = "https://onlinelibrary.wiley.com" + re.findall(regex_proteins_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def proteins_(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issue-item__title visitable")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_proteins_article_title, str(ele))[0]
            link = "https://onlinelibrary.wiley.com" + re.findall(regex_proteins_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_proteins_article_title, str(ele))[0]
            link = "https://onlinelibrary.wiley.com" + re.findall(regex_proteins_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_nature(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    selected = []
    reconstructed = []
    mydivs = soup.findAll("li")
    for ele in mydivs:
        link = ele.find('a')
        if "/nature/volumes/" in str(link):
            selected.append(link)
    for element in selected:
        volume_number = re.findall(regex_nature_volumes_numbers, str(element))[0]
        volume_link = re.findall(regex_biophysj_issue_link, str(element))[0]
        reconstructed.append(volume_number)
        volumes_dictionary[volume_number] = "http://www.nature.com/" + volume_link
    return reconstructed
def get_issue_nature(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    reconstructed = []
    mydivs = soup.findAll("a", class_="kill-hover flex-box-item")
    for ele in mydivs:
        issuestring = ele.find('h3', class_="h2 serif pa20 equalize-line-height text13")
        issue_number1 = re.findall(regex_nature_issues_numbers, str(issuestring))[:-1]
        issue_number = ", ".join(issue_number1).strip()
        issue_link = "https://www.nature.com" + re.findall(regex_nature_issues_link, str(ele))[0]
        reconstructed.append(issue_number)
        issues_dictionary[issue_number] = issue_link
    return reconstructed
def nature(url, mode):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.findAll("h3", class_="mb10 extra-tight-line-height")
    selected = []
    for x in mydivs:
        if mode == "all":
            title_all = re.findall(regex_nature_article_title, str(x))[2]
            title = title_all.strip()
            link = "https://www.nature.com" + re.findall(regex_nature_article_link, str(x))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(x) for a in mode):
            title_all = re.findall(regex_nature_article_title, str(x))[2]
            title = title_all.strip()
            link = "https://www.nature.com" + re.findall(regex_nature_article_link, str(x))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_nature_biotechnology(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    mydivs = soup.findAll("li")
    selected = []
    for ele in mydivs:
        h = ele.findAll("a")
        if "view volume" in str(h):
            title = re.findall(regex_nature_methods_volumes_title, str(h))[0]
            link = "https://www.nature.com" + re.findall(regex_nature_methods_volumes_link, str(h))[0]
            selected.append(title)
            volumes_dictionary[title] = link
    return selected
def get_issue_nature_biotechnology(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    selected = []
    mydivs = soup.findAll("a", class_="kill-hover flex-box-item")
    for ele in mydivs:
        title = "- ".join(re.findall(regex_nature_methods_issues_title, str(ele)))
        link = "https://www.nature.com" + re.findall(regex_nature_methods_issues_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def nature_biotechnology(url, mode):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.findAll("h3", class_="mb10 extra-tight-line-height")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_nature_methods(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    mydivs = soup.findAll("li")
    selected = []
    for ele in mydivs:
        h = ele.findAll("a")
        if "view volume" in str(h):
            title = re.findall(regex_nature_methods_volumes_title, str(h))[0]
            link = "https://www.nature.com" + re.findall(regex_nature_methods_volumes_link, str(h))[0]
            selected.append(title)
            volumes_dictionary[title] = link
    return selected
def get_issue_nature_methods(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    selected = []
    mydivs = soup.findAll("a", class_="kill-hover flex-box-item")
    for ele in mydivs:
        title = "- ".join(re.findall(regex_nature_methods_issues_title, str(ele)))
        link = "https://www.nature.com" + re.findall(regex_nature_methods_issues_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def nature_methods(url, mode):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.findAll("h3", class_="mb10 extra-tight-line-height")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_nature_protocols(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    mydivs = soup.findAll("li")
    selected = []
    for ele in mydivs:
        h = ele.findAll("a")
        if "view volume" in str(h):
            title = re.findall(regex_nature_methods_volumes_title, str(h))[0]
            link = "https://www.nature.com" + re.findall(regex_nature_methods_volumes_link, str(h))[0]
            selected.append(title)
            volumes_dictionary[title] = link
    return selected
def get_issue_nature_protocols(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    selected = []
    mydivs = soup.findAll("a", class_="kill-hover flex-box-item")
    for ele in mydivs:
        title = "- ".join(re.findall(regex_nature_methods_issues_title, str(ele)))
        link = "https://www.nature.com" + re.findall(regex_nature_methods_issues_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def nature_protocols(url, mode):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.findAll("h3", class_="mb10 extra-tight-line-height")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_nature_nrd(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    mydivs = soup.findAll("li")
    selected = []
    for ele in mydivs:
        h = ele.findAll("a")
        if "view volume" in str(h):
            title = re.findall(regex_nature_methods_volumes_title, str(h))[0]
            link = "https://www.nature.com" + re.findall(regex_nature_methods_volumes_link, str(h))[0]
            selected.append(title)
            volumes_dictionary[title] = link
    return selected
def get_issue_nature_nrd(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    selected = []
    mydivs = soup.findAll("a", class_="kill-hover flex-box-item")
    for ele in mydivs:
        title = "- ".join(re.findall(regex_nature_methods_issues_title, str(ele)))
        link = "https://www.nature.com" + re.findall(regex_nature_methods_issues_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def nature_nrd(url, mode):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.findAll("h3", class_="mb10 extra-tight-line-height")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_nature_nsmb(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    mydivs = soup.findAll("li")
    selected = []
    for ele in mydivs:
        h = ele.findAll("a")
        if "view volume" in str(h):
            title = re.findall(regex_nature_methods_volumes_title, str(h))[0]
            link = "https://www.nature.com" + re.findall(regex_nature_methods_volumes_link, str(h))[0]
            selected.append(title)
            volumes_dictionary[title] = link
    return selected
def get_issue_nature_nsmb(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    selected = []
    mydivs = soup.findAll("a", class_="kill-hover flex-box-item")
    for ele in mydivs:
        title = "- ".join(re.findall(regex_nature_methods_issues_title, str(ele)))
        link = "https://www.nature.com" + re.findall(regex_nature_methods_issues_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def nature_nsmb(url, mode):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.findAll("h3", class_="mb10 extra-tight-line-height")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_nature_methods_article_title, str(ele))[1].strip()
            link = "https://www.nature.com" + re.findall(regex_nature_methods_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected



# TODO: journals to be added:
# Ann.Rev.Biochemistry
# Ann.Rev.Biophysics
# J.Magn.Reson.
# J.Biomol.NMR
# Protein Science
# BBA Biomembranes
# Biochemistry
# Protein Expression and Purification
# JBC
# Structure
# Current opinions in structural biology
# Journal of Magnetic Resonance
# Journal of Biomolecular NMR
# JACS
# Mol.Cell
# Chemistry & Biology
# PLOS ONE
# Trends in Biotechnology
# Annual Reviews in Biochemistry
# Curr.Oppin.Chemical Biol. & Biotech.
# Biopolymers
# Annual Reviews in Biophys. & Biomol.Structure
# PNAS
# JMB
# Febs Letters
# TIBS
# Science SKTE
# TIPS
# Methods in Enzymology