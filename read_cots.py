import time
#from time import sleep,gmtime,strftime
import os
import uuid
#from socket import getfqdn
import socket 

#import takcot as TC
from takpak.mkcot import mkcot
from takpak.takcot import takcot

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


print()
print("send a connect")
takserver.takflush()  # flush the xmls the server sends
#print(takserver.takread())  # read all the server CoT's, will send last + the connct

connect_xml = mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")
print("Connect XML is:")
print(connect_xml)

# send the connect string, server does not echo
takserver.taksend(mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")) 
# send the connect string, server does not echo

#time.sleep(5)
print("read the Connect response")
print(takserver.takread())  # read all the server CoT's, will send last + the connct

#print("Flush the server response")
#takserver.takflush()  # flush the xmls the server sends
#time.sleep(3)

#for i in range(10):
while True:
    print()

    print("wait for a server CoT")
    print(takserver.takread(readtimeout=10))
    time.sleep(0.1)

# Always need to close out the connection
# good practice to include reading anything the server pushed
# to prevent broken pipe errors on the server

#takserver.takflush()  # flush the xmls the server sends

print("Closing TAK Server")
takserver.takclose()
quit()


