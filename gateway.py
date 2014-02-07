"""
Here is a simple polling based service gateway, between bluetooth and zeroconf

* The gateway maps EIDs from one protocol to the other and vice-versa
* Currently I am not setting the correct channel for the ELOC, because I am not implementing a proxy here
"""

from udiscovery import *
import time

supported = ['pybonjour', 'pybluez']
services = {}

while 1:
    srvs = discover_entities(supported)
    # bonjour -> bluetooth
    key = 'pybonjour'
    for EID in srvs[key].keys():
        for ELOC in srvs[key][EID]):
            # Pass channel here
            publish_entity(EID, protocols=['pybluez'])
    # bluetooth -> bonjour
    key = 'pybluez'
    for EID in srvs[key].keys():
        for ELOC in srvs[key][EID]):
            publish_entity(EID, protocols=['pybluetooth'])

    time.sleep(3)


