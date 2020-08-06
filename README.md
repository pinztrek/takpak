# takpak
Python Library and sample code to create CoT's and send them to a TAK server

## Motivation
This library was created to allow the generation and push of CoT's to TAK servers. Goals:
* Do so in a way that does not break or put unusual loads on the servers. (ATAK client interaction with the server was the example followed)
* Allow the libraries to be used by themselves (inject a raw CoT, or build a CoT, but not inject)
* Work with current servers. Most of the existing code on the web was significantly out of date, and did not work or caused server issues. 

## Build status
The code is in funcitonal state, but continues to evolve/improve. Creating CoT's is solid, as is opening/closing/sending cots to a server. Reads are a bit kludgey. They work, but do not differentiate between multiple CoT's, and those which cross the readbuffer size. A better approach may be to return one cot or multiple cots as a list, and save the fragments for the next read. But that requires the class to be stateful. So for now, it's usable, but the calling code will need to check for valid cots and reassemble any fragments. 

The code should work with any TAK server that does not use authorization or certs as it emulates an ATAK/CIVTAK client. But has only been tested against FreeTakServer. 

## Features
The takpak library consists of two python3 classes:
* takcot.py- which interacts with the TAK server
    * takopen(ip_address, [port=ur_port_number]) Opens the socket to the server.
    * takclose() Closes out the session (Important for proper server interaction!)
    * taksend(cotdata) Sends a cot to the currently open server
    * takflush() Reads any pending data from the server, quietly ignores it
    * takread() Attempts read from the server, and returns it. Will loop readattempts times, and the timeout can be set. 
* mkcot.py
    * Builds common CoT's based on params
        * Position Reports of Users or points
        * Messages (geochat) to Users whether online or not
    * Note mkcot is not intended to be a full CoT generator. It is only populated for 
      common use cases as seen in ATAK


## Prerequisites
python 3.x. In fact, the libraries and code will give very non-intuitive "almost working" behavior sometimes under older pythons. Main development was on 3.8.

## Code Example
See the sample programs: 
* sendcot.py - pushes a CoT to the server. (may need some updates)
* circle.py- fly's a user in a circle around a point. Depends on an internal user DB for UID's
* readcots.py- Connects to the server, and prints CoT's the server publishes. Currently not breaking them apart yet. 
* takmsg.py- Connects to a server, and initiates a message to a user. Depends on a table of UID's, which would be replaced with a real DB in user code of UID's

All of the sample code should have keyboard interupt handlers added, as should some of the library code. But it works for now. 

## Installation
The best method is to save the source to something like /opt/takpak and then pip (or pip3) install from there. 

But if you want to have the package linked to the module source, you can use something like this from the top takpak directory:
* pip3 install -e .

Just remember that if you delete your source dir the module breaks

## How to use
See code examples for detail, but TL;DR is:<br/>
from takpak.mkcot import mkcot<br/>
from takpak.takcot import takcot<br/>

Then use the various methods:<br/>
-# substantiate the class<br/>
takserver = takcot()

-# Open the socket<br/>
testsock = takserver.takopen("172.16.30.30") # assumes port 8087, you can override

-# create a CoT (this is a really basic one to connect with)<br/>
cot_xml = mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")

-# then send a cot, the first one FTS interprets as a "Connection"<br/>
takserver.taksend(cot_xml) # again, many params you can override

-# Then read the result if interested<br/>
print(takserver.takread())  # read all the server CoT's, will send last several it has + the connect

-# close the connection when done to prevent errors on the server<br/>
takserver.takclose()

## Contribute

If you want to contribute please direct message/email me. I'll need a real email address or github account name, along with a short description of the project you are using it for. 

## Collaboration Approach
Please do not commit to the master branch without discussion. Ideally, we probably need to use the "Fork and Pull Request" model. (See https://reflectoring.io/github-fork-and-pull/ if not familiar). This will allow us to use pull requests and review before committing changes to the master. Alternatively, at least create your own dev branch. But this (I think) makes it a bit harder to tell when edits are ready to be integrated. 

## Credits
While takpak is original code, it would not be possible without the multitude of tools and projects that provided insight into how TAK servers behave, and how to interact with them. This is primarily FreeTakServer (https://github.com/FreeTAKTeam/FreeTakServer) and ATAK/CIVTAK (https://www.civtak.org/). 

Push_cursor_on_target (PCOT)was a bit of inspiration. While quite old, and not functional for server use, it did provide one example of how CoT generation and sending to a client could be done. I chose a different direction for my code, as the CoT generation and server interaction are two separate libraries. The ID and Dimension list definitions were used from their code, as there are only so many ways to capture a standard definitions like CoT uses in Python. The Element Tree method of building XML's that PCOT used also informed my code development. Again, there are only so many ways to efficiently create XMLS's in python.

CoT (Cursor on Target) format, definitions, etc are widely documented on the web and were invalable for understanding how to create a CoT. But blackbox reverse engineering of how the ATAK/CIVTAK client interacted via network traces and instrumentation was required to generate CoT's acceptible by modern servers.  

## License
This code is licensed under GPL3. Please note this means that any derivative code would need to be also released under the same license. 

GPL3 © Alan Barrow
