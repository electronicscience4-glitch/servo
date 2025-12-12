
from machine import Pin, PWM
from time import sleep

# ڕێکخستنی پینی PWM بۆ کۆنتڕۆڵی سێرڤۆ
servo_pin = Pin(0)
servo = PWM(servo_pin)

# ڕێکخستنی Duty Cycle بۆ پلە جیاوازەکان
max_duty = 7864    # 180 پلە
min_duty = 1802    # 0 پلە
half_duty = int((max_duty + min_duty) / 2)  # 90 پلە

# ڕێکخستنی فرێکوێنسی PWM
frequency = 50
servo.freq(frequency)

def move_servo(angle):
    """جوڵاندنی سێرڤۆ بۆ پلەیەکی دیاریکراو (0-180)"""
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    
    # گۆڕینی پلە بۆ دەیوتی سایکڵ
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)
    return duty

def sweep_servo(start_angle=0, end_angle=180, step=10, delay=0.1):
    """جوڵاندنی سێرڤۆ بە شێوازێکی هاتوچۆ"""
    if start_angle < end_angle:
        angles = range(start_angle, end_angle + 1, step)
    else:
        angles = range(start_angle, end_angle - 1, -step)
    
    for angle in angles:
        duty = move_servo(angle)
        print(f"پلە: {angle}° - Duty: {duty}")
        sleep(delay)

def test_servo_positions():
    """تاقیکردنەوەی پلە جیاوازەکانی سێرڤۆ"""
    positions = [
        (0, "0 پلە - لای چەپ"),
        (45, "45 پلە"),
        (90, "90 پلە - ناوەند"),
        (135, "135 پلە"),
        (180, "180 پلە - لای ڕاست")
    ]
    
    for angle, description in positions:
        print(f"جوڵاندن بۆ {description}")
        move_servo(angle)
        sleep(2)

print("🚀 سێرڤۆ مۆتۆر - ڕاسپبێری پیکۆ")
print(f"فرێکوێنسی PWM: {frequency}Hz")
print(f"Duty Cycle: {min_duty} - {max_duty}")

try:
    while True:
        print("\n🔧 هەڵبژاردە:")
        print("1. جوڵەی هاتوچۆ (سویپ)")
        print("2. پلە دیاریکراوەکان")
        print("3. چوارگۆشە (0-90-180)")
        print("4. کۆتایی")
        
        choice = input("➡️  هەڵبژاردن (1-4): ").strip()
        
        if choice == "1":
            print("🔄 جوڵەی هاتوچۆ...")
            sweep_servo(0, 180, 5, 0.05)
            sweep_servo(180, 0, 5, 0.05)
            
        elif choice == "2":
            print("🎯 پلە دیاریکراوەکان...")
            test_servo_positions()
            
        elif choice == "3":
            print("🔄 چوارگۆشە...")
            for angle in [0, 90, 180, 90]:
                move_servo(angle)
                print(f"پلە: {angle}°")
                sleep(1)
                
        elif choice == "4":
            print("👋 کۆتایی هات")
            break
            
        else:
            print("❌ هەڵبژاردنی نادروست")
            
except KeyboardInterrupt:
    print("\n❌ کۆتایی هات بە Ctrl+C")
    
finally:
    # کوژاندنەوەی PWM
    servo.deinit()
    print("✅ PWM کوژایەوە")
