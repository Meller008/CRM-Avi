import socket, time


# sock = socket.socket()
# sock.bind( ("", 6666) )
# sock.listen(5)
#
# try:
#     while 1: # работаем постоянно
#         conn, addr = sock.accept()
#         print("New connection from " + addr[0])
#         try:
#             data = conn.recv(16384)
#             udata = data.decode("utf-8")
#             print("Data: " + udata)
#         except:
#             print("err")
#         finally:
#             # так при любой ошибке
#             # сокет закроем корректно
#             conn.close()
# finally: sock.close()


conn = socket.socket()
conn.connect( ("127.0.0.1", 6666) )

conn.send(b"data_ok")


# в скрипте, читающем данные:
try: data = conn.recv(1024)
except socket.error: # данных нет
    pass # тут ставим код выхода
else: # данные есть
    print(data)
    # если в блоке except вы выходите,
    # ставить else и отступ не нужно
