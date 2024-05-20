import pigpio
from time import sleep

class ServoControl:
    def __init__(self, pi, pin=16):
        self.pi = pi
        self.pin = pin
        self.pi.set_PWM_frequency(self.pin, 50)  # Configura la frecuencia PWM a 50 Hz para servos
        self.pi.set_servo_pulsewidth(self.pin, 0)  # Establece el servo en estado neutral

    def open_servo(self):
        self.pi.set_servo_pulsewidth(self.pin, 2500)  # Abre el servo
        print("Servo abierto")

    def close_servo(self):
        self.pi.set_servo_pulsewidth(self.pin, 1500)  # Cierra el servo
        print("Servo cerrado")

    def open_door(self):
        try:
            self.open_servo()  # Abre el servo
            sleep(10)  # Espera 10 segundos
            self.close_servo()  # Cierra el servo después de 10 segundos
            sleep(0.5)  # Espera 0.5 segundos
        finally:
            self.close_servo()  # Asegura que el servo esté cerrado
            self.stop()  # Detiene la instancia del servo

    def stop(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)  # Detiene el servo
        self.pi.stop()  # Detiene la conexión con el daemon de pigpio

# Configuración inicial
pi = pigpio.pi()
instancia_servo = ServoControl(pi)

if __name__ == "__main__":
    try:
        while 1:
            # Abre y cierra el servo en bucle
            instancia_servo.open_servo()
            print("Servo abierto")
            sleep(0.6)
            instancia_servo.close_servo()
            print("Servo cerrado")
            sleep(0.6)
            input("Pulsa una tecla para continuar")
    except:
        instancia_servo.close_servo()  # Cierra el servo en caso de excepción
        instancia_servo.stop()  # Detiene la instancia del servo

    finally:
        instancia_servo.close_servo()  # Cierra el servo al finalizar
        instancia_servo.stop()  # Detiene la instancia del servo al finalizar
