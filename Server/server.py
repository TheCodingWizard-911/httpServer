#!/usr/bin/python

import socket
import sys
import threading
import datetime
import config

from requestHandler import Request
from requestMethods import Methods


class Server:

    serverPort = config.serverPort
    serverHost = "127.0.0.1"
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverHost, serverPort))
    serverSocket.listen()

    print("The Server is listening on port :", serverPort)

    clients = set()
    response = None

    def log(self, message):
        file = open("server.log", "a")
        file.write(message)

    def startServer(self):
        thread = threading.Thread(
            target=self.createClientConnection,
        )
        thread.start()

    def createClientConnection(self):

        while True:

            connectionSocket, address = self.serverSocket.accept()
            self.log(f"Connected To Client with address : {address}\n")
            self.log(f"The Connection Socket is : {connectionSocket}\t")
            self.log(f"At time : {str(datetime.datetime.now()).split()[-1]}\n")
            self.clients.add(connectionSocket)

            data = ""

            while True:
                recieved = connectionSocket.recv(1024).decode()
                data += recieved

                if not recieved.split("\r\n")[-2]:
                    break

            method = Request.parseRequest(Request, data)

            self.log(f"Received request : {Request.requestLine}\t")
            self.log(f"At time : {str(datetime.datetime.now()).split()[-1]}\n")

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
            self.log(f"Request {Request.requestLine} successfully completed\t")
            self.log(f"At time : {str(datetime.datetime.now()).split()[-1]}\n")
            if not config.persistantConnection:
                connectionSocket.close()
            else:
                try:
                    continue
                except KeyboardInterrupt:
                    break


if __name__ == "__main__":
    httpServer = Server()
    try:
        httpServer.createClientConnection()
    except KeyboardInterrupt:
        print("\nExiting Server...")
        sys.exit()
