import zephyrlsl
import bluetooth
import sys

socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

device_id = sys.argv[1]
address = '00:00:00:00:00:00'

zephyrlsl.connect(socket, address)

resp_enabled = True
ecg_enabled = True
acc_enabled = True
log_enabled = False
sum_enabled = False

total_streams = resp_enabled + ecg_enabled + acc_enabled + log_enabled + sum_enabled
print('Should connect to %s streams', total_streams)

zephyrlsl.initial(socket, resp_enabled, ecg_enabled, acc_enabled, log_enabled, sum_enabled)
try:
    zephyrlsl.stream(socket, address, resp_enabled, ecg_enabled, acc_enabled, log_enabled, sum_enabled)
except KeyboardInterrupt:
    zephyrlsl.disconnect(socket) 
