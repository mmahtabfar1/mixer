# Mixer a simple music streaming app written in python

I had a bunch of mp3 files from my favorite artist on my computer and I thought
it would be a good idea and educational experience to stream them over to my laptop using my raspberry pi.
I had to do something during the quarantine :/

## Overview
I built this using python's sockets API.
Clients make TCP requests for the song name to the server which then streams
music over to them over UDP.
