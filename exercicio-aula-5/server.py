import sys, threading, pickle
from time import sleep
from socket import socket
from threading import Thread

TAMANHO_PACOTE = 4096
MAX_THREADS = 4
SEPARATOR = "<>"

thread_count = 0
count_lock = False

def processar(sck):
    global thread_count
    global count_lock

    while count_lock:
        continue
    count_lock = True
    thread_count += 1
    count_lock = False
    identificador = threading.current_thread().ident

    try:
        conexao, origem = sck.accept()
        print(f"{identificador} - Nova conexão estabelecida...")
        print(f"{identificador} - Processando Requisição...")
        array, num = traduzirMensagem(conexao)
        # array = pickle.loads(bytes(array, encoding='utf8'))
        array = list(map(int, array.split(",")))
        num = int(num)
        if num in array:
            conexao.send(str(array.index(num)).encode())
        else:
            conexao.send("-1".encode())
        conexao.close()
    except Exception as ex:
        print(f"{identificador} - Erro: {ex}")
    finally:
        while count_lock:
            continue
        count_lock = True
        thread_count -= 1
        count_lock = False

        print(f"{identificador} - Processamento Encerrado!")

def traduzirMensagem(conexao):
    bytes_lidos = 0
    res = conexao.recv(TAMANHO_PACOTE).decode()
    bytes_lidos += len(res)
    if res.count(SEPARATOR) == 1:
        total, array = res.split(SEPARATOR)
    else:
        total, array, num = res.split(SEPARATOR)
    total = int(total)
    while bytes_lidos < total:
        dado = conexao.recv(min(total - bytes_lidos, TAMANHO_PACOTE)).decode()
        bytes_lidos = bytes_lidos + len(dado)
        if dado == "":
            raise RuntimeError("Conexão socket falhou!")
        if SEPARATOR in dado:
            dado, num = dado.split(SEPARATOR)
        array += dado
    return array, num

def escutar():
    print("Iniciando Servidor...")
    socket_bind_info = ('127.0.0.1', 3001)
    sck = socket()
    sck.bind(socket_bind_info)
    sck.listen()
    print("Servidor Iniciado!")

    while True:
        try:
            if thread_count < MAX_THREADS :
                thread = Thread(target=processar, args=(sck,))
                thread.start()

        except KeyboardInterrupt:
            sck.close()
            print("Programa Encerrado!")
            sys.exit(1)


if __name__ == '__main__':
    escutar()
