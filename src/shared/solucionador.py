from datetime import time
from typing import List, Dict

from src.shared.domain.entities.Nota import Nota
from src.shared.helpers.functions.utils import Utils


class Solucionador:
    NOTAS_TOTAIS = 20  # quantidade de notas que o programa escolherá e parará ao encontrá-los
    MENOR_DIST = 3  # menor distância entre notas escolhidas e a média aritimética entre elas
    # para que sejam escolhidas pelo algorítmo
    ERR_MAX = 0.04  # erro máximo permitido entre a média das notas escolhidas e a média desejada

    @staticmethod
    def algoritmo(notas_que_tenho: List[Nota], notas_que_quero: List[Nota], media_desejada: float) -> List[Nota]:
        # variável que representa o tamanho da lista `notas_que_quero`
        tamanho_notas_que_quero = len(notas_que_quero)

        # variável que representa o tamanho da lista `notas_que_tenho`
        tamanho_notas_que_tenho = len(notas_que_tenho)

        # lista que conterá as notas possíveis de serem retornadas
        notas_possiveis = list()

        # Se não for possível atingir tal nota, retornará uma lista vazia
        # ex: se o aluno escolher média 10, e tirou 0 em alguma nota, esse "if" captará
        # obs: Nota.DOMINIO_DE_NOTAS[-1] = 10
        if (Utils.media(notas_que_tenho + [Nota(peso=notas_que_quero[i].peso, valor=Nota.DOMINIO_DE_NOTAS[-1]) for i in
                                           range(tamanho_notas_que_quero)]) - media_desejada < 0):
            return []

        # Caso em que nenhuma nota foi pedida para ser calculada
        if (len(notas_que_quero) == 0):
            raise Exception("Para o uso do algorítmo, deve ser pedido alguma nota para ser calculada")

        # Caso em que foi pedido apenas uma nota
        if (len(notas_que_quero) == 1):
            # seleciona o mínimo valor para a nota; a partir dela será determinada a nota mínima que o aluno deve ter
            # obs: o argumento `notas_que_quero` representa as notas que quero além da nota em que está sendo analisado o domínio
            valor_minimo = Utils.minimo_valor_no_dominio(notas_que_tenho=notas_que_tenho, notas_que_quero=[],
                                                         peso_especifico=notas_que_quero[0].peso,
                                                         media_desejada=media_desejada, erro_max=Solucionador.ERR_MAX,
                                                         distancia_max=Solucionador.MENOR_DIST)

            # se `valor_minimo` for igual a -1, significa que não é possível atingir a média desejada
            if (valor_minimo == -1):
                return []

            # `valor_minimo` foi encontrado, sendo este o valor da nota procurada
            else:
                notas_que_quero[0].valor = valor_minimo
                return list(notas_que_quero)

        # Caso em que foi pedido um conjunto de notas maior que uma
        else:
            # limitando o domínio de cada nota
            for idx, nota in enumerate(notas_que_quero):

                # seleciona o mínimo valor de cada nota para que seja possível calcular uma média válida
                valor_minimo = Utils.minimo_valor_no_dominio(notas_que_tenho=notas_que_tenho,
                                                             notas_que_quero=notas_que_quero[:idx] + notas_que_quero[
                                                                                                     idx + 1:],
                                                             peso_especifico=nota.peso, media_desejada=media_desejada,
                                                             erro_max=Solucionador.ERR_MAX, distancia_max=Solucionador.MENOR_DIST)

                # se `valor_minimo` for igual a -1, significa que não é possível atingir a média desejada
                if (valor_minimo == -1):
                    return []

                # seleciona um máximo valor de cada nota para que seja possível calcular uma média válida
                valor_maximo = Utils.maximo_valor_no_dominio(notas_que_tenho=notas_que_tenho,
                                                             notas_que_quero=notas_que_quero[:idx] + notas_que_quero[
                                                                                                     idx + 1:],
                                                             peso_especifico=nota.peso, media_desejada=media_desejada,
                                                             erro_max=Solucionador.ERR_MAX, distancia_max=Solucionador.MENOR_DIST)

                # limitando o domínio da nota
                nota.limita_dominio(valor_minimo, valor_maximo)

        # embaralhamento dos dominios das notas que quero
        for nota in notas_que_quero:
            nota.randomiza_dominio()

        # lista que conterá o index da vez de análse da função, começando com [0,0,0, ...]
        # com o tamanho dependendo da quantidade de notas que o programa quer calcular
        idx_possiveis_notas = [0 for _ in range(tamanho_notas_que_quero)]

        # lista de notas que quero determinar, utilizando a lista de domínios
        # de notas para montá-las formando, assim, uma combinação de notas
        for idx, nota in enumerate(notas_que_quero):
            nota.valor = nota.dominio_da_nota[idx_possiveis_notas[idx]]

        # variável que representa que todas as notas foram verificadas
        todas_as_notas_verificadas = False

        # rodará até encontrar 3 notas possíveis ou acabar as notas
        while (not todas_as_notas_verificadas):

            # verifica se chegou a iteração da última nota
            if (all([idx_possiveis_notas[idx] == len(notas_que_quero[idx].dominio_da_nota) - 1 for idx in
                     range(len(idx_possiveis_notas))])):
                todas_as_notas_verificadas = True

            # junção das notas que tenho com combinação previamente feita
            todas_as_notas = notas_que_tenho + notas_que_quero

            # cálculo da média desta iteração
            media = Utils.media(todas_as_notas)

            # verifica se a média varia de 0.04 em relação à média desejada
            if (abs(media - media_desejada) <= Solucionador.ERR_MAX):
                # verifica se todas as notas distam da média no máximo MENOR_DIST
                if (Utils.distancia_entre_notas(notas_que_quero, Solucionador.MENOR_DIST)):
                    combinacao_possivel = [Nota(peso=nota.peso, valor=nota.valor) for nota in notas_que_quero]
                    notas_possiveis.append(tuple(combinacao_possivel))

            # faz o break do laço se encontra NOTAS_TOTAIS como
            # tamanho da lista de combinações de notas possíveis
            if (len(notas_possiveis) == Solucionador.NOTAS_TOTAIS):
                melhor_combinacao = notas_possiveis[0]

                # lógica para verificar quais das combinações escolhidas
                # de notas possui o menor desvio padrão
                for nota in range(1, len(notas_possiveis)):
                    if (Utils.desvio_padrao(notas_possiveis[nota]) - media_desejada < Utils.desvio_padrao(
                            melhor_combinacao) - media_desejada):
                        melhor_combinacao = notas_possiveis[nota]
                return list(melhor_combinacao)

            # se não for possível parar o laço, adiciona 1 ao último index da lista de index
            # ex: [0, 0, 0, ..., 0, 0] --(+1)--> [0, 0, 0, ..., 0, 0]
            # ex2: [0, 0, 0, ..., 0, 19] --(+1)--> [0, 0, 0, ..., 0, 20] -> [0, 0, 0, ..., 1, 0]
            # ex3: [0, 0, 0, ..., 0, 19, 19] --(+1)--> [0, 0, 0, ..., 0, 19, 20] -> [0, 0, 0, ..., 0, 20, 0] ->
            # -> [0, 0, 0, ..., 1, 0, 0]
            idx_possiveis_notas[-1] += 1

            if (not all([nota.valor == nota.dominio_da_nota[-1] for nota in notas_que_quero])):
                for idx in list(range(len(idx_possiveis_notas)))[::-1]:
                    if (idx_possiveis_notas[idx] == len(notas_que_quero[idx].dominio_da_nota) and idx != 0):
                        # zera o valor do index da nota dessa iteração
                        idx_possiveis_notas[idx] = 0

                        # alterando o valor da nota dessa iteração para o primeiro valor do domínio
                        notas_que_quero[idx].valor = notas_que_quero[idx].dominio_da_nota[idx_possiveis_notas[idx]]

                        # aumentando o index da nota seguinte
                        idx_possiveis_notas[idx - 1] += 1
                    else:
                        # alterando valor da nota dessa iteração
                        notas_que_quero[idx].valor = notas_que_quero[idx].dominio_da_nota[idx_possiveis_notas[idx]]
                        break

        # se não encontrou nenhuma nota, retorna uma lista vazia
        if (len(notas_possiveis) == 0):
            return []

        # se encontrou alguma(s) combinação(ões) de nota(s), faz o cálculo
        # do desvio padrão e retorna a combinação com menor desvio padrão
        else:
            melhor_combinacao = notas_possiveis[0]
            for nota in range(1, len(notas_possiveis)):
                if (Utils.desvio_padrao(notas_possiveis[nota]) - media_desejada < Utils.desvio_padrao(
                        melhor_combinacao) - media_desejada):
                    melhor_combinacao = notas_possiveis[nota]
            return list(melhor_combinacao)

    # função que exibirá, pelos inputs passados, a lista de combinações de notas possíveis escolhidas pelo algorítmo
    @staticmethod
    def teste_algoritmo(notas_que_tenho: Dict[float, float], notas_que_quero: List[Nota],
                        media_desejada: float) -> None:
        t_inicial = time.time()
        notas_possiveis = Solucionador.algoritmo(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero,
                                           media_desejada=media_desejada)
        t_final = time.time()

        t_exec = t_final - t_inicial

        print("Para as notas:")
        Utils.print_lista_de_notas(notas_que_tenho)
        print(f" pesos:")
        Utils.print_pesos_de_notas(notas_que_quero)
        print(f", e média {media_desejada} uma combinação de notas possíveis é:")
        Utils.print_lista_de_notas(notas_possiveis)
        print(f"\nO algorítmo demorou {t_exec:.5f} segundos para executar.")
