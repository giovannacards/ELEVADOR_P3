import machine
from machine import Pin
import time
from time import sleep
from stepper import Stepper

ligar_modo_prints = True

# Configuração dos pinos dos motores
motor_x_step = 14
motor_x_dir = 27
motor_y_step = 13
motor_y_dir = 12

# Configuração dos endereços e posições
enderecos = {
    1: (0, 0),
    2: (2500, 0), 
    3: (5000, 0),
    4: (0, 2500), 
    5: (2500, 2500),
    6: (5000, 2500),
    7: (0, 5000), 
    8: (2500, 5000),
    9: (5000, 5000),
}


# Função para mover o elevador para um endereço
def mover_para_endereco(endereco):
    if endereco in enderecos:
        pos_x, pos_y = enderecos[endereco]
        mover_eixos(pos_x, pos_y)


# Função para mover ambos os eixos para as posições
def mover_eixos(posicao_x, posicao_y):
    mover_motor_x(posicao_x)
    mover_motor_y(posicao_y)


# Mover em X
def mover_motor_x(posicao_x):
    # Se target positivo, para a direita, se negativo para a esquerda
    s2 = Stepper(motor_x_step,motor_x_dir,steps_per_rev=200,speed_sps=300)
    s2.target(posicao_x)

    time.sleep(20)

    '''s2 = Stepper(motor_x_step,motor_x_dir,steps_per_rev=200,speed_sps=300)
    s2.target(posicao_x * -1)

    time.sleep(20)'''

  
# Mover em Y
def mover_motor_y(posicao_y):
    # Se target positivo, para baixo, se negativo para cima
    s1 = Stepper(motor_y_step,motor_y_dir,steps_per_rev=200,speed_sps=300)
    s1.target(posicao_y)

    time.sleep(20)

    '''s1 = Stepper(motor_y_step,motor_y_dir,steps_per_rev=200,speed_sps=300)
    s1.target(posicao_y * -1)

    time.sleep(20)'''


# Dispensar a peça
def dispensar():
    i = 0
    x = 0

    # Picuda na peça
    while i < 32:
        servo = Pin(22,Pin.OUT)
        servo.value(1)
        sleep(0.0024)
        servo.value(0)
        i += 1

    sleep(1)
    
    # Servo volta à posição inicial
    while x < 32 :
        servo = Pin(22,Pin.OUT)
        servo.value(1)
        sleep(0.0015)
        servo.value(0)
        x += 1


while True:
    
    #tempo de pausa entre os movimentos   
    sleep(1)
    # Exemplo de uso para mover para o endereço 1
    time.sleep(5)
    mover_para_endereco(6)
    dispensar()
    
    # mover para origem quando o botao de reset da pagina for pressionado
    mover_para_endereco(1)