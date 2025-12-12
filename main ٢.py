from machine import Pin, PWM
from time import sleep

# پێکهاتەی سادە
servo = PWM(Pin(0))
servo.freq(50)

min_duty = 1802
max_duty = 7864

def move_servo(angle):
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)
    print(f"پلە: {angle}°")

# تاقیکردنەوەی خێرا
try:
    while True:
        move_servo(0)
        sleep(1)
        move_servo(90)
        sleep(1)
        move_servo(180)
        sleep(1)
        
except KeyboardInterrupt:
    servo.deinit()
    print("کۆتایی هات")