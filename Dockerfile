FROM continuumio/miniconda3:latest
WORKDIR /app
COPY . /app 
RUN conda env create -f environment.yaml
SHELL ["conda", "run", "-n", "venv", "/bin/bash", "-c"]
EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "4"]
CMD ["conda", "run", "--no-capture-output", "-n", "venv", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "4"]