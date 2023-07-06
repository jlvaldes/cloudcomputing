# Aplicación para el procesamiento de información genética
from adn_image_procesor import image_processing
from conf_initializer import conf_init

def start_process():
    print('Inicio de procesamiento de cadenas de ADN')
    conf_init()
    image_processing()
    print('Finalización de procesamiento de cadenas de ADN')
    return 0


if __name__ == '__main__':
    start_process()