from typing import Optional
from btree import ArvoreB
from file_manager import escrever_registro, ler_registro

def executar_operacoes(arquivo_operacoes: str, arvoreB: ArvoreB, arquivo_dados: str):
    with open(arquivo_operacoes, 'r') as f:
        for linha in f:
            rest = linha[1:]
            operacao = linha[0]
            if operacao == 'b':
                chave = int(rest.strip().split('|')[0])
                print(f'\nBusca pelo registro de chave {chave}\n')
                (achou, pageRrn, pos, offset) = arvoreB.buscarNaArvore(chave, arvoreB.get_raiz())
                if achou:
                    registro = ler_registro(arquivo_dados, offset)
                    print(f'{registro} ({len(registro)} - offset {offset})')
                else:
                    print(f'Registro de chave {chave} não encontrado!')
            elif operacao == 'i':
                chave = int(rest.strip().split('|')[0])
                registro = rest.strip()
                if registro[-1] == '\n':
                    registro = registro[:-1]

                print(f'\nInsercao do registro de chave {chave}\n')
                (achou, pageRrn, pos, offset) = arvoreB.buscarNaArvore(chave, arvoreB.get_raiz())
                if not achou:
                    offset = escrever_registro(arquivo_dados, registro)
                    arvoreB.gerenciadorDeInsercao(arvoreB.get_raiz(), [(chave, offset)])
                    print(f'{registro} ({len(registro)} - offset {offset})')
                else:
                    print(f'Erro: chave {chave} já existente!')
