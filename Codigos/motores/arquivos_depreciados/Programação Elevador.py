import machine
from machine import Pin
from time import sleep


"""
----------------------------------------------------

                MOTORES DA ESTRUTURA

----------------------------------------------------
"""

# Configuração dos pinos dos motores
motor_x_step = Pin(0, Pin.OUT)
motor_x_dir = Pin(1, Pin.OUT)
motor_y1_step = Pin(2, Pin.OUT)
motor_y1_dir = Pin(3, Pin.OUT)
motor_y2_step = Pin(4, Pin.OUT)
motor_y2_dir = Pin(5, Pin.OUT)

# Configuração dos endereços e posições
enderecos = {
    1: (100, 100),  # Exemplo: Endereço 1 com posição (X, Y)
    2: (200, 200),  # Endereço 2
    3: (300, 300),  # Endereço 3
    # ... Adicione os outros endereços e posições aqui
}

# Função para mover o elevador para um endereço específico
def mover_para_endereco(endereco):
    if endereco in enderecos:
        pos_x, pos_y = enderecos[endereco]
        mover_eixos(pos_x, pos_y)

# Função para mover ambos os eixos para as posições especificadas
def mover_eixos(posicao_x, posicao_y):
    mover_motor_x(posicao_x)
    mover_motor_y(posicao_y)

# Função para mover o motor X para uma posição específica
def mover_motor_x(posicao_x):
    # Determine a direção (sentido) em que o motor X deve girar
    if posicao_x > 0:
        motor_x_dir.value(1)  # Configura a direção para frente
    else:
        motor_x_dir.value(0)  # Configura a direção para trás

    # Calcule o número de passos necessários para chegar à posição desejada
    passos_x = abs(posicao_x)
    
    # Gere os pulsos para mover o motor X
    for _ in range(passos_x):
        motor_x_step.value(1)  # Sinal de pulso alto
        sleep(0.001)  # Aguarda um curto período de tempo (ajuste conforme necessário)
        motor_x_step.value(0)  # Sinal de pulso baixo
        sleep(0.001)  # Aguarda um curto período de tempo (ajuste conforme necessário)

# Função para mover os motores de passo no eixo Y para uma posição específica
def mover_motor_y(posicao_y):
    # Determine a direção (sentido) em que os motores Y devem girar
    if posicao_y > 0:
        motor_y1_dir.value(1)  # Configura a direção do motor Y1 para frente
        motor_y2_dir.value(1)  # Configura a direção do motor Y2 para frente
    else:
        motor_y1_dir.value(0)  # Configura a direção do motor Y1 para trás
        motor_y2_dir.value(0)  # Configura a direção do motor Y2 para trás

    # Calcule o número de passos necessários para chegar à posição desejada
    passos_y = abs(posicao_y)
    
    # Gere os pulsos para mover os motores Y
    for _ in range(passos_y):
        motor_y1_step.value(1)  # Sinal de pulso alto para motor Y1
        motor_y2_step.value(1)  # Sinal de pulso alto para motor Y2
        sleep(0.001)  # Aguarda um curto período de tempo (ajuste conforme necessário)
        motor_y1_step.value(0)  # Sinal de pulso baixo para motor Y1
        motor_y2_step.value(0)  # Sinal de pulso baixo para motor Y2
        sleep(0.001)  # Aguarda um curto período de tempo (ajuste conforme necessário)

# Exemplo de uso para mover para o endereço 1
mover_para_endereco(1)


"""
----------------------------------------------------------------

                            ATUADOR

----------------------------------------------------------------
"""
#define o pino do servo 
servo = Pin(13,Pin.OUT)

#função que dispensa a peça no local desejado
def dispensar():
    
    """
        Os comando abaixo indicam a posição que o servo deve admitir ao executar a função a função.
        O servo está sendo comandado sem o uso de uma biblioteca.
        Adotando a posição inicial como 0 graus, temos o movimento do servo para 90° e 0° novamente
        Mais informações em: https://www.makerhero.com/blog/video-controle-de-servo-motor-sem-biblioteca/
    """
    
    #inicia os contadores das variáveis x e y
    i=0
    x=0
    
    
 
    #90 graus
    while i<32:
        servo.value(1)# ativa o servo
        sleep(0.0024)# largura de pulso de 2,4 ms
        servo.value(0)# desliga o servo
        i+=1 #soma 1 no contador
    
    #tempo de pausa entre os movimentos
    sleep(1)
    
    #0 graus
    while x < 32 :
        servo.value(1)# ativa o servo
        sleep(0.0015)#largura de pulso de 1,5 ms
        servo.value(0)# desliga o servo
        x+=1#soma 1 no contador
        
    #tempo de pausa entre os movimentos   
    sleep(1)

#exemplo de como executar a função:
dispensar()       


