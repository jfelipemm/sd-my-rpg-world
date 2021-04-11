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
FIND_OPERATION = config["findOperation"]

def requisicao():
    sck = socket()
    sck2 = socket()

    server_info = (IP, PORT)
    sck.connect(server_info)
    print("Conexao com o servidor foi aceita!")

    print("Enviando mensagem...")
    array = numpy.random.randint(MIN_NUMBER, MAX_NUMBER, SIZE)
    num = random.randint(MIN_NUMBER, MAX_NUMBER)
    print(f"Array: {array} --- Num: {num}")
    
    mensagem = criarMensagem(list(array), num)
    sck.send(mensagem.encode())

    res = sck.recv(TAMANHO_PACOTE).decode()

    if not res:
        print("Não foi possível executar a operação. Algum erro ocorreu no servidor!")
    elif "-" not in res:
        print(f"Índice do número: {res}!")
    else:
        print(f"Número não existe no array!")
    
    sck.close()

def criarMensagem(array, num):
    array = ','.join([str(i) for i in array])
    mensagem = FIND_OPERATION + SEPARATOR + str(array) + SEPARATOR + str(num)
    # mensagem = pickle.dumps(array, 0).decode() + SEPARATOR + str(num)
    # array = codecs.encode(pickle.dumps(array), "base64").decode()
    # mensagem = array + SEPARATOR + str(num)
    tam = len(SEPARATOR + mensagem)
    tam += len(str(tam))
    mensagem = str(tam) + SEPARATOR + mensagem
    return mensagem

if __name__ == '__main__':
    requisicao()
