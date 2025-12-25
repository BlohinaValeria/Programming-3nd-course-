# Server
FROM python:3.11 as server
WORKDIR /app
COPY server/requirements.txt .
RUN pip install -r requirements.txt
COPY server/ .
COPY proto/glossary.proto .
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto
CMD ["python", "grpc_server.py"]

# Client
FROM python:3.11 as client
WORKDIR /app
COPY client/requirements.txt .
RUN pip install -r requirements.txt
COPY client/ .
COPY proto/glossary.proto .
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto
CMD ["python", "web_client.py"]