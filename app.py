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
    cur.execute(f'SELECT * FROM correct')
    cordata = cur.fetchall()
    for cor in cordata:
        correct[cor[1]] = int(cor[2])
    # print(correct) 

    miss = []
    total = 0
    cur.execute(f'SELECT * FROM detect')
    detdata = cur.fetchall()
    for det in detdata:
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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)