import struct
from typing import List, Tuple

def ler_cabecalho(arquivo: str) -> int:
    with open(arquivo, 'rb') as f:
        return int.from_bytes(f.read(4), byteorder='little')

def ler_registros(arquivo: str):
    registros = []
    with open(arquivo, 'rb') as f:
        quantidade_reg = ler_cabecalho(arquivo)
        f.seek(4)
        i = 0
        while i < quantidade_reg:
            offset = f.tell()
            tamanho = int.from_bytes(f.read(2), byteorder='little')
            registro = f.read(tamanho).decode('utf-8')
            registros.append((registro, offset))
            i = i+1
    return registros

def ler_registro(arquivo: str, offset: str) -> str:
    registros = []
    with open(arquivo, 'rb') as f:
        f.seek(offset)
        i = 0
        tamanho = int.from_bytes(f.read(2), byteorder='little')
        registro = f.read(tamanho).decode('utf-8')
        return registro
    return registros

def escrever_registro(arquivo: str, registro: str) -> int:
    with open(arquivo, 'ab') as f:
        f.seek(0, 2)
        offset = f.tell()
        tamanho = len(registro)
        f.write(tamanho.to_bytes(2, byteorder='little'))
        f.write(registro.encode('utf-8'))
        return offset

def clear_file(filename):
    with open(filename, 'r+') as file:
        file.truncate(0)

