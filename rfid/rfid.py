from smartcard.Exceptions import CardConnectionException, NoCardException
from smartcard.System import *
from smartcard import util
from time import sleep

while (1):
    try:
        sc_readers = readers()
        print(sc_readers[0])

        first_reader = sc_readers[0]
        print(type(first_reader))
        connection = first_reader.createConnection()

        get_uid = util.toBytes("FF CA 00 00 00")
        alt_get_uid = [0xFF, 0xCA, 0x00, 0x00, 0x00] # alternative to using the helper
        firmware = util.toBytes("FF 00 48 00 00")
    except Exception as e:
        print ("card pluged out")
        exit()
    try:
        # send the command and capture the response data and status
        connection.connect()
        data, sw1, sw2 = connection.transmit(firmware)

        # print the response
        uid_1 = util.toHexString(data)
        status = util.toHexString([sw1, sw2])
        uid = uid_1.replace(" ","") + status.replace(" ","")
        uid = bytearray.fromhex(uid).decode()
        print("Firmware = {}".format(uid))
        sleep (1)
    except NoCardException:
        print("ERROR: Card not present")

