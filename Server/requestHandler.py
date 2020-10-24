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
