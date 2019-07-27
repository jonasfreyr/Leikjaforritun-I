import _thread, socket

HOST = '127.0.0.1'   # Standard loopback interface address (localhost)
PORT = 65432

conns = []

players = {}
bullets = {}
grenades = {}

id = 1

def new_client(conn, addr, id):
    print("Connection started with:", addr)
    while True:
        try:
            data = conn.recv(262144).decode()

            data = eval(data)

            players[id] = data

        except:
            print("Connection ended with:", addr)
            conns.remove(conn)
            del players[id]
            break

        try:
            temp = dict(players)

            del temp[id]


            conn.sendall(str(temp).encode())

            print("-----------")

        except:
            print("fd")
            conns.remove(conn)
            del players[id]
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)

    # _thread.start_new_thread(start_main, ())
    while True:
        conn, addr = s.accept()

        conns.append(conn)

        _thread.start_new_thread(new_client, (conn, addr, id))

        id += 1