# python-udiscovery 

udiscovery is a python library that abstracts device identification over different
discovery protocols. Basically it allows you determine that one device over bluetooth
and the same device over zeroconf, are in fact one and the same.

The end goal here to allow for applications to make smarter decisions when discovering
services, based on prior knowledge. And to authenticate devices based on public keys
when switching technologies.

## What can it do?

Right now we only support bluetooth (py-bluez) and zeroconf (using py-bonjour).
But plugins are easy enough to write, and contributions are always welcome.
The currently support plugins use:

* pybonjour for zeroconf
* pybluez for bluetooth

If you want to implement your own plugin for a different library, for one of
the already supported protocols keep the following in mind

### Bluetooth

* The EID is encoded as the service-id element


### Zeroconf

* The EID is encoded within the service TXT record


