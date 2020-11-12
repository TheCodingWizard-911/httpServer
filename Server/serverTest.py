import sys
import Server.server as server

if __name__ == "__main__":
    httpServer = server.Server()
    try:
        httpServer.createClientConnection()
    except KeyboardInterrupt:
        print("\nExiting Server...")
        sys.exit()