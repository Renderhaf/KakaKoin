import os
from flask import Flask, render_template
from flask import request
from flask.json import jsonify
import json
import hashlib
import Userdb as udb
import BlockchainHashed
import BlockChainDB as bdb

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['HOST'] = 'localhost'

bch = BlockchainHashed.BCH()

print(bch.verifyBlockchain())

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['Type'] == "start":
            d = bch.userInfo(request.form["user"])
            return jsonify(d)
        if request.form['Type'] == "Transfer":
            usrs = udb.getUsers()
            if request.form["From"] in usrs:
                if request.form["To"] in usrs:
                    if request.form["DigSig"] == usrs[request.form["From"]][1]:
                        rdata = bch.newTransaction(request.form["To"],request.form["From"], float(request.form["Amount"]))
                        print(rdata)
                        return jsonify(rdata)
                    else:
                        return jsonify("Wrong Digital Signiture!")
                else:
                    return jsonify("Sorry,The User You are Sending to Doesnt Exist!")
            else:
                return jsonify("Sorry, The User You Are Sending From Doesnt Exist!")
    else:
        return render_template("KakaKoin.html") # Just page

@app.route("/Sign", methods=['GET', 'POST'])
def Sign():
    if request.method == 'POST':
        if request.form["Type"] == "Sign": # Signin
            usr = request.form["User"]
            pas = hashlib.sha256(request.form["Password"].encode('utf-8')).hexdigest()
            digsig = request.form["DigitalSig"]

            newtext = {usr: [pas,digsig]}
            #Read existing JSON file
            data = udb.getUsers()
            #Append the new entry onto Temporary variable
            if usr in data:
                return jsonify("User Already Exists")
            else:
                data.update(newtext)
                #Save new file
                udb.putUsers(data)

            return jsonify("Sign Up")
    else:
        return render_template("Signup.html")

@app.route("/Log", methods=['GET','POST'])
def Log():
    if request.method == 'POST':
        if request.form["Type"] == "log": # login
            usr = request.form["User"]
            pas = hashlib.sha256(request.form["Password"].encode('utf-8')).hexdigest()

            data = udb.getUsers()

            if usr in data:
                if data[usr][0] == pas:
                    return jsonify("Logged In")
                else:
                    return jsonify("Wrong Password")
            else:
                return jsonify("Username Doesnt exist")
    else:
        return render_template("Login.html")

@app.route("/Mine", methods=['GET','POST'])
def Mine():
    return render_template("Mine.html")

if __name__ == "__main__":
    port=os.environ.get('PORT') or 5000
    app.run(host='0.0.0.0', port=int(port))
