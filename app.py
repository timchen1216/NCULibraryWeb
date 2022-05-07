import sqlite3
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

#主頁
@app.route("/")
def index():
    return render_template("index.html")
# 檢查操作
@app.route("/detectdata")
def detectdata():
    con = sqlite3.connect('LibraryWeb.db')
    cur = con.cursor()

    correct = {}
    for cor in cur.execute(f'SELECT * FROM correct'):
        correct[cor[1]] = int(cor[2])
    # print(correct)

    miss = []
    total = 0
    for det in cur.execute(f'SELECT * FROM detect'):
        # print(correct[det[1]])    
        if correct[det[1]] != int(det[2]):        
            total += 1
            number, dp, cp = det[1], det[2], correct[det[1]]
            m = [number, dp, cp]
            miss.append(m)    

    for mis in miss:
        cur.execute(f"INSERT INTO miss (`number`, `dp`, `cp`) VALUES ('{mis[0]}','{mis[1]}','{mis[2]}')")
    
    con.commit()
    con.close()

    return render_template("check.html",miss = miss, total = total)
app.run()