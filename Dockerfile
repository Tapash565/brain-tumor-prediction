FROM python:3.10.18
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--workers=2", "--bind", "0.0.0.0:5000", "app:app"]