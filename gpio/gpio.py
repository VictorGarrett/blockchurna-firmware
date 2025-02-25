import RPi.GPIO as rpGPIO


class GPIO:
    
    def __init__(self):
        # Configuração inicial dos GPIOs
        rpGPIO.setmode(rpGPIO.BCM)  # Usar a numeração BCM
        rpGPIO.setwarnings(False)  # Desativar avisos

        # Definir os pinos usados
        self.GPIO_BRANCO = 18  # 24
        self.GPIO_CONFIRMA = 24 # 23
        self.GPIO_CORREGE = 23  # 18

        # Configurar os pinos como entrada com pull-up
        rpGPIO.setup(self.GPIO_BRANCO, rpGPIO.IN, pull_up_down=rpGPIO.PUD_UP)
        rpGPIO.setup(self.GPIO_CONFIRMA, rpGPIO.IN, pull_up_down=rpGPIO.PUD_UP)
        rpGPIO.setup(self.GPIO_CORREGE, rpGPIO.IN, pull_up_down=rpGPIO.PUD_UP)


    def gpio_check(self, pin):
        return rpGPIO.input(pin) == rpGPIO.LOW
    
gpio = GPIO()
