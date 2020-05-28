from jnpr.junos.utils.config import Config
from jnpr.junos.utils.util import Util
from jnpr.junos import Device
import pyangbind.lib.pybindJSON as pybindJSON
#junos_routing_options is the class I generated from the YANG file created by running "show system schema module junos-conf-routing-options..." on a Junos device
from binding import openconfig_local_routing
from pprint import pprint
from lxml import etree
next_hop_table = (0,"10.10.0.1")

oc = openconfig_local_routing()
route = oc.local_routes.static_routes.static.add("8.8.8.8/32")
nh = route.next_hops.next_hop.add(next_hop_table[0])
conf = (pybindJSON.dumps(oc,mode="ietf"))
print conf


with Device(host='192.168.1.101',user='neteng',passwd='password123') as dev:
	with Config(dev, mode='exclusive') as cu:
		cu.load(path="vmx1.oc.bgp.conf",format="text")
		cu.pdiff()
		cu.rollback()
