### Requerimentos
- Python 3
- Módulo Numpy (Requerido para exercicio-aula-5)

### Como instalar o Numpy
Com o python instalado, execute o seguinte comando no terminal:
`pip install numpy`

### Como executar um arquivo python
Basta digitar em um terminal o seguinte comando:
Para linux: `python3 nomedoarquivo`
Para windows: `python nomedoarquivo`
O nome do arquivo deve conter a extensão `.py`.

### Para executar o programa
Execute o arquivo `core-server.py` que funciona como serviço central para receber requisições do cliente. Execute 2 instâncias do arquivo `find-server.py` que são os serviços responsáveis por receber requições do core-server para cada trecho do array.
Com o core-server e duas instâncias do find-server em execução, execute o arquivo `cliente.py`. Ele é responsável por enviar uma requisição ao core-server com o array e o número a ser encontrado.