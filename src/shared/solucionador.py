from datetime import time
from typing import List, Dict
from src.shared.domain.entities.boletim import Boletim

from src.shared.domain.entities.nota import Nota
from src.shared.helpers.functions.utils import Utils

from itertools import product


class Solucionador:
    NOTAS_TOTAIS = 1  # quantidade de notas que o programa escolherá e parará ao encontrá-los
    MENOR_DIST = 1.5  # menor distância entre notas escolhidas e a média aritimética entre elas
                    # para que sejam escolhidas pelo algorítmo
    ERR_MAX = 0.04  # erro máximo permitido entre a média das notas escolhidas e a média desejada
    PRIMEIRO_PASSO = 0.5  # primeiro passo para aumentar o range de média desejada
    PASSO = 0.5 # passo para aumentar o range de média desejada
    
    @staticmethod
    def algoritmo(boletim: Boletim,  media_desejada: float) -> Boletim:
        
        aumento_range = 0
                
        # variável que representa a quantidade de notas que quero calcular 
        tamanho_notas_que_quero = len(boletim.quero_peso_global())

        # lista que conterá as notas possíveis de serem retornadas
        notas_possiveis = list()

        # Se não for possível atingir tal nota, retornará uma lista vazia
        # ex: se o aluno escolher média 10, e tirou 0 em alguma nota, esse "if" captará
        # obs: Nota.DOMINIO_DE_NOTAS[-1] = 10
        if (Boletim.media_final_externo(idx_tenho=boletim.idx_tenho, 
                                        idx_quero=boletim.idx_quero, 
                                        tenho=boletim.tenho, 
                                        quero=[Nota(valor=Nota.DOMINIO_DE_NOTAS[-1],
                                                    peso=nota.peso) for nota in boletim.quero], 
                                        peso_prova=boletim.peso_prova, 
                                        peso_trabalho=boletim.peso_trabalho) < media_desejada):
                                                    
            return None

        # Verifica se existe combinações para médias maiores que a pedida,
        # mas não existem combinações para o intervalo da média desejada
        while(media_desejada + aumento_range <= Nota.DOMINIO_DE_NOTAS[-1]):
       
            # garantia de que os domínios estão no valor original
            for nota in boletim.quero:
                nota.restaura_dominio()
            
            # limitando o domínio de cada nota
            for idx, nota in enumerate(boletim.quero):
                tenho_peso_global = boletim.tenho_peso_global()
                quero_peso_global = boletim.quero_peso_global()
                # seleciona o mínimo valor de cada nota para que seja possível calcular uma média válida
                valor_minimo = Utils.minimo_valor_no_dominio(notas_que_tenho=tenho_peso_global,
                                                            notas_que_quero=quero_peso_global[:idx] + \
                                                                            quero_peso_global[idx + 1:],
                                                            peso_especifico=quero_peso_global[idx].peso, 
                                                            media_desejada=media_desejada,
                                                            erro_max=Solucionador.ERR_MAX, 
                                                            distancia_max=Solucionador.MENOR_DIST,
                                                            aumento_do_range=aumento_range)

                # se `valor_minimo` for igual a -1, significa que não é possível atingir a média desejada
                if (valor_minimo == -1):
                    return None

                # Para o cálculo de uma nota apenas, e quando `valor_minimo` for encontrado, este será o valor da nota procurada
                if(tamanho_notas_que_quero == 1):
                    boletim.quero[0].valor = valor_minimo
                    return boletim
                
                # seleciona um máximo valor de cada nota para que seja possível calcular uma média válida
                valor_maximo = Utils.maximo_valor_no_dominio(notas_que_tenho=tenho_peso_global,
                                                                notas_que_quero=quero_peso_global[:idx] + quero_peso_global[
                                                                                                        idx + 1:],
                                                                peso_especifico=quero_peso_global[idx].peso, media_desejada=media_desejada,
                                                                erro_max=Solucionador.ERR_MAX+aumento_range, distancia_max=Solucionador.MENOR_DIST)

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

            # O loop 'while' externo (while media_desejada + aumento_range <= 10.0) ainda existe
            # para controlar o aumento do range de busca.
            # O codigo abaixo substitui APENAS o loop 'while' interno que gerava as combinacoes.

            # Cria uma lista de listas. Cada lista interna contem todas as notas possiveis
            # (o dominio) para uma das notas que queremos descobrir.
            # Ex: [[5.0, 5.5, 6.0], [7.0, 7.5]] para duas notas.
            dominios = [nota.dominio_da_nota for nota in boletim.quero]

            # O product recebe as listas de dominios e gera UMA combinacao completa por vez.
            # Isso substitui toda a logica manual de indices (idx_possiveis_notas) do 'while'.
            # O '*' antes de 'dominios' desempacota a lista, tratando cada dominio como um argumento separado.
            for combinacao in product(*dominios):
                
                # Dentro deste loop, 'combinacao' e uma tupla com uma solucao candidata.
                # Ex: (5.5, 7.0)

                # Pega os valores da tupla 'combinacao' e os atribui as notas que queremos descobrir
                # no objeto 'boletim'.
                for i, valor_nota in enumerate(combinacao):
                    boletim.quero[i].valor = valor_nota

                # Calcula a media final para a combinacao atual que foi carregada no boletim.
                media = boletim.media_final()

                # Verifica se a media calculada esta dentro do intervalo de busca aceitavel.
                # O limite superior deste intervalo cresce com o 'aumento_range'.
                if (media_desejada - Solucionador.ERR_MAX <= media <= media_desejada + Solucionador.ERR_MAX + aumento_range):
                    
                    # Se a media e valida, verifica o criterio de proximidade entre as notas.
                    if (Utils.distancia_entre_notas(boletim.quero, Solucionador.MENOR_DIST)):
                        
                        # Se todos os criterios passaram, armazena esta combinacao como uma solucao viavel.
                        combinacao_possivel = [Nota(peso=nota.peso, valor=nota.valor) for nota in boletim.quero]
                        notas_possiveis.append(tuple(combinacao_possivel))

                # Se o numero de solucoes viaveis encontradas atingiu o nosso objetivo (NOTAS_TOTAIS),
                # o 'break' interrompe o loop 'for'. Nao ha necessidade de testar mais milhoes de combinacoes.
                if (len(notas_possiveis) == Solucionador.NOTAS_TOTAIS):
                    break # Sai do loop 'for'

            # Este bloco so e executado se o loop encontrou pelo menos uma solucao.
            if (len(notas_possiveis) > 0):
                
                # Assume a primeira solucao como a melhor inicialmente.
                melhor_combinacao = notas_possiveis[0]
                
                # Itera sobre as outras solucoes encontradas para ver se alguma e melhor.
                for idx_nota in range(1, len(notas_possiveis)):
                    
                    # O criterio de desempate principal e o desvio padrao (preferimos notas mais proximas).
                    if(round(Utils.desvio_padrao(notas_possiveis[idx_nota]), 4) == round(Utils.desvio_padrao(melhor_combinacao), 4)):
                        if(
                            Boletim.media_final_externo(
                                idx_tenho=boletim.idx_tenho,
                                idx_quero=boletim.idx_quero,
                                tenho=boletim.tenho,
                                quero=list(notas_possiveis[idx_nota]),
                                peso_prova=boletim.peso_prova,
                                peso_trabalho=boletim.peso_trabalho
                            ) < Boletim.media_final_externo(
                                idx_tenho=boletim.idx_tenho,
                                idx_quero=boletim.idx_quero,
                                tenho=boletim.tenho,
                                quero=list(melhor_combinacao),
                                peso_prova=boletim.peso_prova,
                                peso_trabalho=boletim.peso_trabalho    
                            )
                        ):
                            melhor_combinacao = notas_possiveis[idx_nota]
                    # Se o desvio padrao da combinacao atual for menor, ela se torna a nova melhor.
                    elif (Utils.desvio_padrao(notas_possiveis[idx_nota]) < Utils.desvio_padrao(melhor_combinacao)):
                        melhor_combinacao = notas_possiveis[idx_nota]
                        
                # Carrega a melhor combinacao encontrada no boletim e o retorna como a resposta final.
                boletim.quero = list(melhor_combinacao)
                return boletim

            # primeira soma do `aumento_range`, para tornar a média desejada inteira
            if((media_desejada + Solucionador.ERR_MAX + aumento_range)*2 % 1 != 0):
                aumento_range += round(Solucionador.PRIMEIRO_PASSO - (media_desejada + Solucionador.ERR_MAX + aumento_range) % 1,  2)

            else:
                aumento_range += Solucionador.PASSO
                
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
