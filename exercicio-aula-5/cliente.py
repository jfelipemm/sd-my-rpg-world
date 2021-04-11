import numpy, random, pickle, codecs
from socket import socket
from config import config

IP = config["ip"]
PORT = config["port"]
TAMANHO_PACOTE = config["tamanhoPacote"]
MIN_NUMBER = config["numeroMinimo"]
MAX_NUMBER = config["numeroMaximo"]
SIZE = config["tamanhoArray"]
SEPARATOR = config["separador"]

def requisicao():
    sck = socket()
    sck2 = socket()

    server_info = (IP, PORT)
    server_info2 = (IP, PORT + 1)
    sck.connect(server_info)
    print("Conexao com o servidor 1 foi aceita!")
    sck2.connect(server_info2)
    print("Conexao com o servidor 2 foi aceita!")

    print("Enviando mensagem...")
    array = numpy.random.randint(MIN_NUMBER, MAX_NUMBER, SIZE)
    num = random.randint(MIN_NUMBER, MAX_NUMBER)
    print(f"Array: {array} --- Num: {num}")
    
    array1, array2 = numpy.array_split(array, 2)
    mensagem1 = criarMensagem(list(array1), num)
    mensagem2 = criarMensagem(list(array2), num)
    sck.send(mensagem1.encode())
    sck2.send(mensagem2.encode())

    res = sck.recv(TAMANHO_PACOTE).decode()
    res2 = sck2.recv(TAMANHO_PACOTE).decode()

    if "-" not in res:
        print(f"Índice do número: {res}!")
    elif "-" not in res2:
        res2 = int(res2) + len(array1)
        print(f"Índice do número: {res2}!")
    else:
        print(f"Número não existe no array!")
    
    sck.close()
    sck2.close()

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

if __name__ == '__main__':
    requisicao()
