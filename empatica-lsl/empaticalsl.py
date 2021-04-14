from pylsl import StreamInfo, StreamOutlet
import time

def connect(s, BUFFER, device_id, TCP_IP, TCP_PORT):

    # connect to port
    s.connect((TCP_IP, TCP_PORT))
    
    # get list of devices and connect to first device in list
#    LIST = 'device_list \r\n'.encode()
#    s.send(LIST)
#    
#    data = s.recv(BUFFER)
#    data_decoded = data.decode('ascii')
#    messages = data_decoded.split("\n")
#    message = messages[0]
#    data_array = [x.strip() for x in message.split(' ')]
#    device_id = data_array[4]
#    print(device_id)

    print('device_id: ', device_id)        
    connect_str = 'device_connect ' + device_id + ' \r\n'
    CONNECT = connect_str.encode()
    s.send(CONNECT)
    print_response(s, BUFFER)
        
        
def initial(s, BUFFER, device_id, acc_enabled, bvp_enabled, gsr_enabled, ibi_enabled, hr_enabled, temp_enabled, batt_enabled):
    # subscribe to stream then pause
	
    SUBSCRIBE_acc = 'device_subscribe acc ON \r\n'.encode()
    SUBSCRIBE_bvp = 'device_subscribe bvp ON \r\n'.encode()
    SUBSCRIBE_gsr = 'device_subscribe gsr ON \r\n'.encode()
    SUBSCRIBE_ibi = 'device_subscribe ibi ON \r\n'.encode()
    SUBSCRIBE_tmp = 'device_subscribe tmp ON \r\n'.encode()
    SUBSCRIBE_bat = 'device_subscribe bat ON \r\n'.encode()
    PAUSE = 'pause ON \r\n'.encode()
    
    if acc_enabled:
        s.send(SUBSCRIBE_acc)
        print_response(s, BUFFER)
        s.send(PAUSE)
        print_response(s, BUFFER)
    if bvp_enabled:
        s.send(SUBSCRIBE_bvp)
        print_response(s, BUFFER)
        s.send(PAUSE)
        print_response(s, BUFFER)
    if gsr_enabled:
        s.send(SUBSCRIBE_gsr)
        print_response(s, BUFFER)
        s.send(PAUSE)
        print_response(s, BUFFER)
    if ibi_enabled | hr_enabled:
        s.send(SUBSCRIBE_ibi)
        print_response(s, BUFFER)
        s.send(PAUSE)
        print_response(s, BUFFER)
    if temp_enabled:
        s.send(SUBSCRIBE_tmp)
        print_response(s, BUFFER)
        s.send(PAUSE)
        print_response(s, BUFFER)
    if batt_enabled:
        s.send(SUBSCRIBE_bat)
        print_response(s, BUFFER)
        s.send(PAUSE)
        print_response(s, BUFFER)
    else:
        print("Error: Not subscribed to any streams")


def stream(s, BUFFER, device_id, acc_enabled, bvp_enabled, gsr_enabled, ibi_enabled, hr_enabled, temp_enabled, batt_enabled):
    
    UNPAUSE = 'pause OFF \r\n'.encode()
    s.send(UNPAUSE)
    print('Streaming...')
	
    if acc_enabled:
        # ACC LSL outlet
        acc_info = StreamInfo('Empatica%sACC'% device_id, 'ACC', 3, 64, 'float32', 'Empatica%s' % device_id)
        acc_info.desc().append_child_value("manufacturer", "Empatica")
        acc_channels = acc_info.desc().append_child("channels")
        for c in ['X', 'Y', 'Z']:
            acc_channels.append_child("channel").append_child_value("label", c).append_child_value("unit", "g").append_child_value("type", "ACC")
        acc_outlet = StreamOutlet(acc_info, 12)  
    
    if bvp_enabled:
        # BVP LSL outlet
        bvp_info = StreamInfo('Empatica%sPPG'% device_id, 'PPG', 1, 64, 'float32', 'Empatica%s' % device_id)
        bvp_info.desc().append_child_value("manufacturer", "Empatica")
        bvp_channels = bvp_info.desc().append_child("channels")
        bvp_channels.append_child("channel").append_child_value("label", "PPG").append_child_value("unit", "absorption").append_child_value("type", "PPG")
        bvp_outlet = StreamOutlet(bvp_info, 12)
	
    if gsr_enabled:
        # GSR LSL outlet
        gsr_info = StreamInfo('Empatica%sEDA'% device_id, 'EDA', 1, 4, 'float32', 'Empatica%s' % device_id)
        gsr_info.desc().append_child_value("manufacturer", "Empatica")
        gsr_channels = gsr_info.desc().append_child("channels")
        gsr_channels.append_child("channel").append_child_value("label", "EDA").append_child_value("unit", "microsiemens").append_child_value("type", "EDA")
        gsr_outlet = StreamOutlet(gsr_info, 12)
        
    if ibi_enabled:
        # IBI LSL outlet
        ibi_info = StreamInfo('Empatica%sIBI'% device_id, 'IBI', 1, 1, 'float32', 'Empatica%s' % device_id)
        ibi_info.desc().append_child_value("manufacturer", "Empatica")
        ibi_channels = ibi_info.desc().append_child("channels")
        ibi_channels.append_child("channel").append_child_value("label", "IBI").append_child_value("unit", "seconds").append_child_value("type", "IBI")
        ibi_outlet = StreamOutlet(ibi_info, 12)
        
    if hr_enabled:
        # HR LSL outlet
        hr_info = StreamInfo('Empatica%sHR'% device_id, 'HR', 1, 1, 'float32', 'Empatica%s' % device_id)
        hr_info.desc().append_child_value("manufacturer", "Empatica")
        hr_channels = hr_info.desc().append_child("channels")
        hr_channels.append_child("channel").append_child_value("label", "HR").append_child_value("unit", "bpm").append_child_value("type", "HR")
        hr_outlet = StreamOutlet(hr_info, 12)
        
    if temp_enabled:
        # TEMP LSL outlet
        temp_info = StreamInfo('Empatica%sTEMP'% device_id, 'TEMP', 1, 4, 'float32', 'Empatica%s' % device_id)
        temp_info.desc().append_child_value("manufacturer", "Empatica")
        temp_channels = temp_info.desc().append_child("channels")
        temp_channels.append_child("channel").append_child_value("label", "TEMP").append_child_value("unit", "celsius").append_child_value("type", "TEMP")
        temp_outlet = StreamOutlet(temp_info, 12)
        
    if batt_enabled:
        # BATT LSL outlet
        batt_info = StreamInfo('Empatica%sBATT'% device_id, 'BATT', 1, 1, 'float32', 'Empatica%s' % device_id)
        batt_info.desc().append_child_value("manufacturer", "Empatica")
        batt_channels = batt_info.desc().append_child("channels")
        batt_channels.append_child("channel").append_child_value("label", "BATT").append_child_value("unit", "proportion").append_child_value("type", "BATT")
        batt_outlet = StreamOutlet(batt_info, 12)
	
    while True:
        data = s.recv(BUFFER)
        decoded_data = data.decode('ascii')
        messages = decoded_data.split("\n")
        
        for i in range(len(messages)-1):
            message = messages[i]
            data_array = [x.strip() for x in message.split(' ')]
        
            stream_type = data_array[0]
			
            if stream_type == 'E4_Acc':
                accx = float(data_array[2])
                accy = float(data_array[3])
                accz = float(data_array[4])
                #timestamp = float(data_array[1])
                acc_outlet.push_sample([accx, accy, accz])
            elif stream_type == 'E4_Bvp':
                bvp = float(data_array[2])
                #timestamp = float(data_array[1])
                bvp_outlet.push_sample([bvp])
            elif stream_type == 'E4_Gsr':
                gsr = float(data_array[2]) 
                #timestamp = float(data_array[1])
                gsr_outlet.push_sample([gsr])
            elif stream_type == 'E4_Temperature':
                temp = float(data_array[2])
                #timestamp = float(data_array[1])
                temp_outlet.push_sample([temp])
            elif stream_type == 'E4_Ibi':
                ibi = float(data_array[2])
                #timestamp = float(data_array[1])
                ibi_outlet.push_sample([ibi])
            elif stream_type == 'E4_Hr': # part of ibi subscribe
                hr = float(data_array[2])
                #timestamp = float(data_array[1])
                hr_outlet.push_sample([hr])
                print('heart rate (bpm): ',hr)
            elif stream_type == 'E4_Battery':
                batt = float(data_array[2])
                #timestamp = float(data_array[1])
                batt_outlet.push_sample([batt])
            else:
                print("message: ", message)
   
def disconnect(s, BUFFER):
    try:
        DISCONNECT = 'device_disconnect \r\n'.encode()  
        UNSUBSCRIBE = ['device_subscribe acc OFF \r\n'.encode(), 
                        'device_subscribe bvp OFF \r\n'.encode(),
                        'device_subscribe gsr OFF \r\n'.encode(),
                        'device_subscribe ibi OFF \r\n'.encode(),
                        'device_subscribe tmp OFF \r\n'.encode(),
                        'device_subscribe bat OFF \r\n'.encode()]
        PAUSE = 'pause ON \r\n'.encode()
        
        s.send(PAUSE)
        print("Stopping streams...")
        time.sleep(3)
        
        # unsubscribe from all the data streams
        for x in UNSUBSCRIBE:
            s.send(x)
            print_response(s, BUFFER)
        time.sleep(3)
        
        # disconnect from the Empatica BLE server 
        s.send(DISCONNECT)
        print_response(s, BUFFER)
        time.sleep(3)
        s.close()
        print('Socket closed.')
    except:
        print('Error: socket cannot be closed.')
        
def print_response(s, BUFFER):
    data = s.recv(BUFFER)
    decoded_data = data.decode('ascii')
    messages = decoded_data.split("\n")
    message = messages[0]
    print(message)