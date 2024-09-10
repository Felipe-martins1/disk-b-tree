class Pagina:
    def __init__(self, ordem: int) -> None:
        self.numChaves: int = 0
        self.chaves: list = [None] * (ordem - 1)
        self.offsets: list = [None] * (ordem - 1)
        self.filhos: list = [None] * ordem
        self.ordem: int = ordem

    def existe_espaco(self) -> bool:
        return self.numChaves < (self.ordem - 1)

    def insere(self, chaveAndOffset: (int, int), filhoD: int):
        chave, offset = chaveAndOffset

        if not self.existe_espaco():
           self.chaves.append(None)
           self.offsets.append(None)
           self.filhos.append(None)
        
        i = self.numChaves

        while i > 0 and chave < self.chaves[i - 1]:
            self.chaves[i] = self.chaves[i - 1]
            self.offsets[i] = self.offsets[i - 1]
            self.filhos[i + 1] = self.filhos[i]
            i -= 1
        
        self.chaves[i] = chave
        self.offsets[i] = offset
        self.filhos[i + 1] = filhoD
        self.numChaves += 1


class ArvoreB:
    def __init__(self, filename, order):
        self.filename = filename
        self.order = order
        self.header_size = 4 
        self.tam_pag = 4 + (8 * (self.order - 1)) + (4 * self.order)

    def alterar_raiz(self, raiz: int):
        with open(self.filename, 'r+b') as f:
            f.seek(0)
            f.write(raiz.to_bytes(self.header_size, 'little'))

    def inserir(self, chave: (int, int), rrn: int):
        achou: bool
        pos: int
        pag: Pagina
        chavePro: (int, int)
        filhoDpro: int

        if(rrn == None):
            chavePro = chave
            filhoDpro = None
            return chavePro, filhoDpro, True

        pag = self.__lePagina(rrn)
        achou, pos = self.buscarNaPagina(chave[0], pag)
       
        if(achou):
            raise BaseException("Chave Duplicada.")

        chavePro, filhoDpro, promo = self.inserir(chave, pag.filhos[pos])
        
        if(not promo):
            return None, None, False
        
        if(pag.existe_espaco()):
            pag.insere(chavePro, filhoDpro)
            self.escrevePagina(rrn, pag)
            return None, None, False
        else:
            chavePro, filhoDpro, pagAnt, novaPag = self.divide(chavePro, filhoDpro, pag)
            self.escrevePagina(rrn, pagAnt)
            self.escrevePagina(filhoDpro, novaPag)
            return chavePro, filhoDpro, True


    def buscarNaPagina(self, chave: int, pag: Pagina):
        pos = 0
        while pos < pag.numChaves and (pag.chaves[pos] is None or chave > pag.chaves[pos]):
            pos += 1
        if pos < pag.numChaves and chave == pag.chaves[pos]:
            return True, pos
        else:
            return False, pos

    def buscarNaArvore(self, chave: int, pageRrn: int):
        if(pageRrn == None):
            return False, None, None, None
        else:
            pag: Pagina = self.__lePagina(pageRrn)
            achou, pos = self.buscarNaPagina(chave, pag)

            if(achou):
                offset = pag.offsets[pos]
                return True, pageRrn, pos, offset
            else:
                return self.buscarNaArvore(chave, pag.filhos[pos])

    def divide(self, chave: (int, int), filhoD: int, pag: Pagina):
        pag.insere(chave, filhoD)
        meio = self.order // 2
        chavePro = (pag.chaves[meio], pag.offsets[meio])

        filhoDpro = self.__novo_rrn()

        pAtual = Pagina(self.order)
        pNova = Pagina(self.order)

        for i in range(meio):
            pAtual.chaves[i] = pag.chaves[i]
            pAtual.offsets[i] = pag.offsets[i]
            pAtual.filhos[i] = pag.filhos[i]

        pAtual.filhos[meio] = pag.filhos[meio]

        for i in range(meio + 1, len(pag.chaves)):
            pNova.chaves[i - meio - 1] = pag.chaves[i]
            pNova.offsets[i - meio - 1] = pag.offsets[i]
            pNova.filhos[i - meio - 1] = pag.filhos[i]

        pAtual.numChaves = len([chave for chave in pAtual.chaves if chave is not None])
        pNova.numChaves = len([chave for chave in pNova.chaves if chave is not None])

        return chavePro, filhoDpro, pAtual, pNova

    def gerenciadorDeInsercao(self, raiz, chaves):
        for chave in chaves:
            chaveAndOffsetPro, filhoDpro, promocao = self.inserir(chave, raiz)

            (chavePro, offsetPro) = (None, None) if chaveAndOffsetPro == None else chaveAndOffsetPro

            if promocao:
                pNova = Pagina(self.order)
                pNova.chaves[0] = chavePro
                pNova.offsets[0] = offsetPro
                pNova.filhos[0] = raiz
                pNova.filhos[1] = filhoDpro
                pNova.numChaves += 1
                novo_rrn = self.__novo_rrn()
                self.escrevePagina(novo_rrn, pNova)
                raiz = novo_rrn
        return raiz


    def get_raiz(self):
        with open(self.filename, 'rb') as f:
            return int.from_bytes(f.read(self.header_size), 'little')

    def __calc_rrn(self, rrn: int):
        return self.header_size + rrn * self.tam_pag

    def __lePagina(self, rrn: int) -> Pagina:
        with open(self.filename, 'rb') as f:
            f.seek(self.__calc_rrn(rrn))
            pag = Pagina(self.order)
            pag.numChaves = int.from_bytes(f.read(4), 'little')

            i = 0
            while (i < (self.order - 1)):
                if(pag.numChaves == 0):
                    pag.chaves[i] = None
                else:
                    chave = int.from_bytes(f.read(4), 'little', signed=True)
                    pag.chaves[i] = chave if chave != -1 else None
                i += 1
            
            i = 0
            while (i < (self.order - 1)):
                if(pag.numChaves == 0):
                    pag.offsets[i] = None
                else:
                    offset = int.from_bytes(f.read(4), 'little', signed=True)
                    pag.offsets[i] = offset if offset != -1 else None
                i += 1
            
            i = 0
            while (i < self.order):
                filho = int.from_bytes(f.read(4), 'little', signed=True)
                pag.filhos[i] = filho if filho != -1 else None
                i += 1
            return pag

    def escrevePagina(self, rrn: int, pag: Pagina):
        with open(self.filename, 'r+b') as f:
            f.seek(self.__calc_rrn(rrn))
            f.write(pag.numChaves.to_bytes(4, 'little'))
            for chave in pag.chaves:
                chaveToWrite = -1 if chave == None or chave == 0 else chave
                f.write(chaveToWrite.to_bytes(4, 'little', signed=True))

            for offset in pag.offsets:
                offsetToWrite = -1 if offset == None or offset == 0 else offset
                f.write(offsetToWrite.to_bytes(4, 'little', signed=True))
                
            for filho in pag.filhos:
                filhoToWrite = -1 if filho == None else filho
                f.write(filhoToWrite.to_bytes(4, 'little', signed=True))

    def __novo_rrn(self) -> int:
        with open(self.filename, 'r+b') as f:
            f.seek(0, 2)
            offset = f.tell()
            return (offset - self.header_size) // self.tam_pag

    def imprimir_arvore(self, raiz):
        self.__imprimir_pagina(raiz, True)  # Chama a raiz, indicando que é a raiz
        print("-" * 29)  # Linha separadora final após a impressão da árvore

    def __imprimir_pagina(self, rrn: int, is_raiz: bool):
        print('\n')
        pag = self.__lePagina(rrn)
       
        chaves_str = ' | '.join(str(chave) for chave in pag.chaves[:pag.numChaves] if chave is not None)
        offsets_str = ' | '.join(str(offset) for offset in pag.offsets[:pag.numChaves] if offset is not None)
        filhos_str = ' | '.join(str(filho if filho is not None else -1) for filho in pag.filhos[:pag.numChaves + 1])

        if is_raiz:
            print("- - - - - - Raiz - - - - - -")
        
        print(f"Página {rrn}")
        print(f"Chaves: {chaves_str}")
        print(f"Offsets: {offsets_str}")
        print(f"Filhas: {filhos_str}")

        if is_raiz:
            print("- - - - - - - - - - - - - - -")

        for i in range(pag.numChaves + 1):
            if pag.filhos[i] is not None:
                self.__imprimir_pagina(pag.filhos[i], False)
            

            