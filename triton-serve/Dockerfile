FROM nvcr.io/nvidia/tritonserver:22.08-tf2-python-py3
WORKDIR /app
COPY requirements.txt /tmp/
RUN pip install -U /tmp/requirements.txt
COPY . /app/
CMD tritonserver --model-repository /app/models