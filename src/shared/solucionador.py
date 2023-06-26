from datetime import time
from typing import List, Dict
from src.shared.domain.entities.boletim import Boletim

from src.shared.domain.entities.nota import Nota
from src.shared.helpers.functions.utils import Utils


class Solucionador:
    NOTAS_TOTAIS = 200  # quantidade de notas que o programa escolherá e parará ao encontrá-los
    MENOR_DIST = 3  # menor distância entre notas escolhidas e a média aritimética entre elas
    # para que sejam escolhidas pelo algorítmo
    ERR_MAX = 0.04  # erro máximo permitido entre a média das notas escolhidas e a média desejada
    aumento_range = 0  # aumento da média desejada para que o algorítmo encontre mais notas

    @staticmethod
    def algoritmo(boletim: Boletim,  media_desejada: float) -> Boletim:
        # variável que representa a quantidade de notas que quero calcular 
        tamanho_notas_que_quero = len(boletim.quero)

        # lista que conterá as notas possíveis de serem retornadas
        notas_possiveis = list()

        # Se não for possível atingir tal nota, retornará uma lista vazia
        # ex: se o aluno escolher média 10, e tirou 0 em alguma nota, esse "if" captará
        # obs: Nota.DOMINIO_DE_NOTAS[-1] = 10
        if (Utils.media(boletim.tenho + [Nota(peso=boletim.quero[i].peso, valor=Nota.DOMINIO_DE_NOTAS[-1]) for i in
                                           range(len(boletim.quero))]) - media_desejada < 0):
            return None


        # Verifica se existe combinações para médias maiores que a pedida,
        # mas não existem combinações para o intervalo da média desejada
        while(media_desejada + Solucionador.aumento_range <= Nota.DOMINIO_DE_NOTAS[-1]):
            
            # garantia de que os domínios estão no valor original
            for nota in boletim.quero:
                nota.restaura_dominio()
            
            # limitando o domínio de cada nota
            for idx, nota in enumerate(boletim.quero):

                # seleciona o mínimo valor de cada nota para que seja possível calcular uma média válida
                valor_minimo = Utils.minimo_valor_no_dominio(notas_que_tenho=boletim.tenho,
                                                            notas_que_quero=boletim.quero[:idx] + \
                                                                            boletim.quero[idx + 1:],
                                                            peso_especifico=nota.peso, 
                                                            media_desejada=media_desejada,
                                                            erro_max=Solucionador.ERR_MAX, 
                                                            distancia_max=Solucionador.MENOR_DIST,
                                                            aumento_do_range=Solucionador.aumento_range)

                # se `valor_minimo` for igual a -1, significa que não é possível atingir a média desejada
                if (valor_minimo == -1):
                    return None

                # Para o cálculo de uma nota apenas, e quando `valor_minimo` for encontrado, este será o valor da nota procurada
                if(tamanho_notas_que_quero == 1):
                    boletim.quero[0].valor = valor_minimo
                    return boletim
                
                # seleciona um máximo valor de cada nota para que seja possível calcular uma média válida
                valor_maximo = Utils.maximo_valor_no_dominio(notas_que_tenho=boletim.tenho,
                                                                notas_que_quero=boletim.quero[:idx] + boletim.quero[
                                                                                                        idx + 1:],
                                                                peso_especifico=nota.peso, media_desejada=media_desejada,
                                                                erro_max=Solucionador.ERR_MAX, distancia_max=Solucionador.MENOR_DIST)

                # limitando o domínio da nota
                nota.limita_dominio(valor_minimo, valor_maximo)

            # embaralhamento dos dominios das notas que quero
            for nota in boletim.quero:
                nota.randomiza_dominio()

            # lista que conterá o index da vez de análse da função, começando com [0,0,0, ...]
            # com o tamanho dependendo da quantidade de notas que o programa quer calcular
            idx_possiveis_notas = [0 for _ in range(tamanho_notas_que_quero)]

            # lista de notas que quero determinar, utilizando a lista de domínios
            # de notas para montá-las formando, assim, a combinação inicial de notas
            for idx, nota in enumerate(boletim.quero):
                nota.valor = nota.dominio_da_nota[idx_possiveis_notas[idx]]

            # variável que representa que todas as notas foram verificadas
            todas_as_notas_verificadas = False

            # rodará até encontrar `NOTAS_TOTAIS` notas possíveis ou acabar as notas
            while (not todas_as_notas_verificadas):

                # verifica se chegou a iteração da última nota
                if (all([idx_possiveis_notas[idx] == len(boletim.quero[idx].dominio_da_nota) - 1 for idx in
                        range(len(idx_possiveis_notas))])):
                    todas_as_notas_verificadas = True

                # cálculo da média desta iteração
                media = boletim.media_final()

                # verifica se a média varia de 0.04 em relação à média desejada
                if (media_desejada - Solucionador.ERR_MAX <= media and media <= media_desejada + Solucionador.ERR_MAX + Solucionador.aumento_range):
                    # verifica se todas as notas distam da média no máximo MENOR_DIST
                    if (Utils.distancia_entre_notas(boletim.quero, Solucionador.MENOR_DIST)):
                        combinacao_possivel = [Nota(peso=nota.peso, valor=nota.valor) for nota in boletim.quero]
                        notas_possiveis.append(tuple(combinacao_possivel))

                # faz o break do laço se encontra NOTAS_TOTAIS como
                # tamanho da lista de combinações de notas possíveis
                if (len(notas_possiveis) == Solucionador.NOTAS_TOTAIS):
                    melhor_combinacao = notas_possiveis[0]

                    # lógica para verificar quais das combinações escolhidas
                    # de notas possui o menor desvio padrão
                    for nota in range(1, len(notas_possiveis)):
                        if (Utils.desvio_padrao(notas_possiveis[nota]) - media_desejada < Utils.desvio_padrao(melhor_combinacao) - media_desejada):
                            
                            melhor_combinacao = notas_possiveis[nota]
                            
                    # adiciona a melhor combinação no boletim e retorna-o na saída do algoritmo
                    boletim.quero = list(melhor_combinacao)
                    return boletim

                # se não for possível parar o laço, adiciona 1 ao último index da lista de index
                # ex: [0, 0, 0, ..., 0, 0] --(+1)--> [0, 0, 0, ..., 0, 1]
                # ex2: [0, 0, 0, ..., 0, 19] --(+1)--> [0, 0, 0, ..., 0, 20] -> [0, 0, 0, ..., 1, 0]
                # ex3: [0, 0, 0, ..., 0, 19, 19] --(+1)--> [0, 0, 0, ..., 0, 19, 20] -> [0, 0, 0, ..., 0, 20, 0] ->
                # -> [0, 0, 0, ..., 1, 0, 0]
                
                idx_possiveis_notas[-1] += 1

                if (not all([nota.valor == nota.dominio_da_nota[-1] for nota in boletim.quero])):
                    for idx in list(range(len(idx_possiveis_notas)))[::-1]:
                        if (idx_possiveis_notas[idx] == len(boletim.quero[idx].dominio_da_nota) and idx != 0):
                            # zera o valor do index da nota dessa iteração
                            idx_possiveis_notas[idx] = 0

                            # alterando o valor da nota dessa iteração para o primeiro valor do domínio
                            boletim.quero[idx].valor = boletim.quero[idx].dominio_da_nota[idx_possiveis_notas[idx]]

                            # aumentando o index da nota seguinte
                            idx_possiveis_notas[idx - 1] += 1
                        else:
                            # alterando valor da nota dessa iteração
                            boletim.quero[idx].valor = boletim.quero[idx].dominio_da_nota[idx_possiveis_notas[idx]]
                            break


            # se encontrou alguma(s) combinação(ões) de nota(s), faz o cálculo
            # do desvio padrão e retorna a combinação com menor desvio padrão
            if (len(notas_possiveis) != 0):
                melhor_combinacao = notas_possiveis[0]
                for idx_nota in range(1, len(notas_possiveis)):
                    if(round(Utils.desvio_padrao(notas_possiveis[idx_nota]), 4) == round(Utils.desvio_padrao(melhor_combinacao), 4)):
                        if(
                            Boletim.media_final_externo(
                                idx_tenho=boletim.idx_tenho,
                                idx_quero=boletim.idx_quero,
                                tenho=boletim.tenho,
                                quero=list(notas_possiveis[idx_nota])
                            ) < Boletim.media_final_externo(
                                idx_tenho=boletim.idx_tenho,
                                idx_quero=boletim.idx_quero,
                                tenho=boletim.tenho,
                                quero=list(melhor_combinacao)    
                            )
                        ):
                            melhor_combinacao = notas_possiveis[idx_nota]
                    elif (Utils.desvio_padrao(notas_possiveis[idx_nota]) < Utils.desvio_padrao(melhor_combinacao)):
                        melhor_combinacao = notas_possiveis[idx_nota]
                boletim.quero = list(melhor_combinacao)
                return boletim

            # primeira soma do `aumento_range`, para tornar a média desejada inteira
            elif((media_desejada + Solucionador.ERR_MAX) % 1 != 0):
                Solucionador.aumento_range += round(1 - (media_desejada + Solucionador.ERR_MAX) % 1,  2)
                
            # a primeira soma `aumento_range` já foi feita
            else:
                Solucionador.aumento_range += 0.5
                
        # se não encontrou nenhuma nota, retorna uma lista vazia
        return None
        
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
        if(len(notas_possiveis) > 0):
            print(f"As notas possuem média {Utils.media(notas_possiveis+notas_que_tenho)}")
