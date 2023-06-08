from lib2to3.pgen2.token import OP
from flask import Flask, render_template, request, url_for, send_file, redirect
from flask_wtf import FlaskForm
import wl
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import numpy as np
import pywt
from phe import paillier

a1, a2, a3, a4 = 0.1, 0.1, 0.1, 0.1

app = Flask(__name__)

hostname = "127.0.0.1"
port = 3306
username = "root"
password = "tsh1234"
database = "ustcuser"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset=utf8mb4"

db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/", methods=["POST"])
def login():
    get = request.form
    if len(get) == 2:
        [username, password] = list(get.values())
        with app.app_context():
            with db.engine.connect() as conn:
                sql = "select password from user where username='{0}'".format(username)
                rc = conn.execute(text(sql))
                c = rc.fetchone()[0]
                if c == password:
                    sql1 = "select email from user where username='{0}'".format(
                        username
                    )
                    rc1 = conn.execute(text(sql1))
                    e = rc1.fetchone()[0]
                    return render_template("homepage.html", name=username, email=e)
                else:
                    return render_template("login.html")
    if len(get) == 3:
        [username, password, email] = list(get.values())
        with app.app_context():
            with db.engine.connect() as conn:
                sql = "insert into user (username,password,email) values ('{0}','{1}','{2}')".format(
                    username, password, email
                )
                conn.execute(text(sql))
                conn.commit()
        return render_template("login.html")


@app.route("/uploadfile",methods=["POST"])
def uploadfile():
    return redirect("upload")


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/files", methods=["POST"])
def files():
    file = request.files
    pubkey=file["pubkey"]
    file1=file["file1"]
    file2=file["file2"]
    encryption=file["encryption"]
    pubkey.save("ReceiveFiles/pubkey.pub")
    file1.save("ReceiveFiles/file1.txt")
    file2.save("ReceiveFiles/file2.txt")
    encryption.save("ReceiveFiles/encryption.txt")
    return redirect("/download")

@app.route("/download")
def download():
    pubkey,Values=wl.seller_load_encryption("ReceiveFiles/encryption.txt",wl.seller_load_key("ReceiveFiles/pubkey.pub"))
    print(pubkey,len(Values))
    Lis=[649.7040244102334, 639.4410506082235, 599.4331619326099, 582.2821462672514, 612.938411415352, 600.1489784804095, 551.4952734879562, 539.2114449499393, 436.33995738979337, 414.9243456498143, 349.994727641788, 335.71578099151577, 420.5815253593843, 395.5190772203265, 337.1287608077278, 449.2752467412445]
    E_Lis=[pubkey.encrypt(x) for x in Lis]
    for i in range(len(Values)):
        E_Lis[i]=E_Lis[i]+Values[i]*a1
    with open("EncryptionResult/result.txt","w+") as f:
        f.write(wl.envec_dump_json(pubkey,E_Lis))
    #pub,V=wl.seller_load_encryption("EncryptionResult/result.txt",wl.seller_load_key("ReceiveFiles/pubkey.pub"))
    #pub,priv=wl.buyer_load_keypair("keys/publickey.pub","keys/privatekey.priv")
    #v=priv.decrypt(V[0])
    #print(v,priv.decrypt(Values[0]))
    #return "tsh"
    return send_file("EncryptionResult/result.txt",as_attachment=True)



if __name__ == "__main__":
    app.debug = True
    app.run()
