#!/usr/bin/python

import datetime
import mimetypes
import os
import socket
import sys
import threading
import time

serverName = "CN HTTP Server"
websiteRoot = "../Website/"


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
                    Methods, Request.requestURI, Request.requestVersion
                )

            elif method == "HEAD":

                self.response = Methods.headMethod(
                    Methods, Request.requestURI, Request.requestVersion
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


class Request:
    requestLine = None
    requestHeaders = None
    method = None
    requestURI = "/index.html"
    requestVersion = 1.1

    def parseRequest(self, request):

        lines = request.split("\r\n")
        self.requestLine = lines[0].split()
        self.requestHeaders = lines[1:]

        if len(self.requestLine) > 2:

            self.method = self.requestLine[0]
            self.requestURI = self.requestLine[1]
            httpInfo = self.requestLine[2].split("/")
            self.requestVersion = httpInfo[1]

        return self.method


class Methods:

    responseHeaders = None
    responseBody = None
    response = None

    statusCodes = {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        404: "Not Found",
    }

    currentStatus = 200
    version = 1.1

    currentDateTime = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S"
    )

    contentType = "text/html"
    contentLength = 0

    def createResponseHeaders(self):

        self.responseHeaders = f"HTTP/{self.version} {self.currentStatus} {self.statusCodes[self.currentStatus]}\r\n"
        self.responseHeaders += "Accept-Ranges: bytes\r\n"
        self.responseHeaders += f"Date: {self.currentDateTime} GMT\r\n"
        self.responseHeaders += f"Content-Type: {self.contentType}\r\n"
        self.responseHeaders += f"Server: {serverName}\r\n"
        self.responseHeaders += f"Content-Length: {self.contentLength}\r\n"
        self.responseHeaders += "\r\n"

        return self.responseHeaders

    def getMethod(self, uri, version):

        self.version = version

        fileName = uri.strip("/")

        if not fileName:
            fileName = "index.html"

        fileName = os.path.join(websiteRoot, fileName)
        self.contentType = mimetypes.guess_type(fileName)[0]

        try:
            fileEncoding = "utf-8" if (self.contentType == "text/html") else "latin1"
            file = open(fileName, "rb")
            self.responseBody = file.read().decode(fileEncoding)
            self.currentStatus = 200
            self.contentLength = len(self.responseBody)
            self.responseHeaders = self.createResponseHeaders(self)
            self.response = self.responseHeaders + self.responseBody

            return self.response
        except:
            return self.notFound(self)

    def headMethod(self, uri, version):

        self.version = version

        fileName = uri.strip("/")

        if not fileName:
            fileName = "index.html"

        fileName = os.path.join(websiteRoot, fileName)
        self.contentType = mimetypes.guess_type(fileName)[0]

        try:
            fileEncoding = "utf-8" if (self.contentType == "text/html") else "latin1"
            file = open(fileName, "rb")
            self.responseBody = file.read().decode(fileEncoding)
            self.currentStatus = 200
            self.contentLength = len(self.responseBody)
            self.responseHeaders = self.createResponseHeaders(self)
            self.response = self.responseHeaders

            return self.response
        except:
            return self.notFound(self)

    def putMethod(self, uri, version, connectionSocket):
        self.version = version

        fileName = uri.strip("/")

        if not fileName:
            fileName = "putData.text"

        fileName = os.path.join(websiteRoot, fileName)

        data = ""

        file = open(fileName, "w")

        while True:

            line = connectionSocket.recv(1024).decode()
            if not line.split("\r\n")[-2]:
                break
            data += line

        try:

            file.write(data)
            self.contentType = mimetypes.guess_type(fileName)[0]
            self.contentLength = len(data)
            self.contentStatus = 201
            self.responseHeaders = self.createResponseHeaders(self)

            self.response = self.responseHeaders

            return self.response

        except:
            pass

    def deleteMethod(self, uri, version):
        self.version = version

        fileName = uri.strip("/")

        if not fileName:
            fileName = "temp.txt"

        fileName = os.path.join(websiteRoot, fileName)

        data = ""

        try:
            os.remove(fileName)
            fileName = os.path.join(websiteRoot, "delete.html")
            self.contentType = mimetypes.guess_type(fileName)[0]
            file = open(fileName, "r")
            self.responseBody = file.read()
            self.currentStatus = 200
            self.contentLength = len(self.responseBody)
            self.responseHeaders = self.createResponseHeaders(self)
            self.response = self.responseHeaders + self.responseBody

            return self.response
        except:
            pass

    def badRequest(self):

        fileName = os.path.join(websiteRoot, "badRequest.html")
        self.contentType = mimetypes.guess_type(fileName)[0]
        file = open(fileName, "r")
        self.responseBody = file.read()
        self.currentStatus = 400
        self.contentLength = len(self.responseBody)
        self.responseHeaders = self.createResponseHeaders(self)
        self.response = self.responseHeaders + self.responseBody

        return self.response

    def notFound(self):

        fileName = os.path.join(websiteRoot, "notFound.html")
        self.contentType = mimetypes.guess_type(fileName)[0]
        file = open(fileName, "r")
        self.responseBody = file.read()
        self.currentStatus = 404
        self.contentLength = len(self.responseBody)
        self.responseHeaders = self.createResponseHeaders(self)
        self.response = self.responseHeaders + self.responseBody

        return self.response


if __name__ == "__main__":
    httpServer = Server()
    httpServer.createClientConnection()
