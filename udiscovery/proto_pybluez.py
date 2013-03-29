"bluetooth protocol - using the Bluez"

from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
import uuid
import bluetooth
from .protocols import BaseProtocol

class PyBluezProtocol(BaseProtocol):
    """Pybluez Protocol

    * For the bluetooth protocol we publish an
    SDP service with the UUID generated from the hash
    * Entity identifiers are actually bluetooth MAC
    addresses (strings in PyBluez)
    """

    @staticmethod
    def find(uuid_id):
        """
        The bluetooth implementation searches for devices with
        services with the given uuid

        returns a list of MAC addresses i.e. the same as bluetooth.discover_devices()
        """
        result = []
        services = bluetooth.find_service(uuid=uuid_id.__str__())
        for svc in services:
            host = svc['host']
            result.append(host)
        return result

    @staticmethod
    def entity2uuid(entity_id):
        """
        Return all the UUIDs (i.e. SDP service-id) for the device with
        the given MAC
        """
        services = bluetooth.find_service(address=entity_id)
        return [ uuid.UUID(svc['service-id']) for svc in services if svc['service-id'] ]

    @staticmethod
    def publish(uuid_id):
        """
        Enable discovery of our bluetooth device via the given uuid
        """
        # FIXME:
        # * what do we do if the service is already published
        # * should we implement a service table with some locks?

        server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        server_sock.bind(("", bluetooth.PORT_ANY))
        server_sock.listen(1)
        bluetooth.advertise_service( server_sock,
                                    'Unified UUID Discovery',
                                    uuid_id.__str__() )

        return { 'socket' : server_sock, 'uuid' : uuid_id }

    @staticmethod
    def discover():
        """
        Discover nearby bluetooth devices

        returns a dict mapping mac addresses to uuid objects
        ie { <MAC addr> : [ uuid1, uuid2, ... ], ... }
        """
        result = {}
        services = bluetooth.find_service()
        # services with no service-id don't matter
        services = [ svc for svc in services if svc['service-id'] ]
        for svc in services:
            if not result.has_key( svc['host'] ):
                result[ svc['host'] ] = []

            result[ svc['host'] ].append( uuid.UUID(svc['service-id']) )

        return result


