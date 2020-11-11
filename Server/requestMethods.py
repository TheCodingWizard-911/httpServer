import datetime
import mimetypes
import os
import random

serverName = "CN HTTP Server"
websiteRoot = "../Website/"


class Methods:

    responseHeaders = None
    responseBody = None
    response = None
    cookieValue = random.randint(1000, 10000)

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
        self.responseHeaders += f"Set-Cookie: cookie={self.cookieValue}\r\n"
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

    def postMethod(self, uri, version, connectionSocket):

        self.version = version

        fileName = uri.strip("/")

        data = ""

        while True:

            line = connectionSocket.recv(1024).decode()
            if not line.split("\r\n")[-2]:
                break
            data += line

        fileName = "post.html"

        fileName = os.path.join(websiteRoot, fileName)

        try:

            file = open(fileName, "r")
            self.responseBody = file.read()
            self.contentType = mimetypes.guess_type(fileName)[0]
            self.contentLength = len(self.responseBody)
            self.contentStatus = 200
            self.responseHeaders = self.createResponseHeaders(self)
            self.response = self.responseHeaders + self.responseBody

            return self.response

        except:
            pass

    def putMethod(self, uri, version, connectionSocket):
        self.version = version

        fileName = uri.strip("/")

        if not fileName:
            fileName = "putData.txt"

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
