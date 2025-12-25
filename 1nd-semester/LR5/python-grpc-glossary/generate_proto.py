#!/usr/bin/env python3
import subprocess
import os

def generate_proto():
    # Генерируем для сервера
    print("Generating proto files for server...")
    subprocess.run([
        'python', '-m', 'grpc_tools.protoc',
        '-I./proto',
        '--python_out=./server',
        '--grpc_python_out=./server',
        './proto/glossary.proto'
    ])
    
    # Генерируем для клиента
    print("Generating proto files for client...")
    subprocess.run([
        'python', '-m', 'grpc_tools.protoc',
        '-I./proto',
        '--python_out=./client',
        '--grpc_python_out=./client',
        './proto/glossary.proto'
    ])
    
    print("Proto files generated successfully!")

if __name__ == '__main__':
    generate_proto()