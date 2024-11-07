import json
import requests
import csv
import re
import time

sentinelonekey = input("SentinelOne API Token? (refer to documentation to find out how to generate/regenerate one) ")
lenovokey = '' #left blank for corporate security reasons - this key is permanent, however it must be acquired via a dedicated lenovo sales rep which only really exist for large companies - one must fill out an application for the key to receive it

url_sentinelone = 'https://****.sentinelone.net/web/api/v2.1/agents?limit=1000&skipCount=true&machineTypes="laptop"'
s_headers = {'Authorization': f'Bearer {sentinelonekey}'}
r_sentinelone = requests.get(url_sentinelone, headers=s_headers)
sentinelone_list = r_sentinelone.json()
sentinelone_dictionary = (sentinelone_list["data"])

serial = []
models = {}
tapestry = []

def sentinelone():
    
    for x in sentinelone_dictionary:
        for k,v in x.items():
            if k == "serialNumber" and v != None and v[0].isalpha():
                serial.append(v)
    
    new_serial = list(set(serial))
    
    return new_serial

def lenovo():
    
    lenovo_list = []
    
    for x in serial:
        
        url_lenovo = f'http://supportapi.lenovo.com/v2.5/warranty?serial={x}'
        l_headers = {'ClientID': lenovokey}
        r_lenovo = requests.get(url_lenovo, headers=l_headers)
        lenovo_dictionary = r_lenovo.json()
        lenovo_list.append(lenovo_dictionary)
        
        for k,v in lenovo_dictionary.items():
            if k == "Product":
                if "LEGION" not in v:
                    word = (re.search(r'(?<=LAPTOPS/THINKPAD-).*?(?=-TYPE|/)', v).group(0)).replace("-", " ").title() #this will be where you ecounter the majority of bugs - refer to accompanying documentation or in Bookstack under the Guidebook page of the Inventory Update Assistant Book on the Software Documentation Shelf to learn more
                    if word == "T14":
                        word = "T14 Gen 1" #specifying "Gen 1" here for legibility at a glance
                else:
                    word = (re.search(r'(?<=LEGION-SERIES/).*?(?=-PRO)', v).group(0)).title()
                
                models.update({x: word})
    
    return lenovo_list, models

def weave():
    
    number = []
    product = []
    user = []
    usedby = []
    asset = []
    os = []
    tracker = [] 
    semi = []
    total = []
    
    for num in serial:
        for x in sentinelone_dictionary:
            if all(k in x for k in ("serialNumber", "computerName", "lastLoggedInUserName", "osName")):
                for k,v in x.items():
                    if v == num:
                        number.append(num)
                        for a,b in models.items():
                            if a == v:
                                product.append(b)
                        for y,z in x.items():                            
                            if y == "lastLoggedInUserName":
                                user.append(z.replace(".", " ").title())
                                usedby.append(z.lower() + "@****.com")
                            if y == "computerName":
                                asset.append(z)
                            if y == "osName":
                                os.append(z)
    
    #these print statements are meant for debugging purposes - if they do not produce the same number, a list index error will be generated and the script won't work    
    print("Serials:", len(number))
    print("Models:", len(product))
    print("Users:", len(user))
    print("Assets:", len(asset))
    print("Operating Systems:", len(os))
    
    for i in range(len(number)):
        if user[i] != 'Administrator' and user[i] != 'Apex IT' and user[i] != None and user[i] != '':
            temp = {'Name':asset[i], 'User':user[i], 'Used By':usedby[i], 'Asset Tag':asset[i], 'Product':product[i], 'Serial Number':number[i], 'OS':os[i], 'Asset State':'In Use'}
            semi.append(temp)
    
    #the previous for loop was producing tons of duplicates so I wrote this just to trim the fat - there is likely a way to rewrite the problem loop but that is a puzzle for not today (October 10th, 2024)
    for unique in semi:
        if unique not in tracker:
            total.append(unique)
    
    return total

def excel():
    
    field_names = ['Name', 'User', 'Used By', 'Asset Tag', 'Product', 'Serial Number', 'OS', 'Asset State']
    with open('C:/Windows/Temp/Inventory Update Assistant/Assets Update.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(tapestry)

#search function for testing and debugging purposes
def search():
    
    search = input("Search for user name, asset tag, model, serial number, or operating system? ")
    
    if search in ("Name", "name"):
        name = input("Name? ")
        for x in tapestry:
            for k,v in x.items():
                if v == name:
                    print(x)
                    
    if search in ("Asset Tag", "asset tag", "Asset", "asset", "Tag", "tag"):
        asset = input("Asset tag? ")
        for x in tapestry:
            for k,v in x.items():
                if v == asset:
                    print(x)
                    
    if search in ("Model", "model", "Product", "product"):
        model = input("Model? ")
        for x in tapestry:
            for k,v in x.items():
                if v == model:
                    print(x)
    
    if search in ("Serial Number", "serial number", "Serial", "serial", "Number", "number"):
        serial_num = input("Serial number? ")
        for x in tapestry:
            for k,v in x.items():
                if v == serial_num:
                    print(x)
                    
    if search in ("Operating System", "operating system", "Operating", "operating", "System", "system", "OS", "os"):
        os = input("Operating system? ")
        for x in tapestry:
            for k,v in x.items():
                if os in v:
                    print(x)

#debugging function is discussed in the Troubleshooting section of the Bookstack
def count():
    
    num = []
    temp = []
    
    for x in tapestry:
        for k,v in x.items():
            if k == "Serial Number":
                num.append(v)
                
    for x in serial:
        if x not in num:
            temp.append(x)
    
    print(temp)

def debug():
    
    bug = input("Debug? ")
    if bug in ("Yes", "yes", "Y", "y"):
        count()
    else:
        print("\nWow, okay, whatever. Jeez.\n")
        
    look = input("Would you like to perform a search? ")
    if look in ("Yes", "yes", "Y", "y"):
        search()
    else:
        print("\nWow man okay, I get it. I get it.\n\n\n\n\n *sobs*\n")
    
    end = input("Continue? ")
            
    while end in ("Yes", "yes", "Y", "y"):
        
        search()
        end = input("Continue? ")
        
    else:
        
        print("\nThanks for stopping by!\n")

def main():
    
    global serial
    global lenovo_list
    global tapestry
    
    serial = sentinelone()
    lenovo_list, models = lenovo()
    tapestry = weave()
    
    #below print statement is more debugging - length should be approximately equivalent to the number of internal employees at Apex Clean Energy
    print("Tapestry length:", len(tapestry))
    
    excel()
    debug()
    
    time.sleep(5)

main()
