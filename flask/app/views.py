from app import app

from netmiko import ConnectHandler
import re, json, time

tacacs_username = "francish"
tacacs_password = "ASDqwe123@@"

crc_threshold = 1000


def compre_threshold(crc_count):
    new_dict = {key: value for (key, value) in crc_count.items() if value >= crc_threshold }
    

    if len(new_dict) == 0:
        new_dict = "All counters below threshold"

    return new_dict



@app.route("/N5k/<sw_ip>")
def connect_n5k(sw_ip):
    device = ConnectHandler(device_type='cisco_nxos', ip=str(sw_ip), username=tacacs_username, password=tacacs_password)
    time.sleep(10)
    device.clear_buffer()
    output = device.send_command("sh int counters detailed all | incl Ethernet next 68 | exc s | exc o")

    device.disconnect()

    mod_out = ''.join(output.split()).replace('44.rxCRC=',' ').replace('--',' ')
    conv_out = mod_out.split(' ')
    
    convrt_dct = {conv_out[i]: conv_out[i + 1] for i in range(0, len(conv_out), 2)}
    dctvalue_int = {k:int(v) for k, v in convrt_dct.items()}


    dct_output = compre_threshold(dctvalue_int)

    fix_output = {
        "Switch Model": "N5k",
        "Switch MGT IP": sw_ip,
        "crc_error_count": dct_output
    }

    crc_json = json.dumps(fix_output, sort_keys=True)
    return crc_json

@app.route("/N7k/<sw_ip>")
def connect_n7k(sw_ip):
    device = ConnectHandler(device_type='cisco_nxos', ip=str(sw_ip), username=tacacs_username, password=tacacs_password)
    time.sleep(10)
    device.clear_buffer()
    output = device.send_command("sh int | egrep Ethernet|-chann|CRC | exc Ha | exc De")
    
    device.disconnect()

    rem_isupdown = re.sub(r'\s+is.*',r'',output).replace('\n','')
    rem_admindown = re.sub(r'\((\w+\s+){1,}\w+\)','',rem_isupdown)
    z = re.sub(r'\(\w+\)',r'',rem_admindown)
    rem_rntsgiants = re.sub(r'\d+\s+runts\s+\d+\s+giants\s+',r'',z)
    rem_nbffr = re.sub(r'(r)(E)',r'\1\n\2',rem_rntsgiants)
    rem_sspndd = re.sub(r'(r)(p)',r'\1\n\2',rem_nbffr)
    f = re.sub(r'\sCRC.*',r'',rem_sspndd)
    convrt_to_list = re.sub(r'\s+',r' ',f).strip().split(' ')

    convrt_dct = {convrt_to_list[i]: convrt_to_list[i + 1] for i in range(0, len(convrt_to_list), 2)}
    dctvalue_int = {k:int(v) for k, v in convrt_dct.items()}

    dct_output = compre_threshold(dctvalue_int)

    fix_output = {
        "Switch Model": "N7k",
        "Switch MGT IP": sw_ip,
        "crc_error_count": dct_output
    }

    crc_json = json.dumps(fix_output, sort_keys=True)
    return crc_json

@app.route("/F10/<sw_ip>")
def connect_f10(sw_ip):
    device = ConnectHandler(device_type='dell_force10', ip=str(sw_ip), username=tacacs_username, password=tacacs_password)
    time.sleep(10)
    device.clear_buffer()
    output = device.send_command("sh int | gr Gig|-cha|CRC | except part|Descr|Mini").replace('\n',' ')

    device.disconnect()
    
    a = re.sub(r'\sCRC,\s\d\s\w+,\s\d\s\w+','',output)
    b = re.sub(r'\sis\s\w+,(\s\w+){1,}','',a)
    c = re.sub(r'\((\w+\s+){1,}\w+\)','',b)
    d = re.sub(r'(\s+)(\d+\/)',r'\2',c)
    e = re.sub(r'(l)(\s+)(\d+)',r'\1\3',d)
    z = re.sub(r'CRC,\s\d*\s\w*,\s\d*\s\w*','',e)
    f = re.sub(r'\s+',' ',z).strip().split(' ')

    convrt_dct = {f[i]: f[i + 1] for i in range(0, len(f), 2)}
    dctvalue_int = {k:int(v) for k, v in convrt_dct.items()}

    dct_output = compre_threshold(dctvalue_int)

    fix_output = {
        "Switch Model": "F10",
        "Switch MGT IP": sw_ip,
        "crc_error_count": dct_output
    }


    crc_json = json.dumps(fix_output)
    return crc_json
