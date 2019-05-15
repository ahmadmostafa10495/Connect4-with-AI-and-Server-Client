
import socket


def server_program():
    # get the hostname
    file = open("ServerConfig.txt",'r')
    host = file.readline()
    host = host[:len(host)-1]
    #print(host)
    port = int(file.readline())  # initiate port no above 1024
    #print(port)
    file.close()
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    conn2, address2 = server_socket.accept()
    print("Connection from: " + str(address))
    print("Connection from: " + str(address2))
    data = "0"
    conn.send(data.encode())
    data = "1"
    conn2.send(data.encode())
    #data = conn.recv(1024).decode()
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        player1 = conn.recv(1024).decode()
        conn2.send(player1.encode())
        player2 = conn2.recv(1024).decode()
        conn.send(player2.encode())
        if not data:
            # if data is not received break
            break
        #print("from connected user: " + str(data))
        #data = input(' -> ')
        #conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
    q = input("Press q to exit")
