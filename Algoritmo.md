# Algoritmo

## Resumo

O algoritmo funciona por brute force. Porém, existem algumas validações que aceleram o esforço computacional que ele necessita, como restrição do domínio de notas; retirada prévia de casos que realmente não existem possibilidades de notas; para o cálculo de uma nota apenas, retorno do melhor caso; entre outros aspectos posteriormente explicados.

## Definição das Entidades

### 1. Nota

A classe `Nota` possui 3 atributos: `peso`, `valor` e `dominio_de_nota`. O `peso` representa o peso total daquela nota em relação à média final disciplina. O `valor` representa o quanto o aluno tirou naquela prova/trabalho. E o `dominio_de_nota` representa quais são os possíveis valores para aquela nota ([0, 0.5, 1, 1.5, ..., 9.5, 10] ou alguma sublista deste domínio maior). Esta variável é inicializada como sendo o valor da lista mencionada (armazenada em `DOMINIO_DE_NOTAS` da mesma classe). Ela serve para definir os possíveis valores de notas que aquela prova pode possuir para atingir a média desejada. Esta definição pode diminuir as possibilidades que esta nota pode ter, reduzindo o esforço computacional.

Ela possui validação para os seguintes atributos:

1. `valida_valor`: verifica se o este atributo recebido é `float` ou `int`; e se o valor pertence ao `DOMINIO_DE_NOTAS`;

2. `valida_peso`: verifica se o peso é None (necessariamente a nota precisa ter um peso); se o peso é `float`, e se o peso está entre o seguinte intervalo: [0, 1]

Além disso, ela possui alguns métodos:

1. `randomiza_dominio`: pega a lista `dominio_da_nota` e a randomiza;

2. `limita_dominio`: pega um valor mínimo e máximo escolhido no input, e faz uma secção da lista `dominio_da_nota`. Vale ressalta que esta lista deve ser a geral (ou seja, uma cópia de `DOMINIO_DE_NOTAS`), além de não estar randomizada. Esta validação é feita pelo método `valida_limitacao_de_dominio`;

3. `restaura_dominio`: volta o domínio da nota para o original (cópia de `DOMINIO_DE_NOTAS`);

4. `valida_limitacao_de_dominio`: valida se o `dominio_da_nota` está no formato original (ou seja, se ele não foi seccionado ainda); se o input `valor_máximo` realmente é maior que o input `valor_minimo`; e se o domíno já não foi randomizado.

### 2. Utils

Esta classe tem a funcionalidade de apresentar funções que o algorítmo utiliza, como cálculo de médias, desvio padrão, e funções utilizadas no debug do código (como a exibição de uma lista de notas). Os métodos de debug não serão comentados nesta descrição, mas podem ser vistos na classe. 

Os métodos que esta classe possui são:

1. `media_aritimetica`: faz o cálculo da média aritimética das notas (sem considerar os pesos entre elas);

2. `media`: calcula a média ponderada entre as notas, validando se as notas possuem a soma dos seus pesos igual a 1.

3. `desvio_padrao`: calcula o desvio padrão entre as notas, utilizando-se do método anterior `media`;

4. `distancia_entre_notas`: verifica se todas as notas distam de um valor `distancia_min` da média aritimética entre as notas (para verificar a dispersão entre as notas);

5. `minimo_valor_no_dominio`: verifica qual o menor valor que a nota pode ter para ser possível com que a média desejada seja atingida. O cálculo da equação utilizada por esta função estará descrito no tópico "Lógica do algorítmo". Se o valor fornecido for menor que o menor valor mínimo de uma nota (0.0), a função retorna "0.0". Caso o valor fornecido seja maior que o maior valor que uma nota pode ter (10.0), esta função retorna "-1", indicando que é impossível encontrar uma possibilidade que a média desejada seja atingida;

6. `maximo_valor_no_dominio`: verifica qual o maior valor que a nota pode ter para ser possível com que a média desejada seja atingida. O cálculo da equação utilizada por esta função estará descrito no tópico "Lógica do algorítmo". Se o valor fornecido for maior que o maior valor máximo de uma nota (10.0), a função retorna "10.0". Não há uma validação para se existe uma possibilidade do valor máximo ser menor que "0.0", uma vez que o próprio algoritmo verifica a melhor possibilidade, e encontrará que esta nota deve ser "0.0"; 

### Boletim

O boletim possui 4 atributos: `tenho`, que representa uma lista de notas que tenho; `quero`, que representa uma lista de notas que quero; `idx_tenho` que representa o index na lista `tenho` do primeiro trabalho na lista (se for igual ao tamanho da lista representa que não tem trabalho); e `idx_quero` que tem a mesma ideia de `idx_tenho` só que para a lista `quero`. Esta classe foi criada a fim de se separar a lista de provas com a lista de trabalhos, possuindo algumas características que esta divisão necessita, como a média das provas, média dos trabalhos, entre outros. Ela foi criada justamente por uma descoberta de que o sistema que calcula a média final faz a média de provas e a média de trabalhos separadas, arrendondando elas, e após isso faz a média final.

Os métodos implementados nesta classe são:

1. `media_final`


## Lógica do algoritmo

