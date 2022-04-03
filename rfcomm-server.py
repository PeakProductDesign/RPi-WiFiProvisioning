# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import subprocess
import json

def is_json(mJson):
    try:
        json_object = json.loads(mJson)
        if isinstance(json_object, int):
            return False

        if len(json_object) == 0:
            return False
    except ValueError, e:
        return False
    return True

def setwifinetwork(ssid, password):
    commandline = "wpa_cli list_network | grep " + ssid 
    proc = subprocess.Popen(commandline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out, err) = proc.communicate()
    result = out.decode("utf-8")
    print(result)
    if len(result) > 0:
        cell = result.split('\t')
        commandline = "wpa_cli -i wlan0 select_network " + cell[0] 
        proc = subprocess.Popen(commandline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (out, err) = proc.communicate()
        print(cell)
    else:
        commandline = "wpa_cli -i wlan0 add_network"
        proc = subprocess.Popen(commandline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (out, err) = proc.communicate()
        result = out.decode("utf-8")
        result = result.split('\n')
        print(result)
        network_id = result[0]
        commandline = "wpa_cli -i wlan0 set_network " + network_id + " ssid " + "'\"" + ssid + "\"'"
        print(commandline)
        proc = subprocess.Popen(commandline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (out, err) = proc.communicate()
        print(out)
        commandline = "wpa_cli -i wlan0 set_network " + network_id + " psk " + "'\"" + password + "\"'"
        proc = subprocess.Popen(commandline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (out, err) = proc.communicate()
        print(out)
        commandline = "wpa_cli -i wlan0 select_network " + network_id
        proc = subprocess.Popen(commandline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (out, err) = proc.communicate()

        return out

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data[:-2])
        command = data[:-2]
        if is_json(command):
            json_data = json.loads(command)
            out = setwifinetwork(json_data["ssid"], json_data["pw"])
            client_sock.send(out)
        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (out, err) = proc.communicate()
            client_sock.send(out)
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
