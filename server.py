#imports
import socket               
import pickle

#this comment only exists on the develop branch

#server receive data from client and store it in list
#list is nested list
def storeData(data):
   maillist.append(data)
   print("FRAME RECEIVED: To " + data[2] + " From: " + data[1] + " Mail: " + data[3])

#server send data stored in list back to client
#search for data to send in nested list
#pickle that data and send it off to client
#delete the data that has been sent
def sendData(data):
   recipient = data[1]
   print("FRAME RECEIVED: From: " + data[1])
   found = False

   for sub_list in maillist:
      if recipient in sub_list:
         location = maillist.index(sub_list) 
         sublocation = sub_list.index(recipient)

         #if data found is in recipient location and not in sender or message
         if sublocation == 2:
            print("FOUND MAIL TO FORWARD")
            found = True
            print("FRAME TO SEND: To: " + maillist[location][sublocation] + " From: " + maillist[location][sublocation-1] + " Mail: " + maillist[location][sublocation+1])
            mail = maillist.pop(location)
            mail = pickle.dumps(mail)
            mail = bytes(f"{len(mail):<{HEADERSIZE}}", 'utf-8')+mail
            c.send(mail)
            break
   
   #user has no mail
   #pickle no mail data and send it to client
   if found == False:
      print("No Email")
      noMailList = ["No Email"]
      noMailList = pickle.dumps(noMailList)
      noMailList = bytes(f"{len(noMailList):<{HEADERSIZE}}", 'utf-8')+noMailList
      c.send(noMailList)

#headersizer and list
HEADERSIZE = 10
maillist = []

#socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345  
s.bind(('', port))

#listen
s.listen(5)
print ("Server is now listening at welcome socket")   

#accept 
c, addr = s.accept()      
print ('CONNECTED WITH CLIENT AT IP ADDRESSS', addr) 

#display menu and go to proper function based on index[0] of mail
choice = input("Do you want to keep the server open[y] or close it[n] ")
while choice == "y":

   #receive data, unpickle the list
   data = c.recv(1024)
   try:
      data = pickle.loads(data[HEADERSIZE:])
   except EOFError:
      continue
   
   #"M" means client is sending data
   if data[0] == "M":
      storeData(data)
   #"C" means client is checking data
   if data[0] == "C":
      sendData(data)

   choice = input("Do you want to keep the server open[y] or close it[n] ")
   if choice == "n":
      break
   
   #continue listening for connections
   s.listen(5)
   c, addr = s.accept() 
   print ('CONNECTED WITH CLIENT AT IP ADDRESSS', addr)      

#close server
c.close()