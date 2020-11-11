import socket
import sys
import os
import subprocess
import threading 
import math 

UDP_IP_ADDRESS = "192.168.1.2"
UDP_PORT_NO = 33001


# Function to find two's complement 
def findTwoscomplement(str): 
    n = len(str) 
  
    # Traverse the string to get first  
    # '1' from the last of string 
    i = n - 1
    while(i >= 0): 
        if (str[i] == '1'): 
            break
  
        i -= 1
  
    # If there exists no '1' concatenate 1  
    # at the starting of string 
    if (i == -1): 
        return '1'+str
  
    # Continue traversal after the  
    # position of first '1' 
    k = i - 1
    while(k >= 0): 
          
        # Just flip the values 
        if (str[k] == '1'): 
            str = list(str) 
            str[k] = '0'
            str = ''.join(str) 
        else: 
            str = list(str) 
            str[k] = '1'
            str = ''.join(str) 
  
        k -= 1
  
    # return the modified string 
    return str

def send_msg_charger(command,command_name,conv,pris):
	if conv == "1":
		subprocess.run(command,shell=True,stdout=subprocess.DEVNULL)
		while True:
			data, addr = serverSock.recvfrom(1024)
			print (data.hex())
			can_msg_type = data.hex()[0:2]
			# print (can_msg_type)
			# print ("Can ID of the charger :",data.hex()[2:10])
			print ("{}:{}".format(command_name,int(data.hex()[10:18],16)*pris))
			break
	if conv == '0':
		subprocess.run(command,shell=True,stdout=subprocess.DEVNULL)
		while True:
			data, addr = serverSock.recvfrom(1024)
			can_msg_type = data.hex()[0:2]
			n = int(data.hex()[10:26],16)
			print (n)
			bStr = ''
			while n > 0:
				bStr = str(n % 2) + bStr
				n = n >> 1
			res = bStr
			print ("{}:{}".format(command_name,res))
			# print ("{}:{}".format(command_name,int(data.hex()[10:18],16)*pris))
			break

def set_charger_val(voltage,current,can_id):
	print (voltage,current)
	voltage = float(voltage)*10
	voltage = hex(int(voltage))
	checksum_volt = hex(0xff-0x81-int('0x'+ str(voltage[2:3]),16)-int('0x'+ str(voltage[3:5]),16))
	n = int(checksum_volt,16)
	if (n<0):
		bStr = ''
		n = abs(n)
		while n > 0:
			bStr = str(n % 2) + bStr
			n = n >> 1
		res = bStr
		checksum_volt = findTwoscomplement(str(res.zfill(8)))
		decimal_representation = int(checksum_volt,2)
		checksum_volt = hex(decimal_representation)
	else:
		checksum_volt = checksum_volt
	print (str(checksum_volt[2:4]))
	a = "0x88100960{}1564000081{}{}{}"
	print (a.format(val,voltage[2:3].zfill(2),voltage[3:5].zfill(2),str(checksum_volt[2:4]).zfill(2)))
	subprocess.run("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100960{}1564000081{}{}{} -v 192.168.1.254;".format(val,voltage[2:3].zfill(2),voltage[3:5].zfill(2),str(checksum_volt[2:4]).zfill(2)), shell=True,stdout=subprocess.DEVNULL)

	current = float(current)*10
	current = hex(int(current))
	checksum_cur = hex(0xff-0x82-int('0x'+ str(current[2:3]),16)-int('0x'+ str(current[3:5]),16))
	n = int(checksum_cur,16)
	if (n<0):
		bStr = ''
		n = abs(n)
		while n > 0:
			bStr = str(n % 2) + bStr
			n = n >> 1
		res = bStr
		checksum_cur = findTwoscomplement(str(res.zfill(8)))
		decimal_representation = int(checksum_cur,2)
		checksum_cur = hex(decimal_representation)

	else:
		checksum_cur = checksum_cur
	print(str(checksum_cur[2:4]))
	a = "0x88100960{}1564000082{}{}{}"
	print (a.format(val,current[2:3].zfill(2),current[3:5].zfill(2),str(checksum_cur[2:4]).zfill(2)))
	subprocess.run("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100960{}1564000082{}{}{} -v 192.168.1.254;".format(val,current[2:3].zfill(2),current[3:5].zfill(2),str(checksum_cur[2:4]).zfill(2)), shell=True,stdout=subprocess.DEVNULL)


# os.system("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x8800000002{}00000000000000 -v 192.168.1.254; &> /dev/null".format(val))
# os.system("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100950{}1505000000000000 -v 192.168.1.254;".format(val))
# os.system("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100950{}1506000000000000 -v 192.168.1.254;".format(val))


'''val = input("Please enter the CAN ID: ")
if len(val) == 2:
	subprocess.run("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x8800000002{}00000000000000 -v 192.168.1.254;".format(val), shell=True,stdout=subprocess.DEVNULL)
else:
	print ("invalid CAN ID")
	sys.exit()


serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

while True:
	data, addr = serverSock.recvfrom(1024)
	# print (data.hex()) 
	can_msg_type = data.hex()[0:2]
	# print (can_msg_type)
	if (can_msg_type == "80"):
		# print ("Normal CAN Frame")
		print ("Can ID of the charger :",data.hex()[2:10])
	elif (can_msg_type == "88"):
		print ("Extended CAN Frame")
	break

read_charger = input("Press y to read charger data[Y/N]: ")

if read_charger == 'y':
	print ("Reading charger Data")
	send_msg_charger("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100950{}1505000000000000 -v 192.168.1.254;".format(val),"Charger output Voltage","1",0.010)
	send_msg_charger("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100950{}1506000000000000 -v 192.168.1.254;".format(val),"Charger output Current","1",0.010)
	send_msg_charger("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100950{}1507000000000000 -v 192.168.1.254;".format(val),"Charger input Voltage","1",0.10)
	send_msg_charger("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100950{}1502000000000000 -v 192.168.1.254;".format(val),"Charger input Current","1",0.010)
	send_msg_charger("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100950{}1514000000000000 -v 192.168.1.254;".format(val),"Alarm data 1","0",1)
	send_msg_charger("echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100950{}155a000000000000 -v 192.168.1.254;".format(val),"Alarm data 2","0",1)
else:
	print ("do not read charger")'''
val = 21

set_charger = input("Press y to set charger data[Y/N]: ")

if set_charger == 'y':
	print ("sending voltage and current commands")
	voltage = input("Voltage : ")
	current = input("current: ")
	set_charger_val(voltage,current,val)
else:
	print ("do not set charger")

while True:
	set_charger_again = input("Press y to set charger data again [Y/N]: ")

	if set_charger_again == 'y':
		print ("sending voltage and current commands")
		voltage = input("Voltage : ")
		current = input("current: ")
		set_charger_val(voltage,current,val)
	else:
		print ("do not set charger")
		break

# Turn off rectifier
#echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100920{}1564000084a500d6 -v 192.168.1.254;".format(val)
#turn on Rectifier
#echo naveencz12 | sudo sendip -p ipv4 -is 192.168.1.2 -p udp -us 31000 -ud 32000 -d 0x88100920{}156400008400007b -v 192.168.1.254;".format(val)









