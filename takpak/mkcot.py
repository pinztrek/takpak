# build CoT
#
# Assemble a proper CoT from inputs

import uuid
import xml.etree.ElementTree as et
import socket
import logging
#import time
from time import sleep,time,gmtime,strftime

version = "1.0.0"


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
        , cot_id= my_uid, cot_callsign= my_call
        , team_name=__name__ , team_role="Team Member"
        ):
    
        # Get the current time and convert to CoT XML
        now_xml = strftime(datetime_strfmt,gmtime())


        # Add the stale time to the current time and convert to CoT XML
        stale=gmtime(time() + (60 * cot_stale))
        stale_xml = strftime(datetime_strfmt,stale)

        unit_id = ID[cot_identity]
    
        cot_typestr = cot_type +"-" + unit_id + "-" + DIM[cot_dimension]

        if cot_typesuffix:     
            # append the type suffix to the type string
            cot_typestr = cot_typestr + "-" + cot_typesuffix


        event_attr = {
            "version": "1.0",
            "uid": cot_id,
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

        precision_attr = {
            "altsrc": "GPS",
            "geopointsrc": "GPS",
        }

        if cot_callsign:
            contact_attr = {
                "endpoint": "*:-1:stcp",
                "callsign": cot_callsign
            }
        else:
            contact_attr = { } # still have to include the block

        group_attr = {
            "role": team_role,
            "name": team_name
        }
            

        platform_attr = {
            "OS": "29",
            "platform": __name__,
            "version": version
        }

        color_attr = {
            "argb": '-8454017'
        }

        icon_attr = {
            #"iconsetpath": '34ae1613-9645-4222-a9d2-e5f243dea2865/Military/soldier6.png'
            #"iconsetpath": '34ae1613-9645-4222-a9d2-e5f243dea2865/Military/soldier6.png'
            "iconsetpath": 'f7f71666-8b28-4b57-9fbb-e38e61d33b79/Google/placemark_circle.png'
        }
        remarks_attr = {
            "source": "APRS-Inject",
            "keywords": "APRS,KM4BA"
        }
    
        cot = et.Element('event', attrib=event_attr)
        et.SubElement(cot,'point', attrib=point_attr)
        #et.SubElement(cot, 'detail')
        # Create Detail element, save the handle
        #detail = et.SubElement(cot, 'detail', attrib=detail_attr)
        detail = et.SubElement(cot, 'detail')
        # Now add some subelements to detail
        et.SubElement(detail,'contact', attrib=contact_attr)
        et.SubElement(detail,'precisionlocation', attrib=precision_attr)
        if team_name: # Don't include the block if set to "" as override
            et.SubElement(detail,'__group', attrib=group_attr)
        et.SubElement(detail,'takv', attrib=platform_attr)
        #et.SubElement(detail,'color', attrib=color_attr)
        #et.SubElement(detail,'usericon', attrib=icon_attr)
        #et.SubElement(detail,'remarks', attrib=remarks_attr)

        # Prepend the XML header
        cot_xml = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + b'\n' + et.tostring(cot)
        #cot_xml = et.tostring(cot)
        #print(cot_xml)
        return cot_xml

