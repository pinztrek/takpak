import time
#from time import sleep,gmtime,strftime
import os
import uuid
#from socket import getfqdn
import socket 
import math

#import takcot. Note this only works if you have installed the package
#   If you have not installed as a package, you may have to tune your imports
#   to be local to where your source is

from takpak.takcot import takcot
from takpak.mkcot import mkcot

#logging.basicConfig(level=logging.INFO) # level=10

sleeptime = 0.075
degrees=0

my_uid = str(socket.getfqdn())
my_call = my_uid
# Now add a UUID, without the time component
my_uid = my_uid + "-" + str(uuid.uuid1())[-12:]
my_call = my_call + "-" + my_uid[-4:]

# Example allows for various users to spoof real clients
users=[
    [my_call,my_uid,"Cyan"]
    ,["PINZ-2","ANDROID-355675081966541","Dark Green"]
    ,["KM4BA","ANDROID-355675081966541","Purple"]
    ]

for i in range(0,len(users)):
    print("User " + str(i) + " " + users[i][0])
user = ""
while user == "":
    try:
        user = int(input("select a user:") or 0)
    except:
        user = ""
        continue
    if user >= len(users) or type(users) == str:
        user = ""
    else:
        print("User " + users[user][0] + " selected")

# select a server, default to local

server = input('Server? local is default, "FTS" uses FTS Public: ')
if server == "FTS":
    TAK_IP = os.getenv('ATAK_IP', '204.48.30.216')
    TAK_PORT = int(os.getenv('ATAK_PORT', '8087'))
else:
    # use the local server for default
    TAK_IP = '172.16.30.30'
    TAK_PORT = 8087


#-----------------------------------------------------------------------------------------


# substantiate the class
takserver = takcot()

# Now open server
print("Opening TAK Server")
testsock = takserver.open(TAK_IP)

#print("open return is:")
#print(testsock)


#connect_xml=cot_xml
print()
print("send a connect")
takserver.flush()  # flush the xmls the server sends
#print(takserver.read())  # read all the server CoT's, will send last + the connct

# send the connect string, server does not echo
takserver.send(mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")) 

#print("read the Connect response")
#print(takserver.read())  # read all the server CoT's, will send last + the connct

print("Flush the server response")
takserver.flush()  # flush the xmls the server sends
time.sleep(1)

#for i in range(10):
while True:

    delta_lat=math.sin(math.radians(degrees))/4
    delta_lon=math.cos(math.radians(degrees))/4
    #print(str(degrees) + " " + str(delta_lat) + " " + str(delta_lon))

    print()
    print("send a cot")
    takserver.flush()  # flush the xmls the server sends
    #takserver.send(cot_xml)
    takserver.send(mkcot.mkcot(cot_identity="friend"
        , cot_stale = 1
        , cot_dimension="land-unit",cot_typesuffix="E-C-T"
        , cot_callsign=users[user][0] # spoof an active callsign
        , cot_id= users[user][1] # spoof an active uid
        , team_name = users[user][2] # spoof an active team
        , cot_lat=33.9 + delta_lat, cot_lon=-84.6 + delta_lon))
       # , cot_lat=33+i/20, cot_lon=-84+i/20))
    print()

    time.sleep(1)
    print("read the response")
    print(takserver.read())
    degrees=degrees+10
    if degrees >360:
        degrees = 0
    time.sleep(2)


time.sleep(5)

# Always need to close out the connection
# good practice to include reading anything the server pushed
# to prevent broken pipe errors on the server

#takserver.flush()  # flush the xmls the server sends

print("Closing TAK Server")
takserver.close()
