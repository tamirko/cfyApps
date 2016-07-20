# Fortinet plugin for Cloudify

The Fortinet plugin for Cloudify is an example, or template, of how an NFV plugin can be used in Cloudify.
It is functional but does not incorporate all (or even many) of the features of a Fortinet FortiGate appliance
but can be used for demo purposes in AWS and, in the near future, OpenStack.

The example blueprint within the plugin repository stands up an entire networked environment
 (using VPC in AWS, Neutron in OpenStack)
 and then adds in a FortiGate VM as a NAT router / firewall combination between
 an external (public) network and an an internal (private) network.
 It then, using the plugin, is configured to allow
 a test VM within the internal network to be accessible from the external network using firewall policies.
