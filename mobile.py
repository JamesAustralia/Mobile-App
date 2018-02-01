#_*_coding:utf8;_*_
#qpy:3
#qpy:console

# Instant Message GPS
# Apache 2.0 Licence

import os, time, datetime, pprint, random, smtplib, imaplib, imapclient, pyzmail, threading, shelve
#droid = sl4a.Android()

def mainMenu():
        print('\n''--MAIN MENU--''\n''____________________________________________''\n''1) Get location      ' '4) ----''\n' '2) Send command      ''5) ----' '\n' '3)                   ''6) ----''\n''\n''(q) Quit' '\n' '\n')
        choice = input('> ')
        if choice == '1':
                getGPS()
        if choice == '2':
                print('Sending message...')
                sendLoc()
        if choice == '3':
                print('Checking for instructions...')
                testn()
        if choice == '4':
                autoTest()                
        if choice == 'q':
                print('Quitting...')
                droid.exit()
        else:
            print('<INVALID CHOICE>')   
        mainMenu()
        

def getGPS():    
        global msg
        location = {'Latitude': -36.8703324, 'Longitude': 173.07934127, 'Zip': '2987'}
        long = location.get('Longitude', 0)
        latt = location.get('Latitude', 0) 
        msg.setdefault('Longitude', long)
        msg.setdefault('Latitude', latt)
        print(msg)
        mainMenu()


def MOBILEgetGPS():
        global msg
        location = droid.getLastKnownLocation().result
        pprint.pprint(location)
        location = location.get('gps') or location.get('network')    
        pprint.pprint(location)
        addresses = droid.geocode(location['latitude'], location['longitude'])
        postCode = addresses.result[0]['postal_code']
        print('Zip code: ' + postCode)
        print(type(postCode))
        long = location.get('longitude', 0)
        latt = location.get('latitude', 0)
        print(long, latt) 
        msg.setdefault('Longitude', long)
        msg.setdefault('Latitude', latt)
        msg.setdefault('Zip', postCode)
        print(msg)
        mainMenu()


def sendLoc():
        print('SEND EMAIL COMMAND')
        print('Using password: ' + PSK)
        responseBody = 'Subject: Task.\nInstruction received and completed.\nResponse:\n'
        tuple(msg)
        print(msg)
        responseBody += '\n' + PSK + ':\n' + str(msg)
        print('RESPONSE BODY')
        print(responseBody)
        print('Sending email now')
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(myEmail, myPSK)
        smtpObj.sendmail(myEmail, recipientEmail, responseBody)
        smtpObj.quit()
        print('\nMessage sent!''\n')
        print('Need to get a confirmation email back from the server.')
        mainMenu()
        
def getInstructionEmails():
        print(PSK)
        print('Getting new password''\n')
        imapCli = imapclient.IMAPClient(imapServer, ssl = True)
        imapCli.login(myEmail, myPSK)
        imapCli.select_folder('INBOX', readonly = True)
        instructions = []
        UIDs = imapCli.search(['FROM ' + myEmail, 'SUBJECT Confirmation.', 'UNSEEN'])
        rawMessages = imapCli.fetch(UIDs, [b'BODY[]'])
        print(UIDs)
        for UID in rawMessages.keys():
                message = pyzmail.PyzMessage.factory(rawMessages[UID][b'BODY[]'])
                if message.html_part != None:
                        body = message.html_part.get_payload().decode(message.html_part.charset)
                        print('HTML')
                if message.text_part != None:
                        print('Text')
                        body = message.text_part.get_payload().decode(message.text_part.charset)
                instructions.append(body)
        UIDs = imapCli.search(['SUBJECT Confirmation'])
        print(UIDs)
        #imapCli.delete_messages(UIDs)
        #imapCli.expunge()
        imapCli.logout()
        print(instructions)
        if instructions == []:
                print('instructions is the same as the last instructions file. Looking again')
                getInstructions()                
        if instructions != []:
                print('Found new password!''\n''---------------------')
                return instructions        


def parseInstructionEmail(instruction):
        print('Reading email for instructions')
        p=input('Create a safety barrier.., in case of spoof email from server resetting password, Only happens withing 60 seconds of sending the last GPS coordinates')
        global PSK
        lines = instruction.split('\n')
        print('lines')
        print(lines)
        print('\nChecking password...')
        for line in lines:
                print('line')
                print(line)
                if line.startswith('Password'):
                        print('Password CONFIRMED!')        
                        PSK = lines[1]
                        print('\nNew global password is: ' + PSK)
                        shelfFile = shelve.open('C:\\Users\\250gb NoSteam\\Desktop\\app\\password')
                        password = [PSK]
                        shelfFile['storage'] = password
                        shelfFile.close()
                        mainMenu()



def testn():
        instructions = getInstructionEmails()
        for instruction in instructions:
            parseInstructionEmail(instruction)
        time.sleep(1)
        mainMenu()


def getPSK():
        global PSK
        shelfFile = shelve.open('C:\\Users\\250gb NoSteam\\Desktop\\app\\password')
        for i in shelfFile.values():
                PSK = i[0]
        shelfFile.close()



myEmail = input('Enter email address: ')
myPSK = input('Enter email password: ')
imapServer = 'imap-mail.outlook.com'
smtpServer = 'imap-mail.outlook.com'

recipients = ['phishingtroller@hotmail.com']
msg = {}


print('\n---- MOBILE APP ----''\n''------------------''\n')
if PSK == '123456789012':
        print('Synchronise your device now''\n')
        sendLoc()

mainMenu()


