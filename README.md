# Algoritmo

## Resumo

O algoritmo funciona por meio de um **Algoritmo Genético (AG)**. O AG busca uma combinação de notas futuras (provas e trabalhos) que minimize uma função de fitness, de forma iterativa e estocástica. Ele opera sobre uma população de soluções candidatas, evoluindo-as ao longo de gerações por meio de seleção, crossover e mutação, até convergir para a melhor solução encontrada.

## Definição das Entidades

### 1. Boletim_GA

A entidade `Boletim_GA` encapsula todas as informações necessárias para a execução do algoritmo. Seus atributos são:

- `current_tests`: lista de notas de provas que o aluno já possui;
- `current_assignments`: lista de notas de trabalhos que o aluno já possui;
- `num_remaining_tests`: quantidade de provas futuras a serem estimadas;
- `num_remaining_assignments`: quantidade de trabalhos futuros a serem estimados;
- `test_weight`: peso global das provas na média final (valor entre 0 e 1);
- `assignment_weight`: peso global dos trabalhos na média final (valor entre 0 e 1);
- `spec_test_weight`: lista de pesos individuais de cada prova (para média ponderada interna das provas);
- `spec_assignment_weight`: lista de pesos individuais de cada trabalho (para média ponderada interna dos trabalhos);
- `max_grade`: nota máxima possível (padrão: 10.0);
- `target_avg`: média final desejada (preenchida pelo usecase);
- `final_avg`: média final calculada pela solução encontrada (preenchida pelo usecase);
- `provas`: lista de dicionários com `valor` e `peso` de cada prova (todas, incluindo as já existentes), formatada para exibição no frontend;
- `trabalhos`: lista de dicionários com `valor` e `peso` de cada trabalho (todos, incluindo os já existentes), formatada para exibição no frontend;
- `message`: mensagem descritiva sobre a qualidade da solução encontrada.

### 2. GradeGeneticAlgorithm

Esta é a classe principal que implementa o algoritmo genético. É instanciada com um `Boletim_GA`, a média desejada e parâmetros de controle do AG (`population_size` e `generations`). Seus métodos são descritos a seguir.

## Lógica do Algoritmo

### Representação de um Indivíduo

Um **indivíduo** representa uma solução candidata: um conjunto de notas futuras de provas e trabalhos. Ele é estruturado como um dicionário com duas listas:

```python
{'tests': [nota_prova_1, nota_prova_2, ...], 'assignments': [nota_trabalho_1, ...]}
```

Cada valor é um número real no intervalo `[0, max_grade]`.

### Cálculo da Média Ponderada (`calculate_weighted_average`)

A média final é calculada em três etapas:

1. **Média das provas**: se `spec_test_weight` for fornecido, calcula-se a média ponderada das provas pelos seus pesos individuais; caso contrário, calcula-se a média aritmética simples.

2. **Média dos trabalhos**: análogo ao passo anterior, usando `spec_assignment_weight`.

3. **Média final**: combina as duas médias pelos pesos globais `test_weight` e `assignment_weight`:

$$\text{média\_final} = \text{média\_provas} \times w_{\text{prova}} + \text{média\_trabalhos} \times w_{\text{trabalho}}$$

Casos especiais são tratados: se não houver provas, retorna-se apenas a média dos trabalhos, e vice-versa.

### Função de Fitness (`fitness`)

A função de fitness avalia a qualidade de um indivíduo. Ela é **minimizada** e composta por três penalidades:

$$\text{fitness} = 10 \cdot |\text{média\_final} - \text{média\_alvo}| + 2 \cdot \sigma_{\text{notas\_futuras}} + 20 \cdot P_{\text{impossível}}$$

onde:

- $|\text{média\_final} - \text{média\_alvo}|$ penaliza o desvio em relação à média desejada (peso 10);
- $\sigma_{\text{notas\_futuras}}$ é o desvio padrão entre as notas futuras, penalizando soluções com notas muito dispersas (peso 2);
- $P_{\text{impossível}} = \sum \max(0,\, g - \text{max\_grade})$ penaliza notas que excedam o valor máximo permitido (peso 20).

### Inicialização da População (`create_individual`)

A população inicial é composta por `population_size` indivíduos gerados aleatoriamente. Cada nota futura é amostrada de uma distribuição uniforme no intervalo `[0, max_grade]`.

### Seleção (`selection`)

Utiliza-se **seleção por torneio** com tamanho de torneio igual a 3. Três indivíduos são amostrados aleatoriamente da população, e os dois de menor fitness são selecionados como pais.

### Crossover (`crossover`)

O crossover ocorre com probabilidade 0.8. É realizado separadamente para provas e trabalhos: escolhe-se um ponto de corte aleatório em cada lista e intercambiam-se os genes entre os dois pais, gerando dois filhos. Caso o crossover não ocorra, os filhos são cópias diretas dos pais.

### Mutação (`mutate`)

Cada nota futura de um indivíduo é mutada com probabilidade 0.2 por uma perturbação gaussiana de média 0 e desvio padrão 0.5. O valor resultante é clampado ao intervalo `[0, max_grade]`.

### Execução Principal (`run`)

O algoritmo executa o seguinte ciclo por `generations` gerações:

1. Calcula o fitness de todos os indivíduos da população atual;
2. Registra o melhor indivíduo já visto ao longo de todas as gerações (**elitismo global**);
3. Constrói a nova população:
   - Os 2 melhores indivíduos da geração atual são copiados diretamente (**elitismo local**);
   - Os demais são gerados por seleção, crossover e mutação até completar `population_size` indivíduos;
4. Ao final das gerações, calcula a média final do melhor indivíduo encontrado e o retorna junto com seu fitness.

### Pós-processamento no Usecase

Após o retorno do AG, o `GeneticAlgorithmUsecase` aplica as seguintes transformações antes de montar o `Boletim_GA` de resposta:

- **Arredondamento de notas** (`_round_grade_for_front`): arredonda para múltiplos de 0.5, sem arredondar para cima em casos de meio ponto (usa `ROUND_HALF_DOWN`), respeitando o padrão de exibição do sistema Mauá;
- **Arredondamento de pesos** (`_round_weight_for_front`): arredonda para uma casa decimal, também com `ROUND_HALF_DOWN`;
- **Classificação da solução**: com base na diferença `|média_final - média_alvo|`, a mensagem retornada é:
  - diferença ≤ 0.05: solução considerada válida;
  - diferença ≤ 0.20: solução considerada próxima;
  - diferença > 0.20: solução não satisfatória.

Se o AG retornar `None` como solução, o usecase lança o erro `CombinationNotFound`.

# Contribuidores 💰🤝💰

### Infra 🏗️
- Bruno Vilardi - [Brvilardi](https://github.com/Brvilardi) 👷‍♂️
- Hector Guerrini - [hectorguerrini](https://github.com/hectorguerrini) 🧙‍♂️
- Vitor Soller - [VgsStudio](https://github.com/VgsStudio) 🐱‍💻
- Luigi Trevisan - [LuigiTrevisan](https://github.com/LuigiTrevisan) 🍄

### Backend 🚪
- João Branco - [JoaoVitorBranco](https://github.com/JoaoVitorBranco) 😎

### Algoritmo ➕➖
- João Branco - [JoaoVitorBranco](https://github.com/JoaoVitorBranco) 😎
- Pedro Mesquita - [pedrogjmesquita](https://github.com/pedrogjmesquita) 💫
- Thomas Boehm - [ThomassBoehm](https://github.com/ThomassBoehm)


## Agradecimentos especiais 🙏

- [Dev. Community Mauá](https://www.instagram.com/devcommunitymaua/)
- [Clean Architecture: A Craftsman's Guide to Software Structure and Design](https://www.amazon.com.br/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [Institute Mauá of Technology](https://www.maua.br/)
