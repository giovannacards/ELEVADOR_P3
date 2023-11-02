from stepper import Stepper
import time
from time import sleep
from machine import Pin

while True:
    
    i=0
    x=0
    
    
 
    #90 graus
    while i<32:
        servo = Pin(22,Pin.OUT)
        servo.value(1)# ativa o servo
        sleep(0.0024)# largura de pulso de 2,4 ms
        servo.value(0)# desliga o servo
        i+=1 #soma 1 no contador
    
    #tempo de pausa entre os movimentos
    sleep(1)
    
    #0 graus
    while x < 32 :
        servo = Pin(22,Pin.OUT)
        servo.value(1)# ativa o servo
        sleep(0.0015)#largura de pulso de 1,5 ms
        servo.value(0)# desliga o servo
        x+=1#soma 1 no contador
        
    #tempo de pausa entre os movimentos   
    sleep(1)
    
    time.sleep(5)
    s2 = Stepper(14,27,steps_per_rev=200,speed_sps=300)
    print("pãozinnho")
    s2.target(5000)
    time.sleep(20)
    s2 = Stepper(14,27,steps_per_rev=200,speed_sps=300)
    s2.target(-5000)
    time.sleep(20)
    print("batata")
    s1 = Stepper(13,12,steps_per_rev=200,speed_sps=400)
    
    print("pexinho")
    s1.target(5000)
    time.sleep(20)
    s1 = Stepper(13,12,steps_per_rev=200,speed_sps=400)
    s1.target(-5000)
    time.sleep(20)
    print("ah zé augustu")