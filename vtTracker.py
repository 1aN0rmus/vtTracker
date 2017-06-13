#!/usr/bin/python

'''
This is vtTracker! This tool will monitor specified VT notification URLs to track certain data.
@TekDefense
Ian Ahl | www.TekDefense.com | 1aN0rmus@tekDefense.com
Version: 0.1
'''

import re, sys, argparse, json, requests, sqlite3
# Adding arguments
parser = argparse.ArgumentParser(description='vtTracker will monitor specified VT notification URLs to track certain data')
parser.add_argument('-u', '--url', help='Specify the VT Notifications URL to pull notifications from')
parser.add_argument('-d', '--db', help='This option allows the user to set the name of the SQLLite database, if they do not like the default')
parser.add_argument('-r', '--rule', help='Query for a specific rule name. CASE-SENSITIVE')
parser.add_argument('-s', '--summary', action='store_true', default=False, help='Basic statistics')
parser.add_argument('-a', '--dumpall', action='store_true', default=False, help='This option will dump all rows to STDOUT')
args = parser.parse_args()

# declare some variables
vtNotDB = 'vtNotifications.db'
con = sqlite3.connect(vtNotDB)

# If the user wants to output the results to a file this will collect the name of the file and redirect all sys.stdout to that file
def outputMethod():
    if args.output:
        oFile = args.output
        print '[+] Printing results to file:', args.output
        o = open(oFile, "w")
        sys.stdout = o

# Get JSON objects  
def vtNotificationJSON(jsonURL):
        jsonPull = requests.get(jsonURL)
        jsonContent = jsonPull.content
        jsonParsed = json.loads(jsonContent)
        return jsonParsed

def json2DB(jaonParsed):
    insertNum = 0
    noNum = 0
    with con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS VTNOTDB(MD5 TEXT PRIMARY KEY, SHA256 TEXT, FIRST DATE, LAST DATE, NOTDATE TEXT, RULESET TEXT, RULE TEXT, AVPOSITIVES INTEGER, AVTOTALS INTEGER, SIZE INTEGER, FILETYPE TEXT)')
        con.commit()
    for key in jsonParsed['notifications']:
            md5 = key['md5']
            sha256 = key['sha256']
            first = key['first_seen']
            last = key['last_seen']
            notDate = key['date']
            ruleset = key['ruleset_name']
            rule = key['subject']
            avPositives = key['positives']
            avTotals = key['total']
            size = key['size']
            fileType = key['type']
            #jsonDic = {'md5': md5, 'sha256': sha256, 'first': first, 'last': last, 'notDate': notDate, 'ruleset': ruleset, 'rule': rule, 'avPositives': avPositives, 'avTotals': avTotals, 'size': size, 'fileType': fileType}
            try:
                cur.execute("INSERT INTO VTNOTDB(MD5, SHA256, FIRST, LAST, NOTDATE, RULESET, RULE, AVPOSITIVES, AVTOTALS, SIZE, FILETYPE) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (md5,sha256,first,last,notDate,ruleset,rule,avPositives,avTotals,size,fileType))
                con.commit()
                insertNum = insertNum+1   
            except:
                noNum = noNum+1 
    con.close()
    print '### UPDATE STATUS ###'
    print '[+] Samples added to DB: ' + str(insertNum)
    print '[+] Already in DB: ' + str(noNum)

def createDB():
    with con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS VTNOTDB(MD5 TEXT PRIMARY KEY, SHA256 TEXT, FIRST DATE, LAST DATE, NOTDATE TEXT, RULESET TEXT, RULE TEXT, AVPOSITIVES INTEGER, AVTOTALS INTEGER, SIZE INTEGER, FILETYPE TEXT)')
        con.commit()

def dumpAll():
    print 'MD5, SHA256, FIRST_SEEN, LAST_SEEN, NOTIFICATION_DATE, RULESET, RULE, AVHITS, AVTOTAL, SIZE, FILE_TYPE'
    with con: 
        cur = con.cursor()    
        cur.execute("SELECT * FROM VTNOTDB")
    while True:
        row = cur.fetchone()  
        if row == None:
            break   
        rowOut = str(json.dumps(row))[1:-1]
        print rowOut.replace('"', '')

def summary():
    with con:
        # Count of rule hits
        cur = con.cursor()
        cur.execute('SELECT RULE, COUNT(MD5) FROM VTNOTDB GROUP BY RULE')
        rows = cur.fetchall()
        num = 0
        print '### RULE STATS ###'
        for row in rows:
            num = num + row[1]
            print '[+] ' + row[0] + ': ' + str(row[1])
        print '[+] ' + str(num) + ' samples in this database!'
        # Count of file types
        cur.execute('SELECT FILETYPE, COUNT(MD5) FROM VTNOTDB GROUP BY FILETYPE')
        rows = cur.fetchall()
        num = 0
        print
        print '### FILETYPE STATS ###'
        for row in rows:
            num = num + row[1]
            print '[+] ' + row[0] + ': ' + str(row[1])

def ruleQuery(ruleName):
    with con:
        # Count of rule hits
        cur = con.cursor()
        cur.execute('SELECT MD5 FROM VTNOTDB WHERE RULE=?',(ruleName,))
        while True:
            row = cur.fetchone()  
            if row == None:
                break   
            rowOut = str(json.dumps(row))[1:-1]
            print rowOut.replace('"', '')
if args.db:
    vtNotDB = args.db
    con = sqlite3.connect(vtNotDB)
    createDB()

if args.url:
    jsonURL = args.url
    jsonParsed = vtNotificationJSON(jsonURL)
    json2DB(jsonParsed)

if args.dumpall:
    dumpAll()

if args.summary:
    summary()

if args.rule:
    ruleName = args.rule
    print '### Samples for ' + ruleName + ' ###'
    ruleQuery(ruleName)


