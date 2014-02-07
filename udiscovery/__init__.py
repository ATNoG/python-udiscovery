"""A unified discovery namespace implementation using UUIDs as device identifiers

"The force is like Duct Tape, it has a light side, a dark side
and it holds the universe together."
-- Circa unknown

"This pythonic library is like the force too: it binds stuff
together, hopefully the light side is facing out and the dark
side is kept hidden inside."
-- 'Me', while writing python

"""

from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
import uuid
from .protocols import PROTOCOLS

class DiscoveryException(Exception):
    "Base exception for all errors in this package"
    pass
class UnknownProtocol(DiscoveryException):
    "The supplied protocol does not exist"
    pass

def loc2entity(protocol, loc):
    """
    From a protocol specific identifier, determine a uuid

    * protocol: a protocol name
    * entity_id:

    Returns a list uuid objects
    """
    try:
        proto = PROTOCOLS[protocol]
    except KeyError:
        raise UnknownProtocol(protocol)
    return proto.entity2uuid(loc)


def entity2loc(uuid_id, protocols=PROTOCOLS.keys()):
    """Find entity from uuid

    * uuid_id: is the UUID we want to search for
    * protocols: is a list of protocol names, by default all
      protocols are used

    Returns a dictionary with a per protocol list
    of results
    """

    # convert uuid
    uuid_id = uuid.UUID(uuid_id)

    result = {}
    for proto in protocols:
        try:
            result[proto] = PROTOCOLS[proto].find(uuid_id)
        except KeyError:
            raise UnknownProtocol(proto)

    return result

def publish_entity(uuid_id, channel=None, protocols=PROTOCOLS.keys()):
    """Advertise our presence

    * key: public key that will be published
    * protocols: a list of protocols, all by default
    """
    # convert uuid
    uuid_id = uuid.UUID(uuid_id)

    res = {}
    for proto in protocols:
        res[proto] = PROTOCOLS[proto].publish(uuid_id, channel=channel)

    return res

def discover_entities(protocols=PROTOCOLS.keys()):
    """
    Discover nearby entities

    This function returns a tuple with two mappings:

    1. The first one maps protocols to entity ids to uuid objects
    2. The second maps uuids to tuples (protocol, entity id)
    """
    per_proto = {}
    for proto in protocols:
        try:
            per_proto[proto] = PROTOCOLS[proto].discover()
        except KeyError:
            raise UnknownProtocol(proto)

    per_uuid = {}
    for proto in protocols:
        for entity_id in per_proto[proto].keys():
            # uuid str as dict index
            for uuid_obj in per_proto[proto][entity_id]:
                uuid_str = uuid_obj.__str__()
                if not per_uuid.has_key(uuid_str):
                    per_uuid[uuid_str] = []

                per_uuid[ uuid_str ].append( (proto, entity_id) )

    return per_proto


DISCOVERY_PUBKEY_NAMESPACE = uuid.UUID('166266d3-a4b9-4886-9cb3-6d53d3928d68')

