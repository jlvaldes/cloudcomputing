#Script para leer y procesar imágenes de secuenciación de ADN
from bucket_repository import get_adn_image, get_adn_image_batch
from db_repository import save, save_batch

def image_processing():
    get_adn_image()
    print('Se procesó una imagen de secuenciación de cadena de ADN')
    save()
    return 0


def image_processing_batch():
    get_adn_image_batch()
    print('Se procesó un lote de imágenes de secuenciación de cadenas de ADN')
    save_batch()
    return 0