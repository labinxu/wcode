#!/usr/bin/python

import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def client_sender(buffer):
    print('client sender %s' % buffer)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)

        while True:
            # now waiting the response
            recv_len = 1
            response = ''
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print(response)

            # wait more receive
            buffer = raw_input('')
            buffer += '\n'
            client.send(buffer)
    except:
        print('[*] Exception! exit')
        client.close()


def server_loop():
    print('Server loop')
    global target
    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        # new client thread handler
        client_thread = threading.Thread(target=client_handler,
                                         args=(client_socket,))
        client_thread.start()


def client_handler(client_socket):
    global upload
    global execute
    global command
    print('client handler')
    if len(upload_destination):
        file_buffer = ''
        while True:
            data = client_socket.recv(1024)
            if not data:
                print('break while client handler')
                break
            else:
                file_buffer += data
        try:
            file_descripter = open(upload_destination, 'wb')
            file_descripter.write(file_buffer)
            file_buffer.close()

            client_socket.send('Successfully save file to %s\r\n'
                               % upload_destination)
        except:
            client_socket.send('Failed to save file to %s\r\n'
                               % upload_destination)

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        print('command mode')
        while True:
            client_socket.send('<cmdmode:#> ')
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                response = run_command(cmd_buffer)
                client_socket.send(response)


def run_command(command):
    # new line
    print('run_command: %s' % command)
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                         shell=True)
    except:
        output = 'Failed to execute command.\r\n'
    return output


def usage():
    print("BHP Net Tool\n")
    print('Usage server : python nc_demo.py -l -p 9999 -c')
    print("Usage client: python nc_demo.py -t localhost -p 9999 ")
    print("-l --listen - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given \
    file upon receiving a connection")

    print("-c --command - initialize a command shell")

    print("-u --upload=destination - upon receiving connection \
    upload a file and write to [destination]\n\n")

    sys.exit(0)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read command args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                                   ["help", "listen", "execute",
                                    "target", "port", "command", "upload"])

    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-c', '-command'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False, "Unhandled option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()

        client_sender(buffer)

    if listen:
        server_loop()


if __name__ == "__main__":
    main()
