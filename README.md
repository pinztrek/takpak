## Project title
# takpak
Python Library and sample code to create CoT's and send them to a TAK server
A little info about your project and/ or overview that explains **what** the project is about.

## Motivation
This library was created to allow the generation and push of CoT's to TAK servers. Goals:
* Do so in a way that does not break or put unusual loads on the servers. (ATAK client interaction with the server was the example followed)
* Allow the libraries to be used by themselves (inject a raw CoT, or build a CoT, but not inject)
* Work with current servers. Most of the existing code on the web was significantly out of date, and did not work or caused server issues. 

## Build status
The code is in funcitonal state, but continues to evolve/improve

## Features
The takpak library consists of two python3 classes:
* takcot.py- which interacts with the TAK server
    * takopen(ip_address, [port=ur_port_number]) Opens the socket to the server.
    * takclose() Closes out the session (Important for proper server interaction!)
    * taksend(cotdata) Sends a cot to the currently open server
    * takflush() Reads any pending data from the server, quietly ignores it
    * takread() Attempts read from the server, and returns it. Will loop readattempts times, and the timeout can be set. 
* mkcot.py

## Code Example
Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## Installation
Provide step by step series of examples and explanations about how to get a development env running.

## How to use?
If people like your project they’ll want to learn how they can use it. To do so include step by step guide to use your project.

## Contribute

Let people know how they can contribute into your project. A [contributing guideline](https://github.com/zulip/zulip-electron/blob/master/CONTRIBUTING.md) will be a big plus.

## Credits
While takpak is original code, it would not be possible without the multitude of tools and projects that provided insight into how TAK servers behave, and how to interact with them. This is primarily FreeTakServer (https://github.com/FreeTAKTeam/FreeTakServer) and ATAK/CIVTAK (https://www.civtak.org/). 

Push_cursor_on_target was a bit of inspiration. While quite old, and not functional for server use, it did provide one example of how CoT generation and sending to a client could be done. I chose a different direction for my code, as the CoT generation and server interaction are two separate libraries. 

CoT (Cursor on Target) format, definitions, etc are widely documented on the web and were invalable for understanding how to create a CoT. But blackbox reverse engineering of how the ATAK/CIVTAK client interacted via network traces and instrumentation was required to generate CoT's acceptible by modern servers.  

#### Anything else that seems useful

## License
A short snippet describing the license (MIT, Apache etc)

MIT © [Yourname]()
