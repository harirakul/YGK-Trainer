from flask import Flask, render_template, request
from ygk import YGKPage
import json

app = Flask(__name__)

with open('subjects.json', 'rb') as f:
    d = json.load(f)

global p

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/play/<topic>')
def play(topic):
    global p
    p = YGKPage(f"https://www.naqt.com/{d[topic]}")
    q = list(p.questions.keys())
    a = list(p.questions.values())
    return render_template('quiz.html', title=p.name, topic = topic, q = q, a = a)

@app.route('/results/<topic>', methods=['GET', 'POST'])
def eval(topic):
    global p
    #p = YGKPage(f"https://www.naqt.com/{d[topic]}")
    q = list(p.questions.keys())
    a = list(p.questions.values())
    results = []
    for i in range(len(request.form)):
        if request.form.get(list(request.form.keys())[i]).lower() == a[i].lower():
            results.append(1)
        else: results.append(0)
    
    score = f"{results.count(1)}/{len(results)}"
    classes = ["correct" if i == 1 else "wrong" for i in results]

    return render_template('results.html', 
                            topic = topic, 
                            score = score, 
                            classes = classes,
                            q = q, 
                            a = a, 
                            results = results)

if __name__ == "__main__":
    app.run()