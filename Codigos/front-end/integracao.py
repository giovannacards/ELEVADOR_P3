import network
import usocket as socket 
import ujson
from machine import Pin
from elevador_final import *

'''
**************************** FUNCIONAMENTO *********************************

i -) O arquivo elevador_final (que contém a classe elevador)
é chamado.

ii -) É criado um ponto de acesso "Elevador2D" cuja senha é "elevador2023!"

iii -) Os arquivos HTML, CSS e JavaScript são carregados e atualizados para
a página via websocket 

iv -) A cada vez que o botão mover é pressionado após a seleção da posição
o ESP32 recebe, atráves do JavaScript, o número da posição e move, dispensa a
peça e volta para a posição inicial automaticamente.

OBS: O botão dispensar não precisa ser pressionado depois de mover o elevador

******************************************************************************
'''


def init_wifi():
    """
    Esta função recebe os parâmetros de configuração
    da rede e se conecta a rede Wifi.
    :return: retorna network.AP
    """
    
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='Elevador2D', authmode=3, password='elevador2023!')
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))


    print("Rede WIFI iniciada")
    print(f'IP: {ap.ifconfig()[0]}')
    
    return ap



def serve_file(file_path: str) -> str:
    """
    Esta função recebe o caminho do arquivo (HTML, CSS, JavaScript, Json)
    para efetuar sua leitura.
    :param file_path: recebe o caminho do arquivo.
    :return: retorna o conteúdo do arquivo
    """

    try:
        with open(file_path, 'r') as file:
            return file.read()
    except OSError:
        return None
    

def handle_post_request(client_socket: socket, path, data):
    elev = elevador()
    """
    Essa função lida com as requisições POST.
    :param client_socket: recebe o objeto socket
    :param path: recebe a rota especificada no JavaScript
    :param data: recebe os dados da requisição POST
    """ 
    if path == '/dispensar' and data:
        try:
            json_data = ujson.loads(data) # Atribui o json à variável
            isPressed = json_data.get('isPressionado')
            
            if isPressed:
                print('Dispensando...')
                elev.dispensar()
                print('Dispensado!\n')

            # Resposta de que o json foi recebido com sucesso
            client_socket.send('HTTP/1.1 200 OK\n')
            client_socket.send('Content-Type: text/plain\n')
            client_socket.send('Connection: close\n\n')
            
        except Exception as e:
            print("Erro ao lidar com a solicitação POST:", str(e))
    else:
        client_socket.send('HTTP/1.1 404 Not Found\n')
        client_socket.send('Content-Type: text/html\n')
        client_socket.send('Connection: close\n\n')
        client_socket.send('Rota não encontrada')

    if path == '/moverElevador' and data:
        try:
            json_data = ujson.loads(data) # Atribui o json à variável
            position = json_data.get('position')
            print(f"Movendo para a posição {position}...")
            elev.mover(position)
            elev.voltar(position)
            
            # Resposta de que o json foi recebido com sucesso
            client_socket.send('HTTP/1.1 200 OK\n')
            client_socket.send('Content-Type: text/plain\n')
            client_socket.send('Connection: close\n\n')
            
        except Exception as e:
            print("Erro ao lidar com a solicitação POST:", str(e))
    else:
        client_socket.send('HTTP/1.1 404 Not Found\n')
        client_socket.send('Content-Type: text/html\n')
        client_socket.send('Connection: close\n\n')
        client_socket.send('Rota não encontrada')
    

def handle_static_request(client_socket: socket, path: str):
    """
    Essa função lida com as solicitações estáticas.
    :param client_socket: recebe o objeto socket 
    :param path: recebe a rota de cada arquivo 
    """
    
    content_type = 'text/html'  # Tipo de conteúdo inicial

    # Se terminar com .<ext> o tipo do conteúdo recebe tal
    if path.endswith('.css'):
        content_type = 'text/css'
    elif path.endswith('.js'):
        content_type = 'application/javascript'
    elif path.endswith('.json'):
        pass
    if path.endswith('.json'):
        pass
    else:
        # Senão, carrega os outros arquivos
        response = serve_file(path)

    if response is not None:
        client_socket.send('HTTP/1.1 200 OK\n')
        client_socket.send(f'Content-Type: {content_type}\n')
        client_socket.send('Connection: close\n\n')
        client_socket.sendall(response.encode('utf-8'))
    else:
        client_socket.send('HTTP/1.1 404 Not Found\n')
        client_socket.send('Content-Type: text/html\n')
        client_socket.send('Connection: close\n\n')
        client_socket.send('File not found')


def handle_request(client_socket: socket):
    """
    Esta função lida com as solicitações estáticas, e
    também com o recebimento do json enviado do JavaScript.
    :param client_socket: recebe o objeto socket
    """

    request = client_socket.recv(1024)
    request_str = request.decode('utf-8')

    """
    request_str é o texto de requisição POST / GET como abaixo:

        GET /style.css HTTP/1.1
        Host: 192.168.207.74
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36
        DNT: 1
        Accept: text/css,*/*;q=0.1
        Referer: http://192.168.207.74/
        Accept-Encoding: gzip, deflate
        Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6
    """

    try:
        """
        Retorna somente os dois primeiros elementos
        Como por exemplo: ['GET', /style.css] ou ['POST', '/moverElevador']
        """
        method, path = request_str.split(' ')[:2]
        if method == 'POST':
            content_length = 0
            """
            Ao invés de uma lista de elementos de request_str
            retorna uma lista de linhas de request_str
            """
            for line in request_str.split('\r\n'):
                """
                Se conter a informação Content-Length, se trata do POST feito
                via JavaScript
                """
                if 'Content-Length' in line:
                    # i) Content-Length: 16
                    # ii) ['Content-Length', '16']
                    # iii) int(16)
                    content_length = int(line.split(': ')[1])
           
            """
            Se tratando de uma requisição POST, o conteúdo é colocado duas
            linhas abaixo, ou seja, são separados por (\r\n\r\n)
            """
            data = request_str.split('\r\n\r\n')[1]
            if content_length > 0:
                """
                Caso o tamanho do json for menor que o tamanho do conteúdo
                a leitura é refeita
                """
                while len(data) < content_length:
                    data += client_socket.recv(1024).decode('utf-8')

            handle_post_request(client_socket, path, data)
        else:
            if path == '/':
                path = '/index.html'  # Página inicial
            file_path = path[1:]  

            """
            No JavaScript, na função obterDadosElevador() é
            feita a solicitação pela rota /json/elevator_positions.json
            """
            
            if file_path.startswith('/json'):
                pass

            else:
                handle_static_request(client_socket, file_path)
    except Exception as e:
        print("Erro ao lidar com a solicitação:", str(e))



def main():
    PORT = 80
    ponto_acesso = init_wifi()
    addr = socket.getaddrinfo(ponto_acesso.ifconfig()[0], PORT)[0][-1]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(4)

    print('Servidor web em execução...')
    print("Aguardando solicitações...")

    while True:
        client, addr = server.accept()
        client.settimeout(42.0)
        try:
            handle_request(client)
        except Exception as e:
            print("Erro ao lidar com solicitação:", str(e))
        finally:
            client.close()

if __name__ == "__main__":
    main()

