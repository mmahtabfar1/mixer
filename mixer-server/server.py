#!/usr/bin/env python3
"""
Mixer:
an amateur music streamer using TCP and UDP sockets

@author Mahan Mahtabfar
03/21/20
"""
import os
import time
import glob
import socket


def getAudioData(song_name):

    #get the system path to the song file
    song_name = glob.glob(os.getcwd() + "/music/*" + song_name + "*")[0]

    print("Matching file found: ")
    print(song_name)
    audio_format = song_name[(song_name.index('.')+1):]
    print("Audio format: {}".format(audio_format))

    return (open(song_name, "rb"), os.stat(song_name).st_size)

if __name__ == "__main__":

    HEADERSIZE = 30
    IP = "192.168.1.191"
    TCP_PORT = 5764
    UDP_PORT = 9933

    #create a UDP socket to send the audio information
    sock_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #create the TCP socket to handle song requests
    sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_TCP.bind((IP, TCP_PORT))
    sock_TCP.listen(1)
    

    print("Mixer Server is UP and running at {} on port {}".format(IP,
        str(TCP_PORT)))
    print()

    while True:
        clientsocket, address = sock_TCP.accept()
        print("A connection with client {} has been established!".format(address))

        #receive the song request from the client
        header = clientsocket.recv(HEADERSIZE).decode("utf-8")

        msg_len = int(header.strip())

        song_request = clientsocket.recv(msg_len).decode("utf-8")

        print("A request for song {} was received!".format(song_request))

        #load song data and return to client
        data, size = getAudioData(song_request)

        #AF_INET = Ipv4
        #SOCK_DGRAM = UDP protocol

        #packets = [data[i:i+8192] for i in range(0, len(data), 8192)]
        num_packets = int((size/4096) + 1)

        #send ahead of time how many audio packets will be sent through UDP
        print("{} audio packets will be sent".format(str(num_packets)))
        clientsocket.send(bytes(str(num_packets), "utf-8"))

        #close the TCP socket
        clientsocket.close()


        #transmit packets through UDP
        time.sleep(0.35)
        for i in range(num_packets):

            sock_UDP.sendto(data.read(4096), ("192.168.1.179", UDP_PORT)) 
            time.sleep(0.00125)
        

        print(":: Served Client {} with Song Request: {}".format(address[0], song_request))
        print()

