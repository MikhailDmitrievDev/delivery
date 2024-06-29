FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY /order_food /app/

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
RUN cd order_food

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "order_food.wsgi:application"]
