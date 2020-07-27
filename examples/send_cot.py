import time
#from time import sleep,gmtime,strftime
import os
import uuid
#from socket import getfqdn
import socket 

#import takcot. Note this only works if you have installed the package
#   If you have not installed as a package, you may have to tune your imports
#   to be local to where your source is

from takpak.takcot import takcot
from takpak.mkcot import mkcot

#logging.basicConfig(level=logging.INFO) # level=10

sleeptime = 0.075

TAK_IP = '172.16.30.30'
TAK_PORT = 8087

#TAK_IP = os.getenv('ATAK_IP', '204.48.30.216')
#TAK_PORT = int(os.getenv('ATAK_PORT', '8087'))

#-----------------------------------------------------------------------------------------


# substantiate the class
takserver = takcot()

# Now open server
print("Opening TAK Server")
testsock = takserver.takopen(TAK_IP)

#print("open return is:")
#print(testsock)


#connect_xml=cot_xml
print()
print("send a connect")
takserver.takflush()  # flush the xmls the server sends
#print(takserver.takread())  # read all the server CoT's, will send last + the connct

# send the connect string, server does not echo
takserver.taksend(mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")) 

#print("read the Connect response")
#print(takserver.takread())  # read all the server CoT's, will send last + the connct

print("Flush the server response")
takserver.takflush()  # flush the xmls the server sends
time.sleep(1)

for i in range(10):
    print()
    print("send a cot")
    takserver.takflush()  # flush the xmls the server sends
    #takserver.taksend(cot_xml)
    takserver.taksend(mkcot.mkcot(cot_identity="friend"
        , cot_stale = 1
        , cot_dimension="land-unit",cot_typesuffix="E-C-T"
        , cot_lat=33+i/20, cot_lon=-84+i/20))
    print()

    time.sleep(1)
    print("read the response")
    print(takserver.takread())


time.sleep(5)

# Always need to close out the connection
# good practice to include reading anything the server pushed
# to prevent broken pipe errors on the server

#takserver.takflush()  # flush the xmls the server sends

print("Closing TAK Server")
takserver.takclose()
