FROM python:3.10

COPY app_engine.py .
COPY adn_image_procesor.py .
COPY bucket_repository.py .
COPY conf_initializer.py .
COPY db_repository.py .

CMD ["python", "app_engine.py"]