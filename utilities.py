#Helper functions

colors = dict(
   PURPLE = '\033[95m',
   CYAN = '\033[96m',
   DARKCYAN = '\033[36m',
   BLUE = '\033[94m',
   GREEN = '\033[92m',
   YELLOW = '\033[93m',
   RED = '\033[91m',
   BOLD = '\033[1m',
   UNDERLINE = '\033[4m',
   END = '\033[0m',
)

def cprint(out: str, color: str) -> None:
    print(colors[color.upper()] + out + colors["END"])

def rmtfp(para: str) -> str:
    """"
    Removes the main term from the paragraph.
    """
    ind = str(para).index("span", str(para).index("span") + 1)
    return (para[ind + 6 :])

sent_tokenize = lambda passage: passage.split(".")

def make_blank(sent: str, ind: int, word: str) -> str:
    sub = "".join(["_" if i != " " else " " for i in word])
    return sent[0: ind] + sub + sent[ind + len(sub):]

if __name__ == "__main__":
    print(make_blank("Nice dude dude.", 5, "dude dude"))