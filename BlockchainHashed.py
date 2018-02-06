'''
#Instance Variablesm -- Later, these will be loaded through reading blockchain.txt
#For now, this will start with 3 blocks in it -- in production, it will contain the entire blockchain
blockchain = [{"To":3,"From":0,"Amount":1},{"To":5,"From":0,"Amount":5},{"To":5,"From":3,"Amount":0.15}]
'''
import hashlib
import BlockChainDB as bdb
import os

'''
A block is a dictionary
A block's basic structure is:
To - Reciever's Address
From - Sender's Address
Amount - Amount of whole Kakakoins to be sent in the transaction


Optionally, the block can be expanded to include "PreviousHash" and "Modifier", which are the hash of the previous block, and the modifier to make the hash of the current block start with "kaka"
the difficulty can be changed later by adding more letters, such as forcing the hash to start with "kakakakakaka"
'''

'''
Functions In This File:
test() - Tests all the functions in the program.
newTransaction(to,from,amount) - Adds a new transaction
countMoney() - Tallies up the total amount of kaka that every id has

'''


'''
IMPORTANT!
AT THE MOMENT, EVERY SINGLE FUNCTION IS CALLING bdb.read() AT THE BEGINNING. THIS IS INNEFICIENT.
EFFICIENCY CAN BE IMPROVED IF bdb.read() IS ONLY CALLED ONCE, AT THE BEGINNING OF THE FILE. (global variables?)
'''



'''
This is a function that tests all functions in this document
call this at the bottom if you want to test all functions in this program

This program changes the blockchain if modify = True, so only use this on a test blockchain
'''

class BCH:

    def __init__(self):
        self.blockchain = bdb.read()
        self.supply = 0

    # Adds a new transaction to the blockchain, including a very small amount of mining to secure the blockchain.
    # Returns either a success message or an error message as a string.
    def newTransaction (self,to,from_,amount):
        if amount < 0:
            return "ERROR : Transfer Amount Cannot Be Negative!"
        if(self.verifyBlockchain() == False):
            #Blockchain has been tampered with, don't make any new transactions
            return("ERROR: Blockchain Invalid - Transactions Disabled")

        if(from_ != 0):
            #Check that this person isn't overspending.
            if(self.countMoneyFor(from_) - amount < 0):
                return("ERROR: Not enough funds to complete this transaction!")

        if len(self.blockchain) != 0:
            lastBlockHash = hashlib.sha256(str(self.blockchain[len(self.blockchain)-1]).encode('utf-8')).hexdigest()
        else:
            lastBlockHash = ""
        block = {"PreviousHash":lastBlockHash,"To":to,"From":from_,"Amount":amount,"Modifier":""}

        #Find a modifier -- This is the small amount of mining.
        # with 5 zeros in the hash, it will take hundreds of thousands of guesses to get the correct hash. it will take about one second.
        while not(hashlib.sha256(str(block).encode('utf-8')).hexdigest().startswith("00000")):
            block["Modifier"] = hashlib.sha256(str(os.urandom(100)).encode('utf-8')).hexdigest()

        #from is a reserved word, so I use from_
        self.blockchain.append(block)
        bdb.update(self.blockchain)

        self.blockchain = bdb.read()
        return("Transaction completed successfullly!")

    #Returns an dictionary {"Username":Amount} of every single user on the blockchain
    def countMoney(self):
        balanceSheet = {}
        for i in self.blockchain:
            #Add users to the dictionary if they don't exist already
            if (not(i["To"] in balanceSheet.keys())):
                balanceSheet[i["To"]] = 0
            if (not(i["From"] in balanceSheet.keys())):
                balanceSheet[i["From"]] = 0

            if (i["To"] in balanceSheet.keys() and i["From"] in balanceSheet.keys()):
                balanceSheet[i["To"]] += i["Amount"]
                #Balancesheet at "To" += the amount transferred in the block
                balanceSheet[i["From"]] -= i["Amount"]
                #Balancesheet at "From" -= the amount transferred in the block

        #balanceSheet[0] = 0
        # ^ Omitting this line, since I'm using the negative balance of 0 in order to calculate the total kaka balance
        return balanceSheet


    #Returns an int of the current balance of a user
    #The balance should never be negative, but if it is, there are no checks.
    def countMoneyFor(self, username):
        #returns the balance for a specific Username
        cnt = 0
        for i in self.blockchain:
            #print(i)
            if (i["From"] == username):
                cnt -= i["Amount"]
            if (i["To"] == username):
                cnt += i["Amount"]
        return cnt


    #Returns a list of dictionaries, each dictionary is a short version of a block relating to the user.
    #Short versions of a block don't contain hashes.
    def returnHistory(self, username):
        out = []
        for i in self.blockchain:
            if (i["From"] == username):
                newDict = {"To":i["To"],"From":i["From"],"Amount":i["Amount"]}
                out.append(newDict)
            if (i["To"] == username):
                newDict = {"To":i["To"],"From":i["From"],"Amount":i["Amount"]}
                out.append(newDict)
        return out

    def verifyBlockchain(self):
        prevHash = ""
        for i in self.blockchain:
            if prevHash != i["PreviousHash"]:
                #print("Blockchain Doesn't Check Out!!")
                return False
            prevHash = hashlib.sha256(str(i).encode('utf-8')).hexdigest()
        if len(self.blockchain) > 0:
            if not(hashlib.sha256(str(self.blockchain[len(self.blockchain)-1]).encode('utf-8')).hexdigest().startswith("00000")):
                #Special statement for the last blocks
                return False
        return True


    #Returns a list containing [Length of the blockchain, total kakakoin in existence, balance of the user, [all blocks relating to the user]]
    def userInfo(self, username):
        return[len(self.blockchain),abs(self.countMoney()[0]),self.countMoneyFor(username),self.returnHistory(username)]


#test()
# print(bdb.read())
# print(newTransaction("Deez Nutz",0,23))
# print(newTransaction("UrMomGay",0,2.3))
# print(newTransaction("Mr. Krabs",0,99))
#
# print(newTransaction("Dvir",0,100))
# print(newTransaction("Dvir",0,100))
# print(newTransaction("Dvir",0,100))
# print(bdb.read())
