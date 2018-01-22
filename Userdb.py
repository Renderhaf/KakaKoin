import json
import requests

headers = {
        'content-type': "application/json",
        'x-apikey': "5a21f0dc3c4a8dc65b07c0fa28c9fde6d6342",
        'cache-control': "no-cache"
        }

def getUsers():
    url = "https://kakakoin-8e1f.restdb.io/rest/logs"

    response = requests.request("GET", url, headers=headers)

    strr = str(response.text)
    jj = json.loads(strr)

    return json.loads(jj[0]["data"])

def putUsers(d):
    url = "https://kakakoin-8e1f.restdb.io/rest/logs/5a643d1a20ff88360001687a"

    data = d
    strdata = json.dumps(data)
    strdata = strdata.replace("\"", "\\\"")
    payload = "{\"data\":\"" + strdata + "\"}"
    print(payload)

    response = requests.request("PUT", url, data=payload, headers=headers)

    return response.text
