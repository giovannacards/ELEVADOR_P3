import machine
from machine import Pin
from time import sleep

#define o pino do servo 
servo = Pin(22,Pin.OUT)

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