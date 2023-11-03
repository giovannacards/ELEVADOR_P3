import machine
from machine import Pin
import time
from time import sleep
from stepper import Stepper

class elevador():
    '''
    Essa classe é responsável por mover os
    eixo para as respectivas posições.
    :param endereco: recebe o endereço das posições x e y
    '''


    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.motor_x_step = 14
        self.motor_x_dir = 27
        self.motor_y_step = 13
        self.motor_y_dir = 12
        self.servo = Pin(22,Pin.OUT)
        self.enderecos = {
                1: (0, 0), 2: (2500, 0), 3: (5000, 0),
                4: (0, 2500), 5: (2500, 2500), 6: (5000, 2500),
                7: (0, 5000), 8: (2500, 5000), 9: (5000, 5000),
            }
        

    def mover(self):
        if self.endereco in self.enderecos:
            pos_x, pos_y = self.enderecos[self.endereco]
            
            s2 = Stepper(self.motor_x_step, self.motor_x_dir, steps_per_rev=200, speed_sps=300)
            s2.target(pos_x)
            time.sleep(20)

            s1 = Stepper(self.motor_y_step, self.motor_y_dir, steps_per_rev=200,speed_sps=300)
            s1.target(pos_y)
            time.sleep(20)


    def voltar(self):
        if self.endereco in self.enderecos:
            pos_x, pos_y = self.enderecos[self.endereco]
            
            s2 = Stepper(self.motor_x_step, self.motor_x_dir, steps_per_rev=200, speed_sps=300)
            s2.target(pos_x * -1)
            time.sleep(20)

            s1 = Stepper(self.motor_y_step, self.motor_y_dir, steps_per_rev=200,speed_sps=300)
            s1.target(pos_y * -1)
            time.sleep(20)

    
    def dispensar(self):
        i = 0
        x = 0

        # Picuda na peça
        while i < 32:
            self.servo.value(1)
            sleep(0.0024)
            self.servo.value(0)
            i += 1

        sleep(1)
        
        # Servo volta à posição inicial
        while x < 32 :
            self.servo.value(1)
            sleep(0.0015)
            self.servo.value(0)
            x += 1




while True:
    elev = elevador(6)
    elev.mover()
    elev.voltar()
    elev.dispensar()


    '''
    #tempo de pausa entre os movimentos   
    sleep(1)
    # Exemplo de uso para mover para o endereço 1
    time.sleep(5)
    mover_para_endereco(6)
    dispensar()

    # mover para origem quando o botao de reset da pagina for pressionado
    mover_para_endereco(1)'''

