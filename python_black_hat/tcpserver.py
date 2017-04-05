#!/usr/bin/python

import socket
import threading


def handle_client(client_socket):

    # print context of client
    request = client_socket.recv(1024)
    print("[*] Received: %s" % request)
    # response a data package
    client_socket.send("ACK")
    client_socket.close()


def start():
    bind_ip = "0.0.0.0"
    bind_port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    print("[*] Listening on %s:%d" % (bind_ip, bind_port))
    while True:
        client, addr = server.accept()
        print("[*] Accepted connection from: %s %d" % (addr[0], addr[1]))
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


if __name__ == "__main__":
    start()
