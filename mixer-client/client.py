#!/usr/bin/env python3
import io
import socket
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio


HEADERSIZE = 30
SERVER_ADDRESS = "192.168.1.191"
TCP_PORT = 5764
UDP_PORT = 9933


#TCP socket to send song requests
sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_TCP.connect((SERVER_ADDRESS, TCP_PORT))


#UDP socket to receive song requests
sock_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_UDP.bind(('', UDP_PORT))
sock_UDP.settimeout(0.5)


#sock.send() mehtod can be used to send inforamtion to the socket on the server
song_name = str(input("::> "))
song_request = f'{len(song_name):<{HEADERSIZE}}' + song_name
sock_TCP.send(bytes(song_request, "utf-8"))

#receive how man packets are going to be transmitted
num_incoming_packets = int(sock_TCP.recv(4096).decode("utf-8"))
print("There will be {} incoming packets".format(num_incoming_packets))


print(":: Receiving Music Data")
packets = []

for i in range(num_incoming_packets):
    try:
        packet, address = sock_UDP.recvfrom(4096)
    except socket.timeout:
        print(":: UDP socket timeout")
        break
    packets.append(packet)


print(":: Joining Audio Packets")
audio = b"".join(packets)


print(":: Playing audio with pydub")
audio = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
playback = _play_with_simpleaudio(audio)

input()

