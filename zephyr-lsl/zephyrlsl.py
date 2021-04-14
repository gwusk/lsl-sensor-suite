import bluetooth
from pylsl import StreamInfo, StreamOutlet
from zephyr.protocol import create_message_frame as cmf # see https://github.com/jpaalasm/zephyr-bt/blob/master/src/zephyr/protocol.py
import util # see https://github.com/pjg98/final-biomod-bt/blob/master/desktop_parser/util.py

def connect(socket, address):
    try: 
        socket.connect((str(address), 1))
        print("Connected to module at specified MAC address.")
    except bluetooth.BluetoothError:
        raise

def initial(socket, resp_enabled, ecg_enabled, acc_enabled, log_enabled, sum_enabled):
	
    init_message_log = cmf(0x01, [1, 0, 0, 0, 0, 100])
    init_message_ecg = cmf(0x16, [1])
    init_message_resp = cmf(0x15, [1])
    init_message_acc = cmf(0x1E, [1])
    init_message_sum = '\x02\xc2\x00\x00\x03'
    
    if resp_enabled:
        socket.send(init_message_resp)
    if ecg_enabled:
        socket.send(init_message_ecg)
    if acc_enabled:
        socket.send(init_message_acc)
    if log_enabled:
        socket.send(init_message_log)
    if sum_enabled:
        socket.send(init_message_sum)
        print('Requesting summary packet.')
    else:
        print("Error: Not subscribed to any streams")

	
def stream(socket, address, resp_enabled, ecg_enabled, acc_enabled, log_enabled, sum_enabled):
    
    print('Streaming...')
	
    if ecg_enabled:
        # ECG LSL outlet
        ecg_info = StreamInfo('ZephyrECG', 'ECG', 1, 250, 'float32')
        ecg_info.desc().append_child_value("manufacturer", "Zephyr")
        ecg_channels = ecg_info.desc().append_child("channels")
        ecg_channels.append_child("channel").append_child_value("label", "ECG").append_child_value("unit", "microvolts").append_child_value("type", "ECG")
        ecg_outlet = StreamOutlet(ecg_info, 12)
	
    if resp_enabled:
        # RESP LSL outlet
        resp_info = StreamInfo('ZephyrRESP', 'RESP', 1, 18, 'float32')
        resp_info.desc().append_child_value("manufacturer", "Zephyr")
        resp_channels = resp_info.desc().append_child("channels")
        resp_channels.append_child("channel").append_child_value("label", "RESP").append_child_value("unit", "microvolts").append_child_value("type", "RESP")
        resp_outlet = StreamOutlet(resp_info, 12)
	
    if acc_enabled:
        # ACC LSL outlet
        acc_info = StreamInfo('ZephyrACC', 'ACC', 3, 250, 'float32', 'Zephyr%s' % address)
        acc_info.desc().append_child_value("manufacturer", "Zephyr")
        acc_channels = acc_info.desc().append_child("channels")
        for c in ['X', 'Y', 'Z']:
            acc_channels.append_child("channel").append_child_value("label", c).append_child_value("unit", "g").append_child_value("type", "ACC")
        acc_outlet = StreamOutlet(acc_info, 12)  
    
    try:
        while True:
            data = socket.recv(1024)
            decoded_data = data.hex()
            
            stream_type = decoded_data[2:4]
            
            pay_len = 2*int(decoded_data[4:6],16)
            curr_payload = decoded_data[6:pay_len+6]
			
            if stream_type == '21': # RESP
                #timestamp = util.get_timestamp(curr_payload)
                sample_set = util.get_sample_set(curr_payload)
                sample_list = util.parser_10bit(sample_set)
                resp_outlet.push_chunk(sample_list)
                            
            if stream_type == '22': # ECG
                #timestamp = util.get_timestamp(curr_payload)
                sample_set = util.get_sample_set(curr_payload)
                sample_list = util.parser_10bit(sample_set)
                ecg_outlet.push_chunk(sample_list)
            
            if stream_type == '25': # ACC
                #timestamp = util.get_timestamp(curr_payload)
                sample_set = util.get_sample_set(curr_payload)
                sample_list = util.parser_acc(sample_set)
                acc_outlet.push_chunk(sample_list)
                
            socket.send('\x02#\x00\x00\x03')	#Prevents a connection timeout.
			
    except IOError:
        pass

def disconnect(socket):
    try:
        socket.close()
        print('Socket closed.')
    except:
        print('Error: socket cannot be closed.')
