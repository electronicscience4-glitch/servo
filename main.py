from machine import Pin, PWM
from time import sleep, ticks_ms

class ServoController:
    def __init__(self, pin=0, min_duty=1802, max_duty=7864, freq=50):
        self.servo = PWM(Pin(pin))
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.freq = freq
        self.servo.freq(freq)
        self.current_angle = 0
        
        print(f"🎯 سێرڤۆ کۆنتڕۆڵەر - پین: GP{pin}")
        print(f"   Duty Cycle: {min_duty} - {max_duty}")
        print(f"   فرێکوێنسی: {freq}Hz")
    
    def move_to_angle(self, angle, speed=1.0):
        """جوڵاندنی سێرڤۆ بۆ پلەی دیاریکراو بە خێرایی"""
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        
        target_duty = int(self.min_duty + (angle / 180) * (self.max_duty - self.min_duty))
        current_duty = self.servo.duty_u16()
        
        # جوڵە بە شێوازێکی نەرم
        steps = abs(target_duty - current_duty)
        if steps > 0:
            step_size = max(1, int(steps / (speed * 100)))
            if target_duty > current_duty:
                for duty in range(current_duty, target_duty, step_size):
                    self.servo.duty_u16(duty)
                    sleep(0.01 / speed)
            else:
                for duty in range(current_duty, target_duty, -step_size):
                    self.servo.duty_u16(duty)
                    sleep(0.01 / speed)
        
        self.servo.duty_u16(target_duty)
        self.current_angle = angle
        print(f"📊 پلە: {angle}° - Duty: {target_duty}")
        
        return target_duty
    
    def sweep(self, start=0, end=180, step=1, delay=0.02):
        """جوڵەی هاتوچۆی سێرڤۆ"""
        if start < end:
            angles = range(start, end + 1, step)
        else:
            angles = range(start, end - 1, -step)
        
        for angle in angles:
            self.move_to_angle(angle)
            sleep(delay)
    
    def oscillate(self, center_angle=90, amplitude=45, cycles=5, speed=1.0):
        """جوڵەی دەنگەڕەش (ئۆسیلاتۆر)"""
        for i in range(cycles):
            # بڕۆ بۆ ئەندامە ڕاستەکە
            self.move_to_angle(center_angle + amplitude, speed)
            # بڕۆ بۆ ئەندامە چەپەکە
            self.move_to_angle(center_angle - amplitude, speed)
        
        # گەڕانەوە بۆ ناوەند
        self.move_to_angle(center_angle, speed)
    
    def sequence(self, angles, delays):
        """ئەنجامدانی زنجیرەیەک جوڵە"""
        for angle, delay in zip(angles, delays):
            self.move_to_angle(angle)
            sleep(delay)
    
    def calibrate(self, test_angles=[0, 45, 90, 135, 180]):
        """کالیبرکردنی سێرڤۆ"""
        print("🔧 کالیبرکردنی سێرڤۆ...")
        for angle in test_angles:
            duty = self.move_to_angle(angle)
            print(f"   {angle}° -> Duty: {duty}")
            sleep(1)
    
    def get_current_angle(self):
        """وەرگرتنەوەی پلەی ئێستا"""
        return self.current_angle
    
    def deinit(self):
        """کوژاندنەوەی سێرڤۆ"""
        self.servo.deinit()
        print("✅ سێرڤۆ کوژایەوە")

# نمونەی بەکارهێنان
servo = ServoController(pin=0)

def main():
    print("🚀 سێرڤۆ مۆتۆر - پیکۆ")
    
    try:
        while True:
            print("\n🎮 هەڵبژاردە:")
            print("1. کالیبرکردن")
            print("2. جوڵەی هاتوچۆ")
            print("3. جوڵەی دەنگەڕەش")
            print("4. زنجیرەی جوڵە")
            print("5. پلەی دیاریکراو")
            print("6. کۆتایی")
            
            choice = input("➡️  هەڵبژاردن (1-6): ").strip()
            
            if choice == "1":
                servo.calibrate()
                
            elif choice == "2":
                print("🔄 جوڵەی هاتوچۆ...")
                servo.sweep(0, 180, 2, 0.03)
                servo.sweep(180, 0, 2, 0.03)
                
            elif choice == "3":
                print("📡 جوڵەی دەنگەڕەش...")
                servo.oscillate(90, 30, 5, 1.5)
                
            elif choice == "4":
                print("🔢 زنجیرەی جوڵە...")
                angles = [0, 45, 90, 135, 180, 90, 45, 0]
                delays = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0]
                servo.sequence(angles, delays)
                
            elif choice == "5":
                try:
                    angle = int(input("➡️  پلە بنووسە (0-180): "))
                    servo.move_to_angle(angle)
                except ValueError:
                    print("❌ پلەی نادروست")
                    
            elif choice == "6":
                print("👋 کۆتایی هات")
                break
                
            else:
                print("❌ هەڵبژاردنی نادروست")
                
    except KeyboardInterrupt:
        print("\n❌ کۆتایی هات بە Ctrl+C")
        
    finally:
        servo.deinit()

# ئەنجامدانی بەرنامە
if __name__ == "__main__":
    main()