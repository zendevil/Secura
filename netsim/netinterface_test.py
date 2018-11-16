#netinterface_test.py
from netinterface import network_interface
import network

interface1 = network_interface('interface1', 'prikshet')
interface2 = network_interface('interface2', 'andy')

#interface1.send_msg('interface2', b'some message')

print(read_msg('interface1prikshet/OUT'))
interface2.receive_msg()

