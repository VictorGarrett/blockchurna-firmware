import RPi.GPIO as GPIO



class GPIO:
    
    def __init__(self):
        # Configuração inicial dos GPIOs
        GPIO.setmode(GPIO.BCM)  # Usar a numeração BCM
        GPIO.setwarnings(False)  # Desativar avisos

        # Definir os pinos usados
        self.GPIO_BRANCO = 17  
        self.GPIO_CONFIRMA = 27
        self.GPIO_CORREGE = 27     


        # Configurar os pinos como entrada com pull-up
        GPIO.setup(self.GPIO_BRANCO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_CONFIRMA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_CORREGE, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def gpio_check(self, pin):
        return GPIO.input(pin) == GPIO.LOW
