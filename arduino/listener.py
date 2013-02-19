import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dwiri.settings")

from django.core.management import setup_environ
from dwiri import settings
from manager.models import Node, DataStream, DataPoint
from time import gmtime, strftime
import serial

data_stream = tuple('address time analog_0 analog_1 analog_2 analog_3 analog_4 analog_5 checksum'.split(' '))
PAYLOAD_SIZE = 18

# Setup COM Port
ser = serial.Serial('COM3')

##for port in range(1, 10):
##    try:
##        ser = serial.Serial('COM' + str(port))
##    except serial.SerialException:
##        pass
##    else:
##        break

# Setup database connection
setup_environ(settings)

def message(text):
    print '[' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '] ' + str(text)

while True:
    # Wait until beginning of data character is detected
    while True:
        line = ser.readline()
        if line[0] == '~':
            break

    # Create data structure
    data = dict()
    for x in data_stream:
        data[x] = int(ser.readline().rstrip())

    # Calculate checksum
    checksum = PAYLOAD_SIZE
    for x in data_stream[:-1]:
        checksum ^= data[x] & 0xff
        checksum ^= (data[x] >> 8) & 0xff

    # Reject data if checksum not the same
    if checksum != data['checksum']:
        print 'Wrong checksum'
        continue

    try:
        node = Node.objects.get(address=data['address'])
    except Node.DoesNotExist:
        message('Node address ' + str(data['address']) + ' has not been registered')
        continue

    # Save last active
    node.save()

    datastreams = DataStream.objects.all()
    for datastream in datastreams:
        if datastream.inputpin not in data:
            continue

        datapoint = DataPoint.objects.create(raw_value=data[datastream.inputpin], node=node, stream=datastream)
        message(datapoint)
