"""
A Bonjour plugin for python-discovery based on pybonjour

The operation of uuid discovery for Bonjour is slightly unnatural for
the following reasons:
1. Bonjour does not use UUIDs as common identifiers
2. One must always provide a service type for discovery procedures
3. Using UUIDs as device names would be unnatural and it would not
   solve (2)

Breaking this into the four core operations we get:


"""

from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
import select
from time import time
from .protocols import BaseProtocol
import pybonjour
import threading

SERVICE_TABLE = {}

def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
                    regtype, replyDomain):
    """
    This callback is invoked
    whenever a new service is added/removed
    """
    if errorCode != pybonjour.kDNSServiceErr_NoError:
        return

    if not (flags & pybonjour.kDNSServiceFlagsAdd):
        SERVICE_TABLE.pop(serviceName)
        return

#    if not UUIDS.has_key(uuid_id):


    resolved = []
    def callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                     hosttarget, port, txtRecord):
        """
        This is invoked when we finish resolving a service,
        i.e. a UUID
        """
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return

        uuid_id = txtRecord # FIXME: parse this please!!!
        SERVICE_TABLE[serviceName] = {'uuid':uuid_id,
                                        'host':hosttarget.rstrip('.'),
                                        'port':port}

    # Resolve service name
    resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                interfaceIndex,
                                                serviceName,
                                                regtype,
                                                replyDomain,
                                                callback)

    try:
        while not resolved:
            ready = select.select([resolve_sdRef], [], [], 5)
            if resolve_sdRef not in ready[0]:
                break
            pybonjour.DNSServiceProcessResult(resolve_sdRef)
        else:
            resolved.pop()
    finally:
        resolve_sdRef.close()

class DiscoveryAgent(object):
    """
    A discovery agent for Bonjour services
    """
    UUID_SRV_TYPE = '_uuid._tcp' # FIXME: change to _uuid and add udp

    def __init__(self):
        self.sdref = pybonjour.DNSServiceBrowse(regtype = self.UUID_SRV_TYPE,
                                          callBack = browse_callback)

    def discover(self, timeout=3):
        """
        Catch up with Bonjour events.

        This method advances event handling for bonjour
        """

        start = time()
        while time() < start + timeout:
            ready = select.select([self.sdref], [], [], timeout)
            for sd in ready[0]:
                pybonjour.DNSServiceProcessResult(sd)

    def __del__(self):
        if self.sdref:
            self.sdref.close()

    @staticmethod
    def run():
        """
        Blocking loop for the discovery agent
        """
        agent = DiscoveryAgent()
        while True:
            agent.discover(1)

#
# The discovery agent is created when the module is imported
# and called when needed

thread = threading.Thread(target=DiscoveryAgent.run)
thread.daemon = True
thread.start()

def publish_cb(self, sdref, flags, code, name, regtype, domain):
    if code != pybonjour.kDNSServiceErr_NoError:
        print('Error')

class PyBonjourProtocol(BaseProtocol):
    """PyBonjour Protocol"""


    @staticmethod
    def find(uuid_id):
        """
        The bonjour implementation searches for devices with services
        with the given uuid

        returns: a list of hostnames
        """
        result = []
        for srv in SERVICE_TABLE.values():
            if srv['uuid'] == uuid_id:
                result.append(srv['host'])

        return result

    @staticmethod
    def entity2uuid(entity_id):
        """
        Return all the UUIDs for the given hostname
        """
        result = []
        for srv in SERVICE_TABLE.values():
            if srv['host'] == entity_id.rstrip('.'):
                result.append(srv['uuid'])
        return result

    @staticmethod
    def publish(uuid_id, port=6666):
        """
        Enable discovery of our device via the given uuid
        """
        reg = DiscoveryAgent.UUID_SRV_TYPE
        print(type(uuid_id), type(reg), port)
        sdref = pybonjour.DNSServiceRegister(name=str(uuid_id), regtype=reg, port=port, callBack=publish_cb)

        return { 'socket' : sdref, 'uuid' : uuid_id }

        #raise NotImplemented

    @staticmethod
    def discover():
        """
        Discover nearby devices

        returns a dict mapping hostnames to uuid objects
        ie { <hostname> : [ uuid1, uuid2, ... ], ... }
        """

        result = {}
        for srv in SERVICE_TABLE.values():
            if not result.has_key(srv['host']):
                result[srv['host']] = []

            result[srv['host']].append(srv['uuid'])
        return result


