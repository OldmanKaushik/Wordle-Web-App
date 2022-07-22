import flask
from flask import Flask, render_template, request

app = Flask(__name__)

import random
with open('WORDS.txt','r') as file:
    file = [i.strip() for i in file.readlines()]
word_loc = random.randint(0,len(file)-1) #randomly picks a word location
word = file[word_loc]

def validation(word):
    if len(word) != 5:
        print("does not meet length")
        return False
    elif word.isalpha() == False:
        print("There are symbols, other than letters in your input")
        return False
    else:
        return True

variables = ["word"+str(i) for i in range(1,7)]
iters = 0
@app.route('/')
def home():
    extra = flask.request.args.get("extra", "")
    ans = flask.request.args.get("ans", "")
    error = flask.request.args.get("error", "")
    no_of_att = flask.request.args.get("no_of_att","")
    return render_template('nytimes.html',extra=extra,ans=ans, variable=variables[iters], error=error, no_of_att=no_of_att)


@app.route('/wordcheck', methods=["POST"])
def wordcheck():
    global iters
    guess = request.form[variables[iters]]
    
    if validation(guess) == False:
        return flask.redirect(flask.url_for("home", error="Invalid form data, try again"))
    word_dic = {}
    word_dic2 = {}
    word_print = ""
    values = ""

    for new in range(len(word)):
        word_dic[word[new]] = 0
    for inc in range(len(word)):
        word_dic[word[inc]] += 1
                
    for new in range(len(guess)):
        word_dic2[guess[new]] = 0
    for inc in range(len(guess)):
        word_dic2[guess[inc]] += 1
                
    for j in range(len(guess)):
        word_print += guess[j] +"\t"
            
    for k in range(len(guess)):
        if guess[k] == word[k]:
                values += "'O'"
        else:
            if guess[k] in word:
                if word_dic2[guess[k]]> word_dic[guess[k]]:
                    values += "'X'"
                    word_dic2[guess[k]] -=1
                elif word_dic2[guess[k]] <= word_dic[guess[k]]:
                    values += "' '"
            else:
                values+="'X'"
    no_of_att = f"Number of attempts left: {5-iters}"
    if values== "'O''O''O''O''O'":
        return render_template("Victory.html", word=word)
    elif iters==5:
        return render_template("Endpage.html", word=word)
    else:
        print(values)
        iters +=1
        return flask.redirect(flask.url_for("home",extra=word_print, ans=values ,error="", no_of_att=no_of_att))

        
if __name__ == "__main__":
    app.run()

    
        
