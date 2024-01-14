import time
import math
from PCA9685 import PCA9685
from ADC import *

SECONDS = 1


class Motor:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.setPWMFreq(50)
        self.time_proportion = 3  # Depend on your own car,If you want to get the best out of the rotation mode, change the value by experimenting.
        self.adc = Adc()

    def soft_turn_left(self):
        print("soft left")
        self.setMotorModel(-2000, -2000, 4000, 4000)

    def turn_left(self):
        print("left")
        self.setMotorModel(-1500, -1500, 2500, 2500)

    def turn_right(self):
        print("right")
        self.setMotorModel(2500, 2500, -1500, -1500)

    def soft_turn_right(self):
        print("soft right")
        self.setMotorModel(4000, 4000, -2000, -2000)

    def rotate_left(self, traction_factor=1):
        self.setMotorModel(-1000, -1000, 1000, 1000, traction_factor)

    def rotate_right(self, traction_factor=1):
        self.setMotorModel(1000, 1000, -1000, -1000, traction_factor)

    def stop(self):
        self.setMotorModel(0, 0, 0, 0)
        print("FINISH!!!")

    def slow(self):
        self.setMotorModel(300, 300, 300, 300)

    def go_straight(self):
        print("forward")
        self.setMotorModel(800, 800, 800, 800)

    def go_back(self):
        print("backward")
        self.setMotorModel(-800, -800, -800, -800)

    def duty_range(self, duty1, duty2, duty3, duty4):
        if duty1 > 4095:
            duty1 = 4095
        elif duty1 < -4095:
            duty1 = -4095

        if duty2 > 4095:
            duty2 = 4095
        elif duty2 < -4095:
            duty2 = -4095

        if duty3 > 4095:
            duty3 = 4095
        elif duty3 < -4095:
            duty3 = -4095

        if duty4 > 4095:
            duty4 = 4095
        elif duty4 < -4095:
            duty4 = -4095
        return duty1, duty2, duty3, duty4

    def left_Upper_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(0, 0)
            self.pwm.setMotorPwm(1, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(1, 0)
            self.pwm.setMotorPwm(0, abs(duty))
        else:
            self.pwm.setMotorPwm(0, 4095)
            self.pwm.setMotorPwm(1, 4095)

    def left_Lower_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(3, 0)
            self.pwm.setMotorPwm(2, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(2, 0)
            self.pwm.setMotorPwm(3, abs(duty))
        else:
            self.pwm.setMotorPwm(2, 4095)
            self.pwm.setMotorPwm(3, 4095)

    def right_Upper_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(6, 0)
            self.pwm.setMotorPwm(7, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(7, 0)
            self.pwm.setMotorPwm(6, abs(duty))
        else:
            self.pwm.setMotorPwm(6, 4095)
            self.pwm.setMotorPwm(7, 4095)

    def right_Lower_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(4, 0)
            self.pwm.setMotorPwm(5, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(5, 0)
            self.pwm.setMotorPwm(4, abs(duty))
        else:
            self.pwm.setMotorPwm(4, 4095)
            self.pwm.setMotorPwm(5, 4095)

    def setMotorModel(self, duty1, duty2, duty3, duty4, traction_factor=1):
        duty1 = duty1 * traction_factor
        duty2 = duty2 * traction_factor
        duty3 = duty3 * traction_factor
        duty4 = duty4 * traction_factor
        duty1, duty2, duty3, duty4 = self.duty_range(duty1, duty2, duty3, duty4)
        self.left_Upper_Wheel(duty1)
        self.left_Lower_Wheel(duty2)
        self.right_Upper_Wheel(duty3)
        self.right_Lower_Wheel(duty4)

    def Rotate(self, n):
        angle = n
        bat_compensate = 7.5 / (self.adc.recvADC(2) * 3)
        while True:
            W = 2000

            VY = int(2000 * math.cos(math.radians(angle)))
            VX = -int(2000 * math.sin(math.radians(angle)))

            FR = VY - VX + W
            FL = VY + VX - W
            BL = VY - VX - W
            BR = VY + VX + W

            PWM.setMotorModel(FL, BL, FR, BR)
            print("rotating")
            time.sleep(5 * self.time_proportion * bat_compensate / 1000)
            angle -= 5


PWM = Motor()


def loop():
    PWM.setMotorModel(2000, 2000, 2000, 2000)  # Forward
    time.sleep(SECONDS)
    PWM.setMotorModel(-2000, -2000, -2000, -2000)  # Back
    time.sleep(SECONDS)
    PWM.setMotorModel(-500, -500, 2000, 2000)  # Left
    time.sleep(SECONDS)
    PWM.setMotorModel(2000, 2000, -500, -500)  # Right
    time.sleep(SECONDS)
    PWM.setMotorModel(0, 0, 0, 0)  # Stop


def destroy():
    PWM.setMotorModel(0, 0, 0, 0)


if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
