import requests
import json

headers = {
        'content-type': "application/json",
        'x-apikey': "5a21f0dc3c4a8dc65b07c0fa28c9fde6d6342",
        'cache-control': "no-cache"
        }

def write():
    url = "https://kakakoin-8e1f.restdb.io/rest/blockchain-test"

    payload = json.dumps( {"data": "", "length":"0"} )

    response = requests.request("POST", url, data=payload, headers=headers)

    return(response.text)

def update(n):
    url = "https://kakakoin-8e1f.restdb.io/rest/blockchain-test/5a618ea120ff883600012180"

    data = [{"To":"Dvir", "From" : "Oren", "Amount": "150"}]
    strdata = json.dumps(n)
    strdata = strdata.replace("\"", "\\\"")
    payload = "{\"data\":\"" + strdata + "\"}"

    response = requests.request("PUT", url, data=payload, headers=headers)

    return(response.text)

def read():

    url = "https://kakakoin-8e1f.restdb.io/rest/blockchain-test"

    response = requests.request("GET", url, headers=headers)

    strr = str(response.text)
    jj = json.loads(strr)
    dd = json.loads(jj[0]["data"])

    return(dd)
