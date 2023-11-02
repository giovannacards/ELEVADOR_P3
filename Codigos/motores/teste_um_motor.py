from stepper import Stepper
import time

while True:
    s1 = Stepper(13,12,steps_per_rev=200,speed_sps=400)
    s1.target(5000)
    time.sleep(20)
    s1 = Stepper(13,12,steps_per_rev=200,speed_sps=400)
    s1.target(-5000)
    time.sleep(20)