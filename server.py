import os
from flask import Flask, render_template
from flask import request
from flask.json import jsonify
import json
import hashlib

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['HOST'] = 'localhost'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form["Type"] == "log":
            usr = request.form["User"]
            pas = hashlib.sha256(request.form["Password"].encode('utf-8')).hexdigest()

            with open('static/users.json') as f:
                data = json.load(f)

            if usr in data:
                if data[usr] == pas:
                    return jsonify("Logged In")
                else:
                    return jsonify("Wrong Password")
            else:
                return jsonify("Wrong Username")

        if request.form["Type"] == "Sign":
            usr = request.form["User"]
            pas = hashlib.sha256(request.form["Password"].encode('utf-8')).hexdigest()

            newtext = {usr: pas}
            #Read existing JSON file
            with open('static/users.json') as f:
                data = json.load(f)
            #Append the new entry onto Temporary variable
            if usr in data:
                return jsonify("User Already Exists")
            else:
                data.update(newtext)
                #Save new file
                with open('static/users.json', 'w') as f:
                    json.dump(data, f)

            return jsonify("Sign Up")
    else:
        return render_template("KakaKoin.html")

if __name__ == "__main__":
    port=os.environ.get('PORT') or 5000
    app.run(host='0.0.0.0', port=int(port))
