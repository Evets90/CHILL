import requests
import datetime
import re
from bs4 import BeautifulSoup

def general_docstring():
    """This page is an addon to the standard Journal Club page to search for those journal which do not have
    a volume/issue structure (i.e. Nature Communications) through PubMed. You will be able to perform a
    quick scan of those scientific journals to get a sub-list of articles based on a certain keyword in
    the title.
    You need to select a mode, a time range and then a journal. For an explanation of the modes, refer to
    the standard Journal Club page. Time ranges scan anything between Today and the selected limit. The
    resulting articles are listed by 'Most Recent' and only a maximum of 20 articles can be displayed. As
    a workaround if the limit is reached you will be able to copy the URL to PubMed with a button.
    """
    # just to a have a general docstring
    pass


# keywords lists
journals = ['Nature Communications', 'eLife', 'PLOS One', "Scientific Reports"]
modes = ['Standard', 'Loose', 'Funny', 'Custom', 'Impact Factors']
standard = []
loose = []
funny = []
custom = []
standard_ini = ["Nmr", "NMR", "Dynamic", "Membrane", "Structural", "Conformational", "Rhodopsin", "Gpcr", "Relaxation", "G-Coupled", "Spectroscopy", "Metallothionein", "Adrenergic", "Paramagnetic", "Chemical shift", "Nanodiscs", "Lipid", "Magnetic", "Crystal", "Computational", "Peptide", "Labeling", "Labelling", "Zinc", "Zn", "Folding", "Ghrelin", "Methyl", "Heliorhodopsin", "EM", "Retina", "Isotope", "Gloeobacter", "113cd", "Α1b", "Unfolding", "Prion", "Sidechain", "Spectrum", "Spectra", "Spin", "Spectrometry", "Ramachandran", "Armadillo", "dArmRP", "Repetitive protein", "Resonance", "Dipolar", "RDC", "Rdc", "Deuterated", "Cryoem", "Amide", "13c", "19f", "7tm", "Adrenoceptor", "Isotopical", "Misfolding", "Ubiquitin", "Alanine", "Arginine", "Asparagine", "Aspartic acid", "Cysteine", "Glutamic acid", "Glutamine", "Glycine", "Histidine", "Isoleucine", "Leucine", "Lysine", "Methionine", "Phenylalanine", "Proline", "Serine", "Threonine", "Tryptophan", "Tyrosine", "Valine", "PCS", "Pcs", "Pseudocontact", "Modular", "Antibacterial", "Darpin", "Coiled", "Adrenoreceptor", "Lpt", "Bacteriorhodopsin"]
loose_ini = ["Protein", "Receptor", "Structure", "E. coli", "Cryo", "Structure", "Amino", "Mutation", "Microscopy", "Metal", "Polypeptide", "Photoluminescence", "Photoexcited", "Pharmacological", "Modeling", "Neuropeptide", "Selectivity", "Scaffold", "Schiff", "Surface", "Subatomic", "Thermostabilization", "Residue", "Catalytic", "Channel", "Codons", "Cofactor", "Crispr", "Bioinformatics", "Biomedical", "Biomolecular", "Kinetic", "Enzyme", "Hydrophilic", "Hydrophobic", "Response", "Biopolymer", "Rosetta"]
funny_ini = ["Vietnam", "Paradox", "Police", "Parachute", "Sadness", "Stupidity", "Troll", "Hate", "Marvel", "Thanos", "Batman", "Funny", "Joke", "Emotion", "Secret", "Starcraft"]


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
modes_dictionary = {"Standard": standard, "Loose": loose, "Funny": funny, "Custom": custom}
impact_factor_dictionary = {'Nature Communications': 11.878, 'eLife': 7.551, 'PLOS One': 2.776, "Scientific Reports": 4.122}
Journals_dictionary = {"Nature Communications": "Nature+communications", "eLife": "eLife", "PLOS One": "PloS%20one", "Scientific Reports": "Scientific%20reports"}
Time_range_list = ["Last week", "Last two weeks", "Last month", "Last six months", "Last year"]

# sorts
journals.sort(key=str.casefold)
modes.sort(key=str.casefold)
standard.sort(key=str.casefold)
loose.sort(key=str.casefold)
funny.sort(key=str.casefold)

# functions
def get_article(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mydivs = soup.findAll("p", class_="title")
    selected = []
    for ele in mydivs:
        title = ele.get_text()
        link = "https://www.ncbi.nlm.nih.gov" + str(ele.find('a').get('href'))
        selected.append(title)
        selected.append(link)
    return selected

def get_limit(url):
    # preparation
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # look for a elements with correct class
    mytag = soup.findAll("h3", class_="result_count left")
    #limit = int(mytag[0].get_text().split(": ")[1])
    limitlist = re.findall(r'\d+', str(mytag[0].get_text()))
    if len(limitlist) == 1:
        limit = int(limitlist[0])
    else:
        limit = int(limitlist[1])
    return limit


def construct_url(journal, keywords, time):
    """Construct the PubMed query url based on a journal, keywords and start time range"""
    global t
    if time == "Last week":
        t = datetime.date.today() - datetime.timedelta(days=7)
    elif time == "Last two weeks":
        t = datetime.date.today() - datetime.timedelta(days=14)
    elif time == "Last month":
        t = datetime.date.today() - datetime.timedelta(days=31)
    elif time == "Last six months":
        t = datetime.date.today() - datetime.timedelta(days=217)
    elif time == "Last year":
        t = datetime.date.today() - datetime.timedelta(days=365)
    else:
        exit(365)
    # Initial stem
    p1 = "https://www.ncbi.nlm.nih.gov/pubmed/?term=((%22"
    # Journal name
    p2= journal
    # Bridge to keywords
    p3 = "%22%5BJournal%5D)+AND+("
    # Keywords connectors
    p4 = "%5BTitle%5D+OR+"
    # Bridge to time range
    p5 = "%5BTitle%5D)+AND+(%22"
    # Time range connector
    p6 = "%2F"
    # Year, Month, Day
    p7 = str(t.year).zfill(2)
    p8 = str(t.month).zfill(2)
    p9 = str(t.day).zfill(2)
    # End
    p10 = "%22%5BDate+-+Publication%5D+%3A+%223000%22%5BDate+-+Publication%5D))"

    url = p1 + p2 + p3 + p4.join(keywords) + p5 + p7 + p6 + p8 + p6 + p9 + p10
    return url

# TODO: PubMed query example with corresponding url:
# (("Nature communications"[Journal]) AND (armadillo[Title] OR funny[Title]) AND ("2014/01/01"[Date - Publication] : "3000"[Date - Publication]))
# https://www.ncbi.nlm.nih.gov/pubmed/?term=((%22Nature+communications%22%5BJournal%5D)+AND+(armadillo%5BTitle%5D+OR+funny%5BTitle%5D)+AND+(%222020%2F01%2F29%22%5BDate+-+Publication%5D+%3A+%223000%22%5BDate+-+Publication%5D))

# TODO: find a solution for the 20 results limit

