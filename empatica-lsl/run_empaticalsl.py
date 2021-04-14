import empaticalsl
import socket
import sys

TCP_IP = '000.0.0.0'
TCP_PORT = 5000
BUFFER = 4096

device_id = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

empaticalsl.connect(s, BUFFER, device_id, TCP_IP, TCP_PORT)

acc_enabled = False
bvp_enabled = True
gsr_enabled = True
ibi_enabled = True
hr_enabled = True
temp_enabled = True
batt_enabled = False

total_streams = acc_enabled + bvp_enabled + gsr_enabled + ibi_enabled + temp_enabled + batt_enabled
print('Should connect to %s streams' % total_streams)

empaticalsl.initial(s, BUFFER, device_id, acc_enabled, bvp_enabled, gsr_enabled, ibi_enabled, hr_enabled, temp_enabled, batt_enabled)

try:
    empaticalsl.stream(s, BUFFER, device_id, acc_enabled, bvp_enabled, gsr_enabled, ibi_enabled, hr_enabled, temp_enabled, batt_enabled)
except KeyboardInterrupt:
    empaticalsl.disconnect(s, BUFFER)
