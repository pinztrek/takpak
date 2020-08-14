# Make CoT mkcot.py
#
# Assemble a proper CoT from inputs

__author__ = 'Alan Barrow <traveler@pinztrek.com>'
__copyright__ = 'Copyright 2020 Alan Barrow'
__license__ = 'GPL, Version 3+'

import uuid
import xml.etree.ElementTree as et
import socket
import logging
#import time
from time import sleep,time,gmtime,strftime

version = "1.1.0"


ID = {
    "pending": "p",
    "unknown": "u",
    "assumed-friend": "a",
    "friend": "f",
    "neutral": "n",
    "suspect": "s",
    "hostile": "h",
    "joker": "j",
    "faker": "f",
    "none": "o",
    "other": "x"
}
DIM = {
    "space": "P",
    "air": "A",
    "land-unit": "G",
    "land-equipment": "G",
    "land-installation": "G",
    "sea-surface": "S",
    "sea-subsurface": "U",
    "subsurface": "U",
    "other": "X"
}

datetime_strfmt = "%Y-%m-%dT%H:%M:%SZ"

my_uid = str(socket.getfqdn())
my_call = my_uid
# Now add a UUID, without the time component
my_uid = my_uid + "-" + str(uuid.uuid1())[-12:]
my_call = my_call + "-" + my_uid[-4:]


class mkcot:

    def mkcot(
         cot_stale=5, cot_how="m-g"
        , cot_lat=0 , cot_lon=0, cot_hae=9999999
        , cot_ce=9999999.0 , cot_le=9999999.0
        , cot_type="a" # a for atom, an actual event/thing. t used for pings, etc
        , cot_identity="other", cot_dimension="other"
        , cot_typesuffix="" #need to make a default
        , cot_id= my_uid # used to id a single CoT, could be sender UID, or event
        , cot_callsign= my_call
        , cot_ping= False
        , cot_os="1"   # Does not seem to matter, but is required for some CoT's
        , cot_platform=__name__  # Same as OS, sometimes required
        , cot_version=version
        , iconpath=""
        , color=""
        , team_name=__name__ , team_role="Team Member"
        , sender_uid=""
        , tgt_call=False
        , tgt_uid=False
        , tgt_msg=False
        ):
    
        # Get the current time and convert to CoT XML
        now_xml = strftime(datetime_strfmt,gmtime())


        # Add the stale time to the current time and convert to CoT XML
        stale=gmtime(time() + (60 * cot_stale))
        stale_xml = strftime(datetime_strfmt,stale)

        # If cot is a ping append "-ping" to UID
        if cot_ping:
            cot_id = cot_id + "-ping"

        if cot_identity:
            unit_id = ID[cot_identity]
            cot_typestr = cot_type +"-" + unit_id 
            if cot_dimension:
                cot_typestr = cot_typestr +"-" + DIM[cot_dimension]
        else:
            cot_typestr = cot_type # No unit, just go with basic type
   
        if cot_typesuffix:     
            # append the type suffix to the type string
            cot_typestr = cot_typestr + "-" + cot_typesuffix


        event_attr = {
            "version": "2.0",
            "uid": cot_id, # uid of the CoT, sender or event 
            "time": now_xml,
            "start": now_xml,
            "stale": stale_xml,
            "how": cot_how, 
            "type": cot_typestr
        }

        point_attr = {
            "lat": str(cot_lat),
            "lon":  str(cot_lon),
            "hae": str(cot_hae),
            "ce": str(cot_ce),
            "le": str(cot_le)
        }

        # now the sub-elements for the detail block
        if not tgt_call:
            precision_attr = {
                "altsrc": "GPS",
                "geopointsrc": "GPS",
            }
        else:
            precision_attr = None

        # if not a geochat we always have to include the contact block
        if not tgt_call:
            if cot_callsign:
                contact_attr = {
                    "endpoint": "*:-1:stcp",
                    "callsign": cot_callsign
                }
            else:
                contact_attr = { } # still have to include the block
                team_name = "" # No need for team if no callsign
        else:
            contact_attr = None
        

        if team_name and not tgt_call:
            # only use if the team is defined and it's not a geochat
            group_attr = {  
                "role": team_role,
                "name": team_name
            }
        else:
            group_attr = None
            

        if not tgt_call:
            platform_attr = {
                "os": cot_os, 
                "platform": cot_platform, 
                "version": cot_version
            }
        else:
            platform_attr = None


        if iconpath:
            icon_attr = {
                #"iconsetpath": '34ae1613-9645-4222-a9d2-e5f243dea2865/Military/soldier6.png'
                #"iconsetpath": '34ae1613-9645-4222-a9d2-e5f243dea2865/Military/soldier6.png'
                #"iconsetpath": 'f7f71666-8b28-4b57-9fbb-e38e61d33b79/Google/placemark_circle.png'
                "iconsetpath": iconpath
            }
        else:
            icon_attr = None

        if color:
            color_attr = { "argb": '-8454017' }
        else:
            color_attr = None


        # Geochat Attributes -----------------------------------------------
        chat_attr = {
            "parent": "RootContactGroup",
            "groupOwner": "false",
            "chatroom": tgt_call,
            "id": tgt_uid,
            "senderCallsign": cot_callsign
        }
    
        chatgrp_attr = {
            "uid0": sender_uid,
            "uid1": tgt_uid,
            "id": tgt_uid
        }

        link_attr = {
            "uid": sender_uid,
            "type": "a-f-G-U-C",
            "relation": "p-p"
        }

        remarks_attr = { # actual text is appended later as a "tail"
            #"source": "TAKPAK." + sender_uid,  # works, but shows as a different user, same call
            "source": "BAO.F.ATAK." + sender_uid, # the magic prefix are critical to spoof a user
            "to": tgt_uid,
            "time": now_xml,
        }

        serverdestination = {
            # Not clear on who this needs to be... but works coming from the server IP
            # Replace with server IP? Needed at all?
            "destinations": "172.16.30.30:4242:tcp:" + sender_uid
        }

        martidest_attr = {
            "callsign": tgt_call,
        }

        # Now assemble the element tree
        cot = et.Element('event', attrib=event_attr)

        et.SubElement(cot,'point', attrib=point_attr)

        # Create Detail element, save the handle
        detail = et.SubElement(cot, 'detail')

        # Now add some subelements to detail
        # Geochat has different required elements
        if tgt_call:  # target_call means a geochat
            chat = et.SubElement(detail,'__chat', attrib=chat_attr)
            et.SubElement(chat,'chatgrp', attrib=chatgrp_attr)
            et.SubElement(detail,'link', attrib=link_attr)

            # remarks block required
            remarks = et.SubElement(detail,'remarks', attrib=remarks_attr)
            remarks.text= tgt_msg # This is the actual message

            # serverdestination req'd
            et.SubElement(detail,'__serverdestination', attrib=serverdestination)

            #marti=et.SubElement(detail,'marti', attrib=marti_attr)
            marti=et.SubElement(detail,'marti')
            et.SubElement(marti,'dest', attrib=martidest_attr)


        if not cot_ping:
            # Add the contact block, needed except for pings
            if contact_attr:
                et.SubElement(detail,'contact', attrib=contact_attr)

            if precision_attr:
                et.SubElement(detail,'precisionlocation', attrib=precision_attr)

            if group_attr: # Don't include the block if set to "" as override
                et.SubElement(detail,'__group', attrib=group_attr)

            # takv/platform stuff needed for PLI's
            if platform_attr:
                et.SubElement(detail,'takv', attrib=platform_attr)

            # Optional icon/color
            if icon_attr:
                et.SubElement(detail,'usericon', attrib=icon_attr)
            if color_attr:
                et.SubElement(detail,'color', attrib=color_attr)


        # Prepend the XML header
        cot_xml = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + b'\n' + et.tostring(cot)
        #cot_xml = et.tostring(cot)
        #print(cot_xml)
        return cot_xml

