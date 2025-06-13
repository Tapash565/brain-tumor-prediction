FROM continuumio/miniconda3
WORKDIR /app
COPY . /app
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "brain-tumor", "/bin/bash", "-c"]
RUN conda config --add channels conda-forge
EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["conda", "run", "--no-capture-output", "-n", "brain-tumor", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]