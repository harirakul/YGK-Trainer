from bs4 import BeautifulSoup as bs
import pandas as pd
import random, requests
import nltk
import colorama

import pathlib

try:
    nltk.data.find('./tokenizers/punkt.zip')
except:
    nltk.download('punkt', download_dir=f"{pathlib.Path().absolute()}")

from utilities import cprint, rmtfp, make_blank

colorama.init(convert = True)

class YGKPage:
    def __init__(self, url) -> None:
        self.url = url
        r = requests.get(url)
        self.soup = bs(r.content, "html.parser")
        self.paragraphs = self.soup.find("ul", {"class": "ygk"}).findAll("li")
        self.name = self.soup.find("h1").text
        self.get_descriptions()
        self.get_main_terms()
        self.get_vocab_terms()
        self.maindict = dict(zip(self.main_terms, self.descriptions))
        self.df = pd.DataFrame(self.maindict, index=[0]).T
        self.make_questions()

    def get_descriptions(self) -> list:
        self.descriptions = []
        for para in self.paragraphs:
            self.descriptions.append(bs(str(para), 'html.parser').text)
        return self.descriptions

    def get_main_terms(self) -> list:
        self.main_terms = []
        for para in self.paragraphs:
            self.main_terms.append(para.find("span", {"class": "label"}).text)
        return self.main_terms

    def get_vocab_terms(self) -> list:
        self.vocab_terms = []
        for para in self.paragraphs:
            terms = para.find_all("span", {"class": "ygk-term"}) + para.find_all("a", {"class": "ygk-term"})
            self.vocab_terms.extend([t.text for t in terms])
        return self.vocab_terms
    
    def describe(self, term: str) -> str:
        return self.df.loc[[term]][0][0]
    
    def locate_vocab(self, sent: str) -> dict:
        locs = {}
        for word in (self.vocab_terms):
            if word in sent:
                locs[word] = sent.index(word)
        return locs
    
    def make_questions(self) -> None:
        questions = {}
        for para in list(self.df[0]):
            for sent in nltk.sent_tokenize(para):
                locs = self.locate_vocab(sent)
                if len(locs) > 0:
                    n = random.randint(0, len(locs)-1)
                    words = list(locs.keys())
                    inds = list(locs.values())
                    q = make_blank(sent, inds[n], words[n])
                    questions[q] = words[n]
        self.questions = questions
        self.qdf = pd.DataFrame(self.questions, index=[0]).T
    
    def quiz(self):
        correct = 0; completed = 0
        q = list(self.questions.keys())
        a = list(self.questions.values())
        cprint(f"\n{'='*len(self.name)}", "blue")
        cprint(self.name, 'yellow')
        cprint(f"{'='*len(self.name)}\n", "blue")
        cprint(f"There are {len(q)} questions. Enter '<EXIT>' at anypoint to end session.\n", "cyan")
        for i in range(len(q)):
            ans = input(f"{q[i]}\nYOUR ANSWER: ")
            if ans.lower() == a[i].lower(): 
                cprint("Correct.\n", "green")
                correct += 1
            elif ans == '<EXIT>':
                break
            else: 
                cprint('Incorrect.', "red")
                print("The answer was", end=" "); cprint(f"{a[i]}.\n", "yellow")
            completed += 1
        cprint(f"All done. You received a score of {correct}/{completed}.", "cyan")

def play(url: str):
    YGKPage(url).quiz()

if __name__ == "__main__":
    play("https://www.naqt.com/you-gotta-know/mountains.html")
