from machine import Pin
from time import sleep
from stepper import Stepper

class elevador():
    def __init__(self) -> None:
        self.motor_x_step = 14
        self.motor_x_dir = 27
        self.motor_y_step = 13
        self.motor_y_dir = 12
        self.servo = Pin(22,Pin.OUT)
        self.enderecos = {
                1: (0, 0),
                2: (2500, 0), 
                3: (5000, 0),
                4: (0, -2500), 
                5: (2500, -2500), 
                6: (5000, -2500),
                7: (0, -5000), 
                8: (2500, -5000),
                9: (5000, -5000),
            }
        

    def mover(self, endereco):
        self.endereco = endereco
        if self.endereco in self.enderecos:
            pos_x, pos_y = self.enderecos[self.endereco]
            
            s2 = Stepper(self.motor_x_step, self.motor_x_dir, steps_per_rev=200, speed_sps=400)
            s2.target(pos_x)
            sleep(20)
            self.dispensar()

            s1 = Stepper(self.motor_y_step, self.motor_y_dir, steps_per_rev=200,speed_sps=400)
            s1.target(pos_y)
            sleep(20)


    def voltar(self, endereco):
        self.endereco = endereco
        if self.endereco in self.enderecos:
            pos_x, pos_y = self.enderecos[self.endereco]

            s1 = Stepper(self.motor_y_step, self.motor_y_dir, steps_per_rev=200,speed_sps=400)
            s1.target(pos_y * -1)
            sleep(20)
            
            s2 = Stepper(self.motor_x_step, self.motor_x_dir, steps_per_rev=200, speed_sps=400)
            s2.target(pos_x * -1)
            sleep(20)

            

    
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
        print('Peça depositada!')
        
 '''       
while True:
    eleva=elevador()
    eleva.mover(2)
    sleep(14)
    eleva.voltar(2)
    sleep(14)
'''
