from ncclient import manager
import json
from pprint import pprint
import lxml.etree as etree

username = "neteng"
passw = "password123"
with manager.connect(host="10.10.0.223", port=22,username=username,password=passw) as m:
	#junos_bgp_filter = '<configuration><protocols><bgp/></protocols></configuration>'
	#filter_tuple=('subtree',junos_bgp_filter)
	#c = m.get_config(source='running',filter=(filter_tuple)).data_xml
	var = m.rpc.get_route_summary_information().data_xml
        data = etree.fromstring(var)
	print(etree.tostring(data,encoding='unicode',pretty_print=True))

'''
with manager.connect(host="10.10.0.130", port=22,username=username,password=passw) as m:
	#eos_bgp_filter = '<network-instances><network-instance name="default"><protocols><protocol><bgp/></protocol></protocols></network-instance></network-instances>'
	eos_bgp_filter = '<network-instances><network-instance><name>default</name><protocols><protocol><name>BGP</name></protocol></protocols></network-instance></network-instances>'
	filter_tuple = ('subtree',eos_bgp_filter)
	c = m.get_config(source='running',filter=(filter_tuple)).data_xml
        data = etree.fromstring(c)
        print(etree.tostring(data,encoding='unicode',pretty_print=True))
'''
