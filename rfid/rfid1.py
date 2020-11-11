from smartcard.Exceptions import CardConnectionException, NoCardException
from smartcard.System import *
from smartcard import util
from time import sleep

get_uid = util.toBytes("FF CA 00 00 00")
firmware = util.toBytes("FF 00 48 00 00")
picc_ope_par = util.toBytes("FF 00 50 00 00")
buzzer_off = util.toBytes("FF 00 52 00 00")
buzzer_on = util.toBytes("FF 00 52 FF 00")
read_block = util.toBytes("FF B1 00 05 04")
# alt_get_uid = [0xFF, 0xCA, 0x00, 0x00, 0x00] # alternative to using the helper

def get_readers():
	try:
		sc_readers = readers()
		reader = sc_readers[0] 
		return reader
	except Exception as e:
		reader = "NO READERS AVALIABLE"
		return reader

def get_firmware(command,asc_card):
	try:
		asc_card.connect()
		data, sw1, sw2 = asc_card.transmit(command)
		firmware = bytearray.fromhex((util.toHexString(data)).replace(" ","") + (util.toHexString([sw1, sw2])).replace(" ","")).decode()
		print("Scanning Card")
		print("FIRMWARE : {}".format(firmware))
	except Exception as e:
		print ("Please place the smart card")

def get_picc_ope_par(command,asc_card):
	try:
		asc_card.connect()
		data, sw1, sw2 = asc_card.transmit(command)
		print (util.toHexString(data))
		print (util.toHexString([sw1, sw2]))
	except Exception as e:
		print ("Please place the smart card")

def buzzer_control(command,asc_card):
	try:
		if command == "on":
			asc_card.connect()
			print ("turning on buzzer")
			data, sw1, sw2 = asc_card.transmit(buzzer_on)
			result = util.toHexString([sw1, sw2])
		else:
			asc_card.connect()
			print ("turning off buzzer")
			data, sw1, sw2 = asc_card.transmit(buzzer_off)
			result = util.toHexString([sw1, sw2])
	except Exception as e:
		print ("Please place the smart card")	
	
def read_block(command,asc_card):
	try:
		asc_card.connect()	
		data, sw1, sw2 = asc_card.transmit(command)
		print (data)
	except Exception as e:
		print (e)
		print ("Reading error")

while (1):
	reader = get_readers()
	if reader != "NO READERS AVALIABLE":
		con_reader = reader.createConnection()
		get_firmware(firmware,con_reader)
		read_block(read_block,con_reader)
		# get_picc_ope_par(picc_ope_par,con_reader)
		# buzzer_control("on",con_reader)
	else :
		print("NO RFID CARD DETECTED")
		print ("WAITING FOR 20S")
		sleep (10)
		reader = get_readers()
		print (reader)
		if reader == "NO READERS AVALIABLE":
			print("TERMINATING")
			exit()
		else:
			print("DETECTED")
	sleep(0.5)

