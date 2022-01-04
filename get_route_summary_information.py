from jnpr.junos import Device
from lxml import etree

with Device(host='10.10.0.223',password='password123',user='neteng',port=22) as dev:   
   xml_filter = '<route-summary-information><route-table><table-name>inet.0</table-name></route-table></route-summary-information>'
   var = dev.rpc.get_route_summary_information(table='inet.0')
   print(etree.tostring(var, encoding='unicode'))
