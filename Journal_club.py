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
    Custom: create your own custom list of keywords.
                Best suited for: very specific user needs.
    All: list all the articles in the selected issue.
                Best suited for: completionists?
    Funny: search for funny articles.
                Best suited for: it's 11 pm and I am still in the office.
    Impact Factors: no search, list in descending order the journals impact factors.

    For more info, select a mode and click on the "Mode Info" button.

    """
    # just to a have a general docstring
    pass


# keywords lists
journals = ['Nature', 'Biophysical Journal', 'Proteins', "EMBO", "Cell", "Angewandte", "Nature Methods", "Nature Protocols", "Nature Biotechnology", "Nature Structural and Molecular Biology", "Nature Reviews Drug Discovery", "Annual Reviews of Biochemistry", "Annual Reviews of Biophysics", "Journal of Biomolecular NMR", "Protein Science", "ACS - Biochemistry", "Journal of Biological Chemistry", "Cell - Structure", "Trends in Pharmacological Sciences", "Trends in Biochemical Sciences", "Trends in Biotechnology", "Molecular Cell", "FEBS letters", "Biopolymers", "Journal of the American Chemical Society (JACS)", "PNAS", "Science (AAAS)", "Science Advances", "Science Immunology", "Science Robotics", "Science Signaling", "Science Translational Medicine"]
modes = ['Standard', 'Loose', 'All', 'Funny', 'Custom', 'Impact Factors']
standard = []
loose = []
funny = []
custom = []
standard_ini = ["Nmr", "NMR", "Dynamic", "Membrane", "Structural", "Conformational", "Rhodopsin", "Gpcr", "Relaxation", "G-Coupled", "Spectroscopy", "Metallothionein", "Adrenergic", "Paramagnetic", "Chemical shift", "Nanodiscs", "Lipid", "Magnetic", "Crystal", "Computational", "Peptide", "Labeling", "Labelling", "Zinc", "Zn", "Folding", "Ghrelin", "Methyl", "Heliorhodopsin", "EM", "Retina", "Isotope", "Gloeobacter", "113cd", "Α1b", "Unfolding", "Prion", "Sidechain", "Spectrum", "Spectra", "Spin", "Spectrometry", "Ramachandran", "Armadillo", "dArmRP", "Repetitive protein", "Resonance", "Dipolar", "RDC", "Rdc", "Deuterated", "Cryoem", "Amide", "13c", "19f", "7tm", "Adrenoceptor", "Isotopical", "Misfolding", "Ubiquitin", "Alanine", "Arginine", "Asparagine", "Aspartic acid", "Cysteine", "Glutamic acid", "Glutamine", "Glycine", "Histidine", "Isoleucine", "Leucine", "Lysine", "Methionine", "Phenylalanine", "Proline", "Serine", "Threonine", "Tryptophan", "Tyrosine", "Valine", "PCS", "Pcs", "Pseudocontact"]
loose_ini = ["Protein", "Receptor", "Structure", "E. coli", "Cryo", "Structure", "Amino", "Mutation", "Microscopy", "Metal", "Polypeptide", "Photoluminescence", "Photoexcited", "Pharmacological", "Modeling", "Neuropeptide", "Selectivity", "Scaffold", "Schiff", "Surface", "Subatomic", "Thermostabilization", "Residue", "Catalytic", "Channel", "Codons", "Cofactor", "Crispr", "Bioinformatics", "Biomedical", "Biomolecular", "Kinetic", "Enzyme", "Hydrophilic", "Hydrophobic", "Response"]
funny_ini = ["Vietnam", "Paradox", "Police", "Parachute", "Sadness", "Stupidity", "Troll", "Hate", "Marvel", "Thanos", "Batman", "Funny", "Joke"]


def capital(list, new):
    decapitalize = lambda s: s[:1].lower() + s[1:] if s else ''
    for word in list:
        decap = decapitalize(word)
        new.append(word)
        new.append(decap) #TOD
capital(standard_ini, standard)
loose_ini2 = loose_ini + standard_ini
capital(loose_ini2, loose)
capital(funny_ini, funny)

# dictionaries
volumes_url = {"Nature": "https://www.nature.com/nature/volumes", "Biophysical Journal": "https://www.cell.com/biophysj/archive", "Proteins": "https://onlinelibrary.wiley.com/loi/10970134", "EMBO": "https://www.embopress.org/loi/14602075", "Cell": "https://www.cell.com/cell/archive", "Angewandte": "https://onlinelibrary.wiley.com/loi/15213773", "Nature Methods" : "https://www.nature.com/nmeth/volumes", "Nature Protocols": "https://www.nature.com/nprot/volumes", "Nature Biotechnology": "https://www.nature.com/nbt/volumes", "Nature Structural and Molecular Biology": "https://www.nature.com/nsmb/volumes", "Nature Reviews Drug Discovery": "https://www.nature.com/nrd/volumes", "Annual Reviews of Biochemistry": "https://www.annualreviews.org/loi/biochem", "Annual Reviews of Biophysics": "https://www.annualreviews.org/loi/biophys", "Journal of Magnetic Resonance": "https://www.sciencedirect.com/journal/journal-of-magnetic-resonance/issues", "Journal of Biomolecular NMR": "https://link.springer.com/journal/volumesAndIssues/10858", "Protein Science": "https://onlinelibrary.wiley.com/loi/1469896x", "ACS - Biochemistry": "https://pubs.acs.org/loi/bichaw", "Journal of Biological Chemistry": "http://www.jbc.org/content/by/year", "Cell - Structure": "https://www.cell.com/structure/archive", "Trends in Pharmacological Sciences": "https://www.cell.com/trends/pharmacological-sciences/archive", "Trends in Biochemical Sciences": "https://www.cell.com/trends/biochemical-sciences/archive", "Trends in Biotechnology": "https://www.cell.com/trends/biotechnology/archive", "Molecular Cell": "https://www.cell.com/molecular-cell/archive", "FEBS letters": "https://febs.onlinelibrary.wiley.com/loi/18733468", "Biopolymers": "https://onlinelibrary.wiley.com/loi/10970282", "Journal of the American Chemical Society (JACS)": "https://pubs.acs.org/loi/jacsat", "PNAS": "https://www.pnas.org/content/by/year", "Science (AAAS)": "https://science.sciencemag.org/content/by/year", "Science Advances": "https://advances.sciencemag.org/content/by/year", "Science Immunology": "https://immunology.sciencemag.org/content/by/year", "Science Robotics": "https://robotics.sciencemag.org/content/by/year", "Science Signaling": "https://stke.sciencemag.org/content/by/year", "Science Translational Medicine": "https://stm.sciencemag.org/content/by/year"}
modes_dictionary = {"Standard": standard, "Loose": loose, "Funny": funny, "All": "all", "Custom": custom}
volumes_dictionary = {}
issues_dictionary = {}
impact_factor_dictionary = {'Nature': 43.070,'Biophysical Journal': 3.665, 'Proteins': 2.499, "EMBO": 11.2, "Cell": 36.216, "Angewandte": 12.257, "Nature Methods": 28.467, "Nature Protocols": 15.086, "Nature Biotechnology": 35.724, "Nature Structural and Molecular Biology": 12.595, "Nature Reviews Drug Discovery": 57.000, "Annual Reviews of Biochemistry": 30.283, "Annual Reviews of Biophysics": 12.250, "Journal of Biomolecular NMR": 2.534, "Protein Science": 2.735, "ACS - Biochemistry": 2.876, "Journal of Biological Chemistry": 4.106, "Cell - Structure": 4.576, "Trends in Pharmacological Sciences": 10.148, "Trends in Biochemical Sciences": 14.273, "Trends in Biotechnology": 2.370, "Molecular Cell": 14.548, "FEBS letters": 2.675, "Biopolymers": 2.248, "Journal of the American Chemical Society (JACS)": 14.695, "PNAS": 9.58, "Science (AAAS)": 41.063, "Science Advances": 12.804, "Science Immunology": 10.551, "Science Robotics": 19.400, "Science Signaling": 6.481, "Science Translational Medicine": 16.796}

# selection regular expressions
regex_acs_biochemistry_issue_title1 = "class=\"coverDate\">(.*?)</span>"
regex_acs_biochemistry_issue_title2 = "class=\"comma\">(.*?)</span>"
regex_acs_biochemistry_issue_title3 = "</span>(.*?)</a>"
regex_acs_biochemistry_issue_link = "href=\"(.*?)\">"
regex_acs_biochemistry_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_acs_biochemistry_article_link = "href=\"(.*?)\">"

regex_arb_volumes_title = "\">(.*?)<"
regex_arb_volumes_link = "href=\"(.*?)\""
regex_arb_article_title = "\">(.*?)\">(.*?)</span>"
regex_arb_article_link = "href=\"(.*?)\">"

regex_arbf_volumes_title = "\">(.*?)<"
regex_arbf_volumes_link = "href=\"(.*?)\""
regex_arbf_article_title = "\">(.*?)\">(.*?)</span>"
regex_arbf_article_link = "href=\"(.*?)\">"

regex_angewandte_issue_title = "href=\"(.*?)\">(.*?)</a>"
regex_angewandte_issue_link = "href=\"(.*?)\""
regex_angewandte_article_title = "h2>(.*?)\s*</h2"
regex_angewandte_article_link = "href=\"(.*?)\""

regex_biopolymers_issue_title = "href=\"(.*?)\">(.*?)</a>"
regex_biopolymers_issue_link = "href=\"(.*?)\""
regex_biopolymers_article_title = "h2>(.*?)\s*</h2"
regex_biopolymers_article_link = "href=\"(.*?)\""

regex_febs_letters_issue_title = "href=\"(.*?)\">(.*?)</a>"
regex_febs_letters_issue_link = "href=\"(.*?)\""
regex_febs_letters_article_title = "h2>(.*?)\s*</h2"
regex_febs_letters_article_link = "href=\"(.*?)\""

regex_biophysj_issue_title = ">(.*?)<"
regex_biophysj_issue_link = "=\"/(.*?)\">"
regex_biophysj_article_title = ">(.*?)<"
regex_biophysj_article_link = "=\"(.*?)\">"

regex_cell_issue_title = "<strong> (.*?) </strong> (.*?)</a>"
regex_cell_issue_link = "href=\"(.*?)\">"
regex_cell_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_cell_article_link = "href=\"(.*?)\">"

regex_cell_structure_issue_title = "<strong> (.*?) </strong> (.*?)</a>"
regex_cell_structure_issue_link = "href=\"(.*?)\">"
regex_cell_structure_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_cell_structure_article_link = "href=\"(.*?)\">"

regex_EMBO_issue_title = "\">(.*?)<"
regex_EMBO_issue_link = "href=\"(.*?)\""
regex_EMBO_article_title = "h5>(.*?)\s*</h5"
regex_EMBO_article_link = "href=\"(.*?)\">"

regex_jacs_issue_title1 = "class=\"coverDate\">(.*?)</span>"
regex_jacs_issue_title2 = "class=\"comma\">(.*?)</span>"
regex_jacs_issue_title3 = "</span>(.*?)</a>"
regex_jacs_issue_link = "href=\"(.*?)\">"
regex_jacs_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_jacs_article_link = "href=\"(.*?)\">"

regex_jbc_volumes_title = "href=\"(.*?)\">(.*?)</a>"
regex_jbc_volumes_link = "href=\"(.*?)\">"
regex_jbc_issues_title_a = "\">(.*?)</a>"
regex_jbc_issues_title_b = "href=\"/content/(.*?)/index"
regex_jbc_issues_link = "href=\"(.*?)\">"
regex_jbc_article_title = "\">(.*?)\s*(.*?)\s*</h"
regex_jbc_article_link_page = "class=\"cit-first-page\">(.*?)</span>"

regex_jbnmr_issues_title = "\">\s*(.*?)\s*<"
regex_jbnmr_issues_link = "href=\"(.*?)\""
regex_jbnmr_article_title = "\">(.*?)<"
regex_jbnmr_article_link = "href=\"(.*?)\""

regex_proteins_issue_title = "\">(.*?)<"
regex_proteins_issue_link = "href=\"(.*?)\""
regex_proteins_article_title = "2>(.*?)</"
regex_proteins_article_link = "href=\"(.*?)\">"

regex_molecular_cell_issue_title = "<strong> (.*?) </strong> (.*?)</a>"
regex_molecular_cell_issue_link = "href=\"(.*?)\">"
regex_molecular_cell_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_molecular_cell_article_link = "href=\"(.*?)\">"

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

regex_tips_issue_title = "<strong> (.*?) </strong> (.*?)</a>"
regex_tips_issue_link = "href=\"(.*?)\">"
regex_tips_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_tips_article_link = "href=\"(.*?)\">"

regex_tibs_issue_title = "<strong> (.*?) </strong> (.*?)</a>"
regex_tibs_issue_link = "href=\"(.*?)\">"
regex_tibs_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_tibs_article_link = "href=\"(.*?)\">"

regex_trends_biotechnology_issue_title = "<strong> (.*?) </strong> (.*?)</a>"
regex_trends_biotechnology_issue_link = "href=\"(.*?)\">"
regex_trends_biotechnology_article_title = "href=\"(.*?)\">(.*?)</a>"
regex_trends_biotechnology_article_link = "href=\"(.*?)\">"

regex_pnas_issue_title1 = "metadata\">(.*?)\s*</span>"
regex_pnas_issue_title2 = "\">(.*?)</span>"
regex_pnas_issue_link = "href=\"(.*?)\">"
regex_pnas_article_title = "title\">\s*(.*?)\s*</span>"
regex_pnas_article_link = "href=\"(.*?)\">"

regex_science_issue_title1 = "subtitle\">(.*?)</h3>"
regex_science_issue_title2 = "priority-2\">(.*?)</p>"
regex_science_issue_link = "href=\"(.*?)\">"
regex_science_article_title = "title\">(.*?)</"
regex_science_article_link = "href=\"(.*?)\">"

regex_science_advances_issue_title1 = "subtitle\">(.*?)</h3>"
regex_science_advances_issue_title2 = "priority-2\">(.*?)</p>"
regex_science_advances_issue_link = "href=\"(.*?)\">"
regex_science_advances_article_title = "title\">(.*?)</"
regex_science_advances_article_link = "href=\"(.*?)\">"

regex_science_immunology_issue_title1 = "subtitle\">(.*?)</h3>"
regex_science_immunology_issue_title2 = "priority-2\">(.*?)</p>"
regex_science_immunology_issue_link = "href=\"(.*?)\">"
regex_science_immunology_article_title = "title\">(.*?)</"
regex_science_immunology_article_link = "href=\"(.*?)\">"

regex_science_robotics_issue_title1 = "subtitle\">(.*?)</h3>"
regex_science_robotics_issue_title2 = "priority-2\">(.*?)</p>"
regex_science_robotics_issue_link = "href=\"(.*?)\">"
regex_science_robotics_article_title = "title\">(.*?)</"
regex_science_robotics_article_link = "href=\"(.*?)\">"

regex_science_signaling_issue_title1 = "subtitle\">(.*?)</h3>"
regex_science_signaling_issue_title2 = "priority-2\">(.*?)</p>"
regex_science_signaling_issue_link = "href=\"(.*?)\">"
regex_science_signaling_article_title = "title\">(.*?)</"
regex_science_signaling_article_link = "href=\"(.*?)\">"

regex_science_translational_medicine_issue_title1 = "subtitle\">(.*?)</h3>"
regex_science_translational_medicine_issue_title2 = "priority-2\">(.*?)</p>"
regex_science_translational_medicine_issue_link = "href=\"(.*?)\">"
regex_science_translational_medicine_article_title = "title\">(.*?)</"
regex_science_translational_medicine_article_link = "href=\"(.*?)\">"



# sorts
journals.sort(key=str.casefold)
modes.sort(key=str.casefold)
standard.sort(key=str.casefold)
loose.sort(key=str.casefold)
funny.sort(key=str.casefold)

# functions
def get_issues_acs_biochemistry(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("div", class_="parent-item")
    selected = []
    for ele in mydivs:
        title = re.findall(regex_acs_biochemistry_issue_title1, str(ele))[0] + " - " + re.findall(regex_acs_biochemistry_issue_title2, str(ele))[0] + " - " + re.findall(regex_acs_biochemistry_issue_title3, str(ele))[1]
        link = "https://pubs.acs.org" + re.findall(regex_acs_biochemistry_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
        print(ele)
    return selected
def acs_biochemistry(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h5", class_="issue-item_title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_acs_biochemistry_article_title, str(ele))[0]))[1])
            link = "https://pubs.acs.org" + re.findall(regex_acs_biochemistry_issue_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_acs_biochemistry_article_title, str(ele))[0]))[1])
            link = "https://pubs.acs.org" + re.findall(regex_acs_biochemistry_issue_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_arb(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    mydivs = soup.findAll("li")
    selected = []
    for ele in mydivs:
        h = ele.findAll("a")
        if "Vol." in str(h):
            title = re.findall(regex_arb_volumes_title, str(h))[0]
            link = "https://www.annualreviews.org" + re.findall(regex_arb_volumes_link, str(h))[0]
            selected.append(title)
            volumes_dictionary[title] = link
    return selected
def arb(url, mode):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.findAll("div", class_="text")
    selected = []
    for ele in mydivs:
        a = ele.findAll("a")
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_arb_article_title, str(a))[0]))[1])
            link = "https://www.annualreviews.org" + re.findall(regex_arb_article_link, str(a))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_arb_article_title, str(a))[0]))[1])
            link = "https://www.annualreviews.org" + re.findall(regex_arb_article_link, str(a))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_arbf(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a element with the correct class and select
    mydivs = soup.findAll("li")
    selected = []
    for ele in mydivs:
        h = ele.findAll("a")
        if "Vol." in str(h):
            title = re.findall(regex_arbf_volumes_title, str(h))[0]
            link = "https://www.annualreviews.org" + re.findall(regex_arbf_volumes_link, str(h))[0]
            selected.append(title)
            volumes_dictionary[title] = link
    return selected
def arbf(url, mode):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mydivs = soup.findAll("div", class_="text")
    selected = []
    for ele in mydivs:
        a = ele.findAll("a")
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_arbf_article_title, str(a))[0]))[1])
            link = "https://www.annualreviews.org" + re.findall(regex_arbf_article_link, str(a))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_arbf_article_title, str(a))[0]))[1])
            link = "https://www.annualreviews.org" + re.findall(regex_arbf_article_link, str(a))[0]
            selected.append(title)
            selected.append(link)
    return selected

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

def get_issues_febs_letters(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h4", class_="parent-item")
    selected = []
    for ele in mydivs:
        title = "".join(list(zip(re.findall(regex_febs_letters_issue_title, str(ele))[0]))[1])
        link = "https://onlinelibrary.wiley.com" + re.findall(regex_febs_letters_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def febs_letters(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issue-item__title visitable")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_febs_letters_article_title, str(ele))[0]
            link = "https://onlinelibrary.wiley.com" + re.findall(regex_febs_letters_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_febs_letters_article_title, str(ele))[0]
            link = "https://onlinelibrary.wiley.com" + re.findall(regex_febs_letters_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_biopolymers(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h4", class_="parent-item")
    selected = []
    for ele in mydivs:
        title = "".join(list(zip(re.findall(regex_biopolymers_issue_title, str(ele))[0]))[1])
        link = "https://onlinelibrary.wiley.com" + re.findall(regex_biopolymers_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def biopolymers(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issue-item__title visitable")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_biopolymers_article_title, str(ele))[0]
            link = "https://onlinelibrary.wiley.com" + re.findall(regex_biopolymers_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_biopolymers_article_title, str(ele))[0]
            link = "https://onlinelibrary.wiley.com" + re.findall(regex_biopolymers_article_link, str(ele))[0]
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
            link = "https://www.cell.com" + re.findall(regex_cell_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_cell_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_cell_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_cell_structure(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issueLinkCon")
    selected = []
    for ele in mydivs:
        title = " - ".join(re.findall(regex_cell_structure_issue_title, str(ele))[0])
        link = "https://www.cell.com" + re.findall(regex_cell_structure_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def cell_structure(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h3", class_="toc__item__title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_cell_structure_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_cell_structure_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_cell_structure_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_cell_structure_article_link, str(ele))[0]
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

def get_issues_jacs(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("div", class_="parent-item")
    selected = []
    for ele in mydivs:
        title = re.findall(regex_jacs_issue_title1, str(ele))[0] + " - " + re.findall(regex_jacs_issue_title2, str(ele))[0] + " - " + re.findall(regex_jacs_issue_title3, str(ele))[1]
        link = "https://pubs.acs.org" + re.findall(regex_jacs_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def jacs(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h5", class_="issue-item_title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_jacs_article_title, str(ele))[0]))[1])
            link = "https://pubs.acs.org" + re.findall(regex_jacs_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_jacs_article_title, str(ele))[0]))[1])
            link = "https://pubs.acs.org" + re.findall(regex_jacs_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_volumes_jbc(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("td", class_="proxy-archive-year")
    selected = []
    for ele in mydivs:
        try:
            title = "".join(list(zip(re.findall(regex_jbc_volumes_title, str(ele))[0]))[1])
        except IndexError:
            break
        title = "".join(list(zip(re.findall(regex_jbc_volumes_title, str(ele))[0]))[1])
        link = "http://www.jbc.org/" + re.findall(regex_jbc_volumes_link, str(ele))[0]
        selected.append(title)
        volumes_dictionary[title] = link
    selected.sort(reverse=True)
    return selected
def get_issues_jbc(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("td", class_="proxy-archive-by-year-month")
    selected = []
    for ele in mydivs:
        title1 = ", ".join(re.findall(regex_jbc_issues_title_b, str(ele))[0].split(
            "/"))   + " - " + re.findall(regex_jbc_issues_title_a, str(ele))[0]
        title2 = ", ".join(re.findall(regex_jbc_issues_title_b, str(ele))[1].split(
            "/"))   + " - " + re.findall(regex_jbc_issues_title_a, str(ele))[1]
        title3 = ", ".join(re.findall(regex_jbc_issues_title_b, str(ele))[2].split(
            "/"))   + " - " + re.findall(regex_jbc_issues_title_a, str(ele))[2]
        title4 = ", ".join(re.findall(regex_jbc_issues_title_b, str(ele))[3].split(
            "/"))   + " - " + re.findall(regex_jbc_issues_title_a, str(ele))[3]
        link1 = "http://www.jbc.org/" + re.findall(regex_jbc_issues_link, str(ele))[0]
        link2 = "http://www.jbc.org/" + re.findall(regex_jbc_issues_link, str(ele))[1]
        link3 = "http://www.jbc.org/" + re.findall(regex_jbc_issues_link, str(ele))[2]
        link4 = "http://www.jbc.org/" + re.findall(regex_jbc_issues_link, str(ele))[3]
        selected.append(title1)
        selected.append(title2)
        selected.append(title3)
        selected.append(title4)
        issues_dictionary[title1] = link1
        issues_dictionary[title2] = link2
        issues_dictionary[title3] = link3
        issues_dictionary[title4] = link4
    def sorted_nicely(l):
        """ Sort the given iterable in the way that humans expect."""
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key, reverse=True)
    mysorted = sorted_nicely(selected)
    return mysorted
def jbc(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("div", class_="cit-metadata")
    selected = []
    if mode == "all":
        for ele in mydivs:
            h4 = ele.findAll('h4')
            title_list = re.findall(regex_jbc_article_title, str(h4))
            def joining(list):
                    for element in list:
                        if element == "":
                            pass
                        else:
                            title_join = " ".join(element)
                            return title_join.strip()
            title = joining(title_list)
            cite = ele.findAll('cite')
            page = re.findall(regex_jbc_article_link_page, str(cite))[0]
            link = ".".join(url.split(".")[:-1]) + "/" + page + ".short"
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_jbnmr(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="title")
    selected = []
    # reconstruction loop
    for ele in mydivs:
        title = re.findall(regex_jbnmr_issues_title, str(ele))[0]
        link = "https://link.springer.com" + re.findall(regex_jbnmr_issues_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def jbnmr(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h3", class_="title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_jbnmr_article_title, str(ele))[0]
            link = "https://link.springer.com" + re.findall(regex_jbnmr_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_jbnmr_article_title, str(ele))[0]
            link = "https://link.springer.com" + re.findall(regex_jbnmr_article_link, str(ele))[0]
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

def get_issues_protein_science(url):
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
def protein_science(url, mode):
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

def get_issues_molecular_cell(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issueLinkCon")
    selected = []
    for ele in mydivs:
        title = " - ".join(re.findall(regex_molecular_cell_issue_title, str(ele))[0])
        link = "https://www.cell.com" + re.findall(regex_molecular_cell_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def molecular_cell(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h3", class_="toc__item__title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_molecular_cell_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_molecular_cell_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_molecular_cell_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_molecular_cell_article_link, str(ele))[0]
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

def get_issues_tips(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issueLinkCon")
    selected = []
    for ele in mydivs:
        title = " - ".join(re.findall(regex_tips_issue_title, str(ele))[0])
        link = "https://www.cell.com" + re.findall(regex_tips_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def tips(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h3", class_="toc__item__title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_tips_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_tips_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_tips_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_tips_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_tibs(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issueLinkCon")
    selected = []
    for ele in mydivs:
        title = " - ".join(re.findall(regex_tibs_issue_title, str(ele))[0])
        link = "https://www.cell.com" + re.findall(regex_tibs_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def tibs(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h3", class_="toc__item__title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_tibs_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_tibs_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_tibs_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_tibs_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_trends_biotechnology(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="issueLinkCon")
    selected = []
    for ele in mydivs:
        title = " - ".join(re.findall(regex_trends_biotechnology_issue_title, str(ele))[0])
        link = "https://www.cell.com" + re.findall(regex_trends_biotechnology_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def trends_biotechnology(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("h3", class_="toc__item__title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = "".join(list(zip(re.findall(regex_trends_biotechnology_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_trends_biotechnology_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = "".join(list(zip(re.findall(regex_trends_biotechnology_article_title, str(ele))[0]))[1])
            link = "https://www.cell.com" + re.findall(regex_trends_biotechnology_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_pnas(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="hw-issue-meta-data")
    selected = []
    for ele in mydivs:
        title = re.findall(regex_pnas_issue_title1, str(ele))[0] + " - " + " - ".join(re.findall(regex_pnas_issue_title2, str(ele))[1:])
        link = "https://www.pnas.org/" + re.findall(regex_pnas_issue_link, str(ele))[0]
        selected.append(title)
        issues_dictionary[title] = link
    return selected
def pnas(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_pnas_article_title, str(ele))[0]
            link = "https://www.pnas.org/" + re.findall(regex_pnas_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_pnas_article_title, str(ele))[0]
            link = "https://www.pnas.org/" + re.findall(regex_pnas_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_science(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if "subtitle" in str(ele):
            title = re.findall(regex_science_issue_title1, str(ele))[0] + " - " + re.findall(regex_science_issue_title2, str(ele))[0]
            link = "https://science.sciencemag.org/" + re.findall(regex_science_issue_link, str(ele))[0]
            selected.append(title)
            issues_dictionary[title] = link
    return selected
def science_(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_science_article_title, str(ele))[0]
            link = "https://science.sciencemag.org/" + re.findall(regex_science_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_science_article_title, str(ele))[0]
            link = "https://science.sciencemag.org/" + re.findall(regex_science_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_science_advances(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if "subtitle" in str(ele):
            title = re.findall(regex_science_advances_issue_title1, str(ele))[0] + " - " + re.findall(regex_science_advances_issue_title2, str(ele))[0]
            link = "https://advances.sciencemag.org/" + re.findall(regex_science_advances_issue_link, str(ele))[0]
            selected.append(title)
            issues_dictionary[title] = link
    return selected
def science_advances(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_science_advances_article_title, str(ele))[0]
            link = "https://advances.sciencemag.org/" + re.findall(regex_science_advances_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_science_advances_article_title, str(ele))[0]
            link = "https://advances.sciencemag.org/" + re.findall(regex_science_advances_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_science_immunology(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if "subtitle" in str(ele):
            title = re.findall(regex_science_immunology_issue_title1, str(ele))[0] + " - " + re.findall(regex_science_immunology_issue_title2, str(ele))[0]
            link = "https://immunology.sciencemag.org/" + re.findall(regex_science_immunology_issue_link, str(ele))[0]
            selected.append(title)
            issues_dictionary[title] = link
    return selected
def science_immunology(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_science_immunology_article_title, str(ele))[0]
            link = "https://immunology.sciencemag.org/" + re.findall(regex_science_immunology_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_science_immunology_article_title, str(ele))[0]
            link = "https://immunology.sciencemag.org/" + re.findall(regex_science_immunology_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_science_robotics(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if "subtitle" in str(ele):
            title = re.findall(regex_science_robotics_issue_title1, str(ele))[0] + " - " + re.findall(regex_science_robotics_issue_title2, str(ele))[0]
            link = "https://robotics.sciencemag.org/" + re.findall(regex_science_robotics_issue_link, str(ele))[0]
            selected.append(title)
            issues_dictionary[title] = link
    return selected
def science_robotics(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_science_robotics_article_title, str(ele))[0]
            link = "https://robotics.sciencemag.org/" + re.findall(regex_science_robotics_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_science_robotics_article_title, str(ele))[0]
            link = "https://robotics.sciencemag.org/" + re.findall(regex_science_robotics_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_science_signaling(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if "subtitle" in str(ele):
            title = re.findall(regex_science_signaling_issue_title1, str(ele))[0] + " - " + re.findall(regex_science_signaling_issue_title2, str(ele))[0]
            link = "https://stke.sciencemag.org/" + re.findall(regex_science_signaling_issue_link, str(ele))[0]
            selected.append(title)
            issues_dictionary[title] = link
    return selected
def science_signaling(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_science_signaling_article_title, str(ele))[0]
            link = "https://stke.sciencemag.org/" + re.findall(regex_science_signaling_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_science_signaling_article_title, str(ele))[0]
            link = "https://stke.sciencemag.org/" + re.findall(regex_science_signaling_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

def get_issues_science_translational_medicine(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if "subtitle" in str(ele):
            title = re.findall(regex_science_translational_medicine_issue_title1, str(ele))[0] + " - " + re.findall(regex_science_translational_medicine_issue_title2, str(ele))[0]
            link = "https://stm.sciencemag.org/" + re.findall(regex_science_translational_medicine_issue_link, str(ele))[0]
            selected.append(title)
            issues_dictionary[title] = link
    return selected
def science_translational_medicine(url, mode):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("a", class_="highwire-cite-linked-title")
    selected = []
    for ele in mydivs:
        if mode == "all":
            title = re.findall(regex_science_translational_medicine_article_title, str(ele))[0]
            link = "https://stm.sciencemag.org/" + re.findall(regex_science_translational_medicine_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
        elif any(a in str(ele) for a in mode):
            title = re.findall(regex_science_translational_medicine_article_title, str(ele))[0]
            link = "https://stm.sciencemag.org/" + re.findall(regex_science_translational_medicine_article_link, str(ele))[0]
            selected.append(title)
            selected.append(link)
    return selected

# TODO: journals to be added:

# TODO: journals that does not allow web scraping
# Elsevier: J.Magn.Reson., BBA Biomembranes, Protein Expression and Purification, Current opinions in structural biology, Chemistry & Biology, Curr.Oppin.Chemical Biol. & Biotech., Journal of Molecular Biology, Methods in Enzymology

# TODO: reference web architecture
# Wiley: angewandte
# Springer : Nature
# cellpress: Cell
# acs publications: acs biochemistry
# super weird: jbc
# procedings of the national academy of sciences of the usa:  pnas
# zip titles: acs biochemistry
# aaas: science
