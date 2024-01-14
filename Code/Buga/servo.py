import time
from PCA9685 import PCA9685


class Servo:
    def __init__(self):
        self.PwmServo = PCA9685(0x40, debug=True)
        self.PwmServo.setPWMFreq(50)
        self.PwmServo.setServoPulse(8, 1500)
        self.PwmServo.setServoPulse(9, 1500)

    def celebrate(self):
        for i in range(30, 150):
            self.setServoPwm('0', i)
            time.sleep(0.01)
        for i in range(150, 90, -1):
            self.setServoPwm('0', i)
            time.sleep(0.01)

    def move_head_front(self):
        self.setServoPwm('0', 90)

    def move_head_right(self):
        self.setServoPwm('0', 150)

    def move_head_half_right(self):
        self.setServoPwm('0', 120)

    def move_head_left(self):
        self.setServoPwm('0', 30)

    def move_head_half_left(self):
        self.setServoPwm('0', 60)

    def setServoPwm(self, channel, angle, error=10):
        angle = int(angle)
        if channel == '0':
            self.PwmServo.setServoPulse(8, 2500 - int((angle + error) / 0.09))
        elif channel == '1':
            self.PwmServo.setServoPulse(9, 500 + int((angle + error) / 0.09))
        elif channel == '2':
            self.PwmServo.setServoPulse(10, 500 + int((angle + error) / 0.09))
        elif channel == '3':
            self.PwmServo.setServoPulse(11, 500 + int((angle + error) / 0.09))
        elif channel == '4':
            self.PwmServo.setServoPulse(12, 500 + int((angle + error) / 0.09))
        elif channel == '5':
            self.PwmServo.setServoPulse(13, 500 + int((angle + error) / 0.09))
        elif channel == '6':
            self.PwmServo.setServoPulse(14, 500 + int((angle + error) / 0.09))
        elif channel == '7':
            self.PwmServo.setServoPulse(15, 500 + int((angle + error) / 0.09))


# Main program logic follows:
if __name__ == '__main__':
    print("Now servos will rotate to 90°.")
    print("If they have already been at 90°, nothing will be observed.")
    print("Please keep the program running when installing the servos.")
    print("After that, you can press ctrl-C to end the program.")
    pwm = Servo()
    while True:
        try:
            pwm.setServoPwm('0', 90)
            pwm.setServoPwm('1', 90)
        except KeyboardInterrupt:
            print("\nEnd of program")
            break
