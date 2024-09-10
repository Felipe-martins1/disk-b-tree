import sys
from btree import ArvoreB, Pagina
from file_manager import ler_registros, clear_file
from operations import executar_operacoes
import os
import traceback

ORDEM = 5
ARQUIVO_BTREE = 'btree.dat'
ARQUIVO_GAMES = 'games.dat'

def principal(chaves):
    arvore = ArvoreB(ARQUIVO_BTREE, ORDEM)

    if os.path.exists(ARQUIVO_BTREE):
        clear_file(ARQUIVO_BTREE)
 
    with open(ARQUIVO_BTREE, 'w+b') as arqArvb:
        raiz = 0
        arqArvb.write(raiz.to_bytes(4, 'little'))
        pag = Pagina(ORDEM)
        arvore.escrevePagina(raiz, pag)
   
    raiz = arvore.gerenciadorDeInsercao(raiz, chaves)
    arvore.alterar_raiz(raiz)
    print(f"Raiz atualizada para: {raiz}")


def criar_indice():
    try:
        registros = ler_registros(ARQUIVO_GAMES)
        
        chaves = []
        
        for i, (registro, offset) in enumerate(registros):
            campos = registro.split('|')
            chave = int(campos[0])
            chaves.append((chave, offset))
            
        principal(chaves)
        print("Índice criado com sucesso.")
    except Exception as e:
         print(traceback.format_exc())


def main():
    if len(sys.argv) < 2:
        print("Uso: programa -c|-e|-p [arquivo_operacoes]")
        return

    opcao = sys.argv[1]

    if opcao == '-c':
        criar_indice()
    elif opcao == '-e':
        if len(sys.argv) != 3:
            print("Erro: arquivo de operações não especificado.")
            return
        arquivo_operacoes = sys.argv[2]
        btree = ArvoreB(ARQUIVO_BTREE, ORDEM)
        executar_operacoes(arquivo_operacoes, btree, ARQUIVO_GAMES)
    elif opcao == '-p':
        btree = ArvoreB(ARQUIVO_BTREE, ORDEM)
        btree.imprimir_arvore(btree.get_raiz())
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
