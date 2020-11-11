#!/usr/bin/python

import socket
import sys
import threading
import time

from requestHandler import Request
from requestMethods import Methods


class Server:

    serverPort = int(sys.argv[1])
    serverHost = "127.0.0.1"
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverHost, serverPort))
    serverSocket.listen()

    print("The Server is listening on port :", serverPort)

    clients = set()
    response = None

    def startServer(self):
        thread = threading.Thread(
            target=self.createClientConnection,
        )
        thread.start()

    def createClientConnection(self):

        while True:

            connectionSocket, address = self.serverSocket.accept()
            print("Connected To Client at :", address)
            self.clients.add(connectionSocket)

            data = ""

            while True:
                recieved = connectionSocket.recv(1024).decode()
                data += recieved

                if not recieved.split("\r\n")[-2]:
                    break

            method = Request.parseRequest(Request, data)

            if method == "GET":

                self.response = Methods.getMethod(
                    Methods,
                    Request.requestURI,
                    Request.requestVersion,
                )

            elif method == "HEAD":

                self.response = Methods.headMethod(
                    Methods,
                    Request.requestURI,
                    Request.requestVersion,
                )

            elif method == "POST":

                self.response = Methods.postMethod(
                    Methods,
                    Request.requestURI,
                    Request.requestVersion,
                    connectionSocket,
                )

            elif method == "PUT":

                self.response = Methods.putMethod(
                    Methods,
                    Request.requestURI,
                    Request.requestVersion,
                    connectionSocket,
                )

            elif method == "DELETE":

                self.response = Methods.deleteMethod(
                    Methods,
                    Request.requestURI,
                    Request.requestVersion,
                )

            else:

                self.response = Methods.badRequest(Methods)

            connectionSocket.send(self.response.encode("latin1"))
            connectionSocket.close()


if __name__ == "__main__":
    httpServer = Server()
    try:
        httpServer.createClientConnection()
    except KeyboardInterrupt:
        print("\nExiting Server...")
        sys.exit()
