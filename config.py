'''
This application will take input from a text file and send it via serial to cisco router/switch.
'''
import serial
import sys
import time
import serial.tools.list_ports

import credentials

READ_TIMEOUT = 3


def read_serial(console):
    '''
    Check if there is data waiting to be read
    Read and return it.
    else return null string
    '''
    time.sleep(2)
    data_bytes = console.inWaiting()
    if data_bytes:
        return console.read(data_bytes)
    else:
        return ""


def check_logged_in(console):
    '''
    Check if logged in to router
    '''
    console.write("\r\n\r\n".encode())
    time.sleep(1)
    prompt = str(read_serial(console))
    if '>' in prompt or '#' in prompt:
        return True
    else:
        return False

def enable_needed(console):
    '''
    Check if enable password is needed
    '''
    console.write("\r\n\r\n".encode())
    time.sleep(1)
    prompt = str(read_serial(console))
    if '#' in prompt:
        return True
    else:
        return False



def login(console):
    '''
    Login to router
    '''
    login_status = check_logged_in(console)
    if login_status:
        print("Already logged in")
        return None

    print("Logging into device")
    while True:
        console.write("\r\n".encode())
        time.sleep(1)
        input_data = str(read_serial(console))
        print(input_data)
        if not 'Username' in input_data:
            continue
        console.write(credentials.username.encode() + "\n".encode())
        time.sleep(1)

        input_data = str(read_serial(console))
        if not 'Password' in input_data:
            continue
        console.write(credentials.password.encode() + "\n".encode())
        time.sleep(1)

        login_status = check_logged_in(console)
        if login_status:
            print("We are logged in\n")
            break
    enabled = enable_needed(console)
    print(enabled)
    if not enabled:
        console.write('enable'.encode() + "\n".encode())
        time.sleep(1)
        console.write(credentials.enable.encode() + "\n".encode())
        time.sleep(1)
    else:
        print('in Enable already')

def logout(console):
    '''
    Exit from console session
    '''
    print("Logging out from router")
    while check_logged_in(console):
        console.write("logout\n".encode())
        time.sleep(1)


    print("Successfully logged out from router")


def send_command(console, cmd=''):
    '''
    Send a command down the channel
    Return the output
    '''
    console.write(cmd.encode() + '\n'.encode())
    time.sleep(1)
    return read_serial(console)

def port_selection():
    i=1
    portlist ={}
    ports = list(serial.tools.list_ports.comports())
    for entries in ports:
        portlist.update({str(i): str(entries).split("-")})
        i += 1
    i=1
    print("Select from below:")
    for line in portlist:
        print(str(i) + " : " + portlist[line][0] + "-" + portlist[line][1])
        i += 1
    selection = input('Select number for COM Port :')
    comport = portlist[selection][0]
    return comport


def main():
    '''
    Testing using Python to interact to Cisco router via serial port
    '''

    maincomport = port_selection()

    test = "COM3"
    print("\nInitializing serial connection")

    console = serial.Serial(
        port=maincomport.strip(),
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=READ_TIMEOUT
    )

    if not console.isOpen():
        sys.exit()

    login(console)
    print(send_command(console, cmd='terminal length 0'))
    interfacelist = str(send_command(console, cmd='show ip int brief')).split('\\r\\n')
    interfacebrieflist = []
    for i in interfacelist[1:]:
        interfacebrieflist.append(i.split())

    for i in interfacebrieflist:
        print(i[0])
    print(interfacebrieflist[2][0])

    if 'FastEthernet0/1' in interfacebrieflist:
        print('WE got some 10/100 up in this place!')
    else:
        print('boo!')

    with open("data.txt", "r") as myfile:
        data = myfile.read()


    print(str(send_command(console, cmd=data + '\n' + "end")))



    logout(console)


if __name__ == "__main__":
    main()