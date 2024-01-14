import RPi.GPIO as GPIO


class LightSensors:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def get_light_sensors_status(self):
        LMR = 0x00
        if self.left_sensor_high():
            print("Negro a la izquierda: " + str(LMR))
            LMR = (LMR | 4)
        if self.middle_sensor_high():
            print("Negro en medio: " + str(LMR))
            LMR = (LMR | 2)
        if self.right_sensor_high():
            print("Negro a la derecha: " + str(LMR))
            LMR = (LMR | 1)
        return LMR

    def right_sensor_high(self):
        return GPIO.input(self.IR03) == True

    def middle_sensor_high(self):
        return GPIO.input(self.IR02) == True

    def left_sensor_high(self):
        return GPIO.input(self.IR01) == True
