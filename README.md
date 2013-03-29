# python-udiscovery 

udiscovery is a python library that abstracts device identification over different
discovery protocols. Basically it allows you determine that one device over bluetooth
and the same device over avahi, are in fact one an the same.

The end goal here to allow for applications to make smarter decisions when discovering
services, based on prior knowledge.

## What can it do?

Right now we only support bluetooth (py-bluez) and zeroconf (using py-bonjour).
But plugins are easy enough to write, with some knowledge of python.


