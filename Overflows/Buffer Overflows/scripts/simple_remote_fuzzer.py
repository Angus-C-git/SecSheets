#!/usr/bin/python3

import sys, socket
from time import sleep

"""

--> A Simple python3 remote server buffer overflow fuzzer

	-> Helps save time determining at what byte size a given buffer overflowe
	-> Tweak to your needs

"""



current_buffer = "A" * 100  # Arbitary inital buffer length --> Should be adapted on a scenario basis
target_ip = '192.168.0.0'  # Place holder host/target/remote server IP address
target_port = 9999  # Place holder host/target/remote server port number


while True:

	try:

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(('{target_ip}', target_port))  # Form socket connection to remote server

		sock.send(('RELEVANT SERVER COMMAND' + current_buffer))  # Add current test buffer size as an argument to fuzz desired command
		sock.close()
		sleep(1)  # Reduce load on remote server

		current_buffer = current_buffer + "A" * 100  # Index the buffer by another arbitary ammount

	except: 

		print("Fuzzing crashed at {} bytes".format(len(current_buffer)))
		sys.exit()