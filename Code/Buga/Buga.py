from time import sleep

from Ultrasonic import *
from Motor import *
from Led import *
from ADC import *
from LightSensors import *

class Buga:

    def __init__(self):
        self.motor = Motor()
        self.servo = Servo()
        self.lightSensors = LightSensors()
        self.ultrasonic = Ultrasonic()
        self.led = Led()
        self.adc = Adc()

    def busca_camino(self):
        angle = 90
        esquerra: bool = True
        try:
            while True:
                distance = ultrasonic.get_distance()
                print("Objecte detectat a " + str(distance) + " cm")
                if distance < 30:
                    if angle == 30:
                        angle = 35
                        esquerra = False
                    elif angle == 150:
                        angle = 145
                        esquerra = True
                    else:
                        angle = angle - 5 if esquerra else angle + 5
                    self.servo.setServoPwm('0', angle)
                time.sleep(0.1)
                self.motor.setMotorModel(0, 0, 0, 0)
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            self.motor.setMotorModel(0, 0, 0, 0)
            self.servo.setServoPwm('0', 90)

    def encara_camino(self):
        angle = 90
        girs = 0
        esquerra: bool = True
        try:
            while True:
                distance = ultrasonic.get_distance()
                print("Objecte detectat a " + str(distance) + " cm")
                if distance < 30:
                    angle = self.motor.rotate_left(2) if esquerra else self.motor.rotate_right(2)
                    girs = girs + 1
                if girs > 9:
                    girs = 0
                    esquerra = not esquerra
                time.sleep(0.1)
                self.motor.stop()
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            self.motor.stop()
            self.servo.setServoPwm('0', 90)

    def sigue_camino(self):
        try:
            last = 0x00
            while True:
                LMR = self.lightSensors.get_light_sensors_status()

                print("LMR: {0} | last:{1}".format(LMR, last))
                if LMR == 0b000:
                    print("... searching track ...")
                    if last == 0b010:
                        self.motor.go_back()
                        self.led.backLights()
                    else:
                        LMR = last

                if LMR == 0b010:
                    self.servo.move_head_front()
                    self.motor.go_straight()
                    self.led.frontLights()
                elif LMR == 0b100:
                    self.servo.move_head_left()
                    self.motor.turn_left()
                    self.led.frontLeftLight()
                elif LMR == 0b110:
                    self.servo.move_head_half_left()
                    self.motor.soft_turn_left()
                    self.led.frontLeftLight()
                elif LMR == 0b001:
                    self.servo.move_head_right()
                    self.motor.turn_right()
                    self.led.frontRightLight()
                elif LMR == 0b011:
                    self.servo.move_head_half_right()
                    self.motor.soft_turn_right()
                    self.led.frontRightLight()
                elif LMR == 0b111:
                    self.motor.stop()
                    self.servo.celebrate()
                    self.led.frontLightsBlue()
                    distance = self.ultrasonic.get_distance()
                    print("Objecte detectat a " + str(distance) + " cm")
                    Power = self.adc.recvADC(2)
                    print("The battery voltage is " + str(Power * 3) + "V")
                    break

                last = LMR
                sleep(0.1)
        except KeyboardInterrupt:
            self.motor.stop()


if __name__ == '__main__':
    import sys

    buga = Buga()
    if len(sys.argv) < 2:
        print("Parameter error: Please assign the device")
        exit()
    if sys.argv[1] == 'b':
        buga.busca_camino()
    elif sys.argv[1] == 'e':
        buga.encara_camino()
    elif sys.argv[1] == 's':
        buga.sigue_camino()
