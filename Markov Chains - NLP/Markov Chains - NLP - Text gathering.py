# Import package
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

def downloadWikiText(urls):
    text = ''
    for url in tqdm(urls):
        # Specify url of the web page
        source = urlopen(url).read()
        # Make a soup
        soup = BeautifulSoup(source,'lxml')
        # Extract the plain text content from paragraphs
        for paragraph in soup.find_all('p'):
            text += paragraph.text

        # Clean text
        text = re.sub(r'\[.*?\]+', '', text)
        text = text.replace('\n', '')
        # Append space for next text
        text += " "
    # Remove last " " and then save text as a file
    text = text[:-1]
    with open('wiki_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)

urls = ["https://en.wikipedia.org/wiki/Psychology",
        "https://en.wikipedia.org/wiki/Philosophy",
        "https://en.wikipedia.org/wiki/Sigmund_Freud"]
downloadWikiText(urls)