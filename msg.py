#import time
from time import sleep,gmtime,strftime
import socket
import os , sys
import uuid
import random

import sys


from takpak.takcot import takcot
from takpak.mkcot import mkcot

# Bail if not python 3 or later
if sys.version_info.major < 3:
    print("Must use python 3 or later")
    exit()

# select a server, default to local
server = input('Server? local is default, "FTS" or "DISCORD" uses those public servers: ')
if server == "FTS":
    TAK_IP = os.getenv('TAK_IP', '204.48.30.216')
    TAK_PORT = int(os.getenv('TAK_PORT', '8087'))
elif server == "DISCORD":
    TAK_IP = os.getenv('TAK_IP', '128.199.70.11')
    TAK_PORT = int(os.getenv('TAK_PORT', '48088'))
else:
    # use the local server for default
    TAK_IP = '172.16.30.30'
    TAK_PORT = 8087

print("Selected: " + TAK_IP + ":" + str(TAK_PORT))

# populate call and UID, can be overridden later
my_uid = str(socket.getfqdn())
my_call = my_uid
# Now add a UUID, without the time component
my_uid = my_uid + "-" + str(uuid.uuid1())[-12:]
my_call = my_call + "-" + my_uid[-4:]



# temporary user DB, allows for various users to spoof real clients
# This should be replaced with a proper DB based on reading server responses
# UID and callsign are critical. Team mainly matters if pushing things 
# to users that are not online. 
users=[
    [my_call,my_uid,"Cyan"]
    ,["All Chat Rooms 2","All Chat Rooms","Red"]
    ,["PINZ-2","ANDROID-355675081966541","Dark Green"]
    ,["PINZ-3","ANDROID-357752082829560","Dark Green"]
    ,["KM4BA","ANDROID-355675081966541","Purple"]
    ,["corvoTab","ANDROID-R52JB0CDC4E","Yellow"]
    ,["NOVA","ANDROID-359975090666199","Yellow"]
    ,["Predator hq","ef6b0e44-54d1-4922-bbbb-44becbfa7779","Yellow"]
    ,["REES-1","ANDROID-355028092385014","Red"]
    ,["OPERATOR WP4JMV","ANDROID-863134036519299","Blue"]
    ,["DA-B6","ANDROID-358211090479875","Orange"]
    ,["Aguililla","ANDROID-862892042639093","White"]
    ,["Hitman","ANDROID-358221090307778","Green"]
    ,["dB6","ANDROID-2b972fd9e3a7fb94","Red"]
    ,["Heltec 1","Heltec 1-6c626de49d52","Red"]
    ,["Mesh 2","Mesh 2-6c626de49d52","Red"]
    ]

# function to input a "user" for the message sender & recipient
# usertype only matters for the prompt
def get_user(usertype):
    for i in range(0,len(users)):
        print("User: " + str(i) + " " + users[i][0])
    user = ""
    while user == "":
        user = input("select the " + usertype +  " user or q to exit:") or 0
        if user == 0:
            break

        if user.upper() == "Q" or user == "\d":
            print("exiting")
            takserver.close
            exit()
        try:
            user = int(user)
            #if user >= len(users) or type(users) == str:
            if user >= len(users):
                print("Not a valid user, select 0-" + str(len(users)))
                user = ""
                continue
        except: 
            user = ""
            continue
    return(user)

# Open the server connection
takserver = takcot()
testsock = takserver.open(TAK_IP,TAK_PORT)

# Connect- now have to connect with a callsign
takserver.send(mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o", cot_callsign=my_call))
sleep(1)
takserver.flush()  # flush the xmls the server sends

# Main loop
while True:

    user = get_user('From')
    print("User " + users[user][0] + " selected")

    # Setup the sending user
    my_call = users[user][0]
    my_uid = users[user][1]
    my_team = users[user][2]
    print(my_uid)
    print(my_call)

    print()
    # Now get the recipient
    user = get_user('To')
    print("User " + users[user][0] + " selected")

    # assign their details- target_whatever is important for the msg CoT
    target_call = users[user][0]
    target_uid = users[user][1]
    target_team = users[user][2]

    print(target_uid)
    print(target_call)
    print(target_team) # Team does not matter for geochat

    print()
    msg_default = "Test from takpak"
    msg_default = strftime("%Y-%m-%d %H:%M:%SZ ", gmtime()) + msg_default
    target_msg = str(input("Enter the message: " + msg_default + ": ") or msg_default)
    #target_msg = strftime("%Y-%m-%d %H:%M:%SZ ", gmtime()) + message


    # Messages have a unique uid- critical
    event_uid = "GeoChat." + my_uid + "." + target_call + "." + str(uuid.uuid4())

    # Now build the message CoT
    cot_xml = mkcot.mkcot( 
        tgt_call=target_call
        , tgt_uid=target_uid
        , tgt_msg=target_msg
        # can be set as needed
        , cot_type="b-t-f" , cot_how="h-g-i-g-o", cot_typesuffix=""
        # takpak defaults are OK
        , cot_identity = "" ,  cot_dimension = ""
        , cot_id=event_uid
        # this differentiates the CoT as a message
        , sender_uid=my_uid
        , cot_callsign=my_call
        )

    print("Msg xml")
    print(cot_xml)
    print()

    takserver.flush()  # flush the xmls the server sends
    takserver.send(cot_xml)

    sleep(1)
    print("read the server response")
    print(takserver.read())
    print()




