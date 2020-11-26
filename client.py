#imports
import socket   
import pickle

#headersize
HEADERSIZE = 10

#when user chooses to send mail ask for destination, message,
#store information in a list beginning with "M" and pickle the list
#send the pickle and close the connection
def sendMail():
    destId  = input("Enter dest ID as a string ")
    message = input("Enter your message: ")
    mail = ["M", name, destId, message]
    mail = pickle.dumps(mail)
    mail = bytes(f"{len(mail):<{HEADERSIZE}}", 'utf-8')+mail
    print("FRAME TO SEND: to " + destId + " From: " + name + " Mail: " + message)
    s.send(mail)
    print("SENT: to " + destId + " From: " + name + " Mail: " + message)
    s.close()

#when user wants to check their mail
#create list object to send with "C"
#pickle list, send it
#receive pickled list back, unpickle it and display it
#close connection
def checkMail():
    #send request
    mail = ["C", name]
    mail = pickle.dumps(mail)
    mail = bytes(f"{len(mail):<{HEADERSIZE}}", 'utf-8')+mail
    print("FRAME TO SEND: From: " + name)
    s.send(mail)

    #receive data back
    recdata = s.recv(1024)
    recdata = pickle.loads(recdata[HEADERSIZE:])

    if recdata[0] == "No Email":
        msgrec = "No Email"
    else:
        msgrec = "To: " + name + " From: " + recdata[1] + " Mail: " + recdata[3]

    #print data received
    print("EMAIL RECEIVED: " + msgrec)

    s.close()

#create socket
s = socket.socket()          
port = 12345                

#get user name
name = input("Enter your ID as a string ")

#connection established 
s.connect(('127.0.0.1', port)) 
print("Connected to server")

#display menu and get input 
print("Enter 1-> Send Mail ")
print("Enter 2-> Check Mail ")
print("Enter 3-> Quit ")
choice = int(input("Enter your choice "))

if choice == 1:
    sendMail()
elif choice == 2:
    checkMail()
else:
    s.close()        