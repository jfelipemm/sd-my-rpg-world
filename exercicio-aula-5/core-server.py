import sys, threading, pickle, numpy
from time import sleep
from socket import socket
from threading import Thread
from config import config

IP = config["ip"]
PORT = config["port"]
PORT_FIND_SERVER = config["portFindServer"]
TAMANHO_PACOTE = config["tamanhoPacote"]
SEPARATOR = config["separador"]
MAX_THREADS = config["maxThreadsCoreServer"]
FIND_OPERATION = config["findOperation"]

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
        operation, array, num = traduzirMensagem(conexao)
        if operation == FIND_OPERATION:
            res = enviarParaFindServers(array, num)
            conexao.send(res.encode())
        else:
            print(f"{identificador} - Operação não suportada!")
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
    if res.count(SEPARATOR) < 3:
        total, operation, array = res.split(SEPARATOR)
    else:
        total, operation, array, num = res.split(SEPARATOR)
    total = int(total)
    while bytes_lidos < total:
        dado = conexao.recv(min(total - bytes_lidos, TAMANHO_PACOTE)).decode()
        bytes_lidos = bytes_lidos + len(dado)
        if dado == "":
            identificador = threading.current_thread().ident
            raise RuntimeError(f"{identificador} - Conexão socket falhou!")
        if SEPARATOR in dado:
            dado, num = dado.split(SEPARATOR)
        array += dado
    return operation, array, num

def enviarParaFindServers(array, num):
    sck = socket()
    sck2 = socket()

    identificador = threading.current_thread().ident

    server_info = (IP, PORT_FIND_SERVER)
    server_info2 = (IP, PORT_FIND_SERVER + 1)
    sck.connect(server_info)
    print(f"{identificador} - Conexao com o servidor 1 foi aceita!")
    sck2.connect(server_info2)
    print(f"{identificador} - Conexao com o servidor 2 foi aceita!")

    print(f"{identificador} - Enviando mensagem...")
    array = list(map(int, array.split(",")))
    array1, array2 = numpy.array_split(array, 2)
    mensagem1 = criarMensagem(list(array1), num)
    mensagem2 = criarMensagem(list(array2), num)
    sck.send(mensagem1.encode())
    sck2.send(mensagem2.encode())

    res = sck.recv(TAMANHO_PACOTE).decode()
    res2 = sck2.recv(TAMANHO_PACOTE).decode()

    if "-" not in res:
        return res
    elif "-" not in res2:
        res2 = int(res2) + len(array1)
        return str(res2)
    else:
        return "-1"

def criarMensagem(array, num):
    array = ','.join([str(i) for i in array])
    mensagem = str(array) + SEPARATOR + str(num)
    # mensagem = pickle.dumps(array, 0).decode() + SEPARATOR + str(num)
    # array = codecs.encode(pickle.dumps(array), "base64").decode()
    # mensagem = array + SEPARATOR + str(num)
    tam = len(SEPARATOR + mensagem)
    tam += len(str(tam))
    mensagem = str(tam) + SEPARATOR + mensagem
    return mensagem

def escutar():
    print("")
    print(f"Iniciando servidor...")
    socket_bind_info = (IP, PORT)
    sck = socket()
    sck.bind(socket_bind_info)
    sck.listen()
    print(f"Servidor iniciado na porta {PORT}!")

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
