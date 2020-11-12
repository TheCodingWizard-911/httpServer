import sys
import server

if __name__ == "__main__":
    httpServer = server.Server()
    try:
        httpServer.createClientConnection()
    except KeyboardInterrupt:
        print("\nExiting Server...")
        sys.exit()