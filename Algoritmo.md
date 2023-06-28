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

O boletim possui 4 atributos: `tenho`, que representa uma lista de notas que tenho; `quero`, que representa uma lista de notas que quero; `idx_tenho` que representa o index na lista `tenho` do primeiro trabalho na lista (se for igual ao tamanho da lista representa que não tem trabalho); e `idx_quero` que tem a mesma ideia de `idx_tenho` só que para a lista `quero`. Ela recebe `provas_que_tenho`, `provas_que_quero`, `trabalhos_que_tenho` e `trabalhos_que_quero`, sendo todas listas de Nota. Esta classe foi criada a fim de se separar a lista de provas com a lista de trabalhos, possuindo algumas características que esta divisão necessita, como a média das provas, média dos trabalhos, entre outros. Ela foi criada justamente por uma descoberta de que o sistema que calcula a média final faz a média de provas e a média de trabalhos separadas, arrendondando elas, e após isso faz a média final.

Esta classe possui as seguintes validações:

1. `valida_lista_de_notas`: verifica se a lista de notas passadas são do tipo list(Nota);

2. `valida_preenchimento: para fazer o cálculo das médias, é verificado se as listas foram preenchidas, para que o usuário não faça uma média com notas vazias, uma vez que `quero` inicialmente é uma lista de notas com valor nulo (pois é o que o algoritmo quer encontrar);

3. `valida_pesos`: utilizado para verificar se todas as notas passadas possuem a soma de pesos igual a 1;

Os métodos implementados nesta classe são:

1. `provas`: retorna a lista das provas passadas no boletim, utilizando os atributos `idx_tenho` e `idx_quero`;

2. `trabalhos`: retorna a lista dos trabalhos passadas no boletim, utilizando os atributos `idx_tenho` e `idx_quero`;

3. `provas_que_quero`: retorna uma sublista de `quero` apenas com as provas, utilizando `idx_quero`; 

4. `trabalhos_que_quero`: retorna uma sublista de `quero`, apenas com os trabalhos, utilizando `idx_quero`;

5. `media_provas`: faz a média das provas, se utilizando do método `provas()`. Ele verifica se as provas foram preencidas ou não (ou seja, se as notas possuem valor);

6. `media_trabalhos`: faz a média dos trabalhos, se utilizando do método `trabalhos()`. Ele verifica se os trabalhos foram preencidos ou não (ou seja, se as notas possuem valor);

7. `media_final`: representa a média final a partir do boletim dado: calcula individualmente a média das provas e dos trabalhos (se utilizando dos métodos anteriores), e depois os soma para resultar na média final.

8. `media_final_externo`: calcula a média final para uma lista de notas que tenho e que quero externo ao objeto instantciado (sendo um método estático). Ele instancia um novo boletim com as tais notas e os respectivos indexes, e utiliza-se do método `media_final` para gerar a média final das notas passadas.


## Lógica do algoritmo

Como dito anteriormente, o algoritmo funciona por força bruta. A fim de ficar mais explícito o entendimento do código, os parágrafos a seguir serão separados pelo conjunto das linhas que eles estão explicando

### [22]
Cria-se uma lista para representar as possíveis combinações de notas escolhidas randomicamente.

### [27-29]
Primeiramente, ele faz a validação se é possível obter notas a fim de se atingir a média desejada, preenchendo todas as notas que o algoritmo bbusca pelo valor máximo que podem ter (10.0). Se o valor dessa média calculada for menor que o valor da média desejada, significa que não existem combinações possíveis nas quais a média desejada seja batida e, portanto, o algoritmo retorna `None`.

### [34]
Agora, se iniciará o primeiro laço de repetição. A classe Solucionador possui um atributo `aumento_range`, que aumentará conforme não se encontram notas possíveis para atingir uma certa nota (caso que ocorreu em um dos testes feitos). Imagina-se que, dentre as notas que o aluno já tem e as que ele quer tirar, não exista uma combinação possível para que ele tire 6.0, mas existe uma combinação para que tire 7.0. Este `loop` tem a funcionalidade de identificar estes casos. Se o algoritmo, até o máximo valor de uma média possível (10.0), não encontre uma combinação possível de notas, ele retorna `None` (linha 181).

Vale ressaltar que o `aumento_range` varia da seguinte forma: imagine-se que `media_desejada = 6.0`. Então, na primeira repetição, o valor mínimo de uma média possível é `6.0 - Solucionador.ERR_MAX = 6.0 - 0.05 = 5.96`, e o valor máximo de uma média possível é `6.0 + Solucionador.ERR_MAX = 6.0 + 0.04 = 6.04`. Se não foi encontrada nenhuma nota, o valor mínimo continua sendo `5.96`, mas deseja-se que o valor máximo seja `6.5`. Logo, o valor de `Solucionador.aumento_range` para que `6.04 + aumento_range = 6.5` é `0.46`. Após esta repetição, se não for encontrada nenhuma combinação, deseja-se que o valor máximo seja `7.0` e, para tal, `aumento_range = 0.96`, e assim por diante. 

### [37-38]
Para cada repetição (visto posteriormente), será feita uma limitação no domínio das notas. A explicação ficará mais clara futuramente, mas este trecho do código garante que para cada entrada no primeiro laço, os domínios voltem ao original (ou seja, as notas podem apresentar os seguintes valores: [0, 0.5, 1.0, ..., 9.5, 10.0], sendo este o domínio original).

### [44-70]
O trecho a seguir leva em conta o cálculo do mínimo e máximo valor que uma nota pode ter dentre as diversas possíveis (apresentadas no domínio original) para alcançar o valor máximo:

Assumindo que a separação entre prova e trabalho não existe, e assumindo $E_{rr}$ como sendo uma variável que representa o erro máximo que uma média final pode possuir (no caso 0.04, onde, por ex, para atingir uma média 6.0, é possível ter média 5.96 para cima que o sistema arredonda), e $n_x$ como sendo uma nota específica dentre as diversas que se quer analisar o domínio, a seguinte expressão define se uma combinação é possível ou não para atingir uma certa média final:

$$
abs\left(\sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i}+\sum_{i=0}^{len_{quero}-1}n_{quero_i}\cdot p_{quero_i}+n_x\cdot p_x - média \right) \le E_{rr} \:(I)
$$

Vale ressaltar que o mais preciso seria definir não pelo módulo, mas sim que essa diferença pode variar de -0.04 à 0. Porém, foi utilizado este conceito a fim de se facilitar as contas, sendo que o aumento do intervalo (-0.04 à +0.04) aceita mais combinações de notas, não invalidando a solução.

Inicialmente, se verificará qual é o valor mínimo que essa nota `n_x` deve possuir a fim de que seja possível se obter uma média final. Então, sabe-se que outra validação para que uma combinação de notas seja possível é representada pela seguinte expressão:

$$
abs(media_{quero} - n_{quero_{i}}) \le D_{máx} \:(II),
$$

na qual representa que todas as notas que quero devem distanciar da média aritimética entre elas em um valor máximo $D_máx$ (sendo uma constante do algoritmo). A partir dessa expressão, deduz-se que, para $n_x$ ser um valor ser mínimo, assume-se que todas as outras notas são iguais, e que a média aritimética entre todas estas notas deve-se representar $n_x + D_{máx}$, sendo que a soma entre eles (e não a subtração, possíveis por conta do módulo) representa o limite máximo que o valor mínimo pode possuir. Com este raciocínio, tem-se a seguinte expressão:  

$$
\dfrac{n_x + \sum_{i=0}^{len_{quero}-1}n_{quero_i}}{len_{quero}} = média = n_x + D_{máx} \:(III)
$$


Como se quer  minimizar $n_x$, deve-se saber os valores máximos de $n_{quero_i}$ , sendo todos iguais. Logo:

$$
n_x + (len_{quero}-1)n_{quero} = len_{quero}\cdot n_x + len_{quero}\cdot D_{máx}
$$

$$
(len_{quero}-1)n_{quero} = (len_{quero}-1)\cdot n_x + len_{quero}\cdot D_{máx}
$$

$$
\therefore n_{quero} = n_x + \dfrac{len_{quero}\cdot D_{máx}}{len_{quero}-1} \:(IV)
$$

Ao analisar $abs()$ em $(I)$, verifica-se que, para $n_x$ assumir valor mínimo:

$$
\sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i}+\sum_{i=0}^{len_{quero}-1}n_{quero_i}\cdot p_{quero_i}+n_{min}\cdot p_x = média - E_{rr} \:(V)
$$

Assumindo esta condição para que $n_x$ assuma valor mínimo, deve-se substituir $(IV)$ em $(V)$:

$$
\sum_{i=0}^{len_{quero}-1}\left(n_{min} + \dfrac{len_{quero}\cdot D_{máx}}{len_{quero}-1}\right)\cdot p_{quero_i}+n_{min}\cdot p_x = média - E_{rr} - \sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i}
$$

$$
\left(n_{min} + \dfrac{len_{quero}\cdot D_{máx}}{len_{quero}-1}\right)\sum_{i=0}^{len_{quero}-1} p_{quero_i}+n_{min}\cdot p_x = média - E_{rr} - \sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i} \:(VI)
$$

Para facilitar as contas, será englobado as seguintes constantes:

$$
A = média  - \sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i} \:(VII)
$$

$$
B = \dfrac{len_{quero}\cdot D_{máx}}{len_{quero}-1} \:(VIII)
$$

$$
C = \sum_{i=0}^{len_{quero}-1}p_{quero_i} \:(IX)
$$

Logo:

$$
\left(n_{min} + B\right)C+n_{min}\cdot p_x = A - E_{rr}
$$

Isolando $n_{min}$:

$$
n_{min} = \dfrac{A-E_{rr}-B\cdot C}{C+p_x}
$$

Como o resultado buscado é um valor no domínio de notas, que é discreto:

$$
n_{min} = \dfrac{ceil\left(2\cdot \left[\dfrac{A-E_{rr}-B\cdot C}{C+p_x}\right]\right)}{2} \:(X)
$$

Agora, deve-se analisar o valor máximo, que compreende uma distância fixa para a média aritimética entre as notas que o aluno quer buscar. Analisando a equação $(II)$, verifica-se a seguinte expressão que determina um valor máximo para $n_x$:


$$
\dfrac{n_x + \sum_{i=0}^{len_{quero}-1}n_{quero_i}}{len_{quero}} = média = n_x - D_{máx} \:(XI),
$$

onde a subtração é escolhida para representar o menor valor de $n_x$ para que ele represente o valor mínimo, tendo uma distância máxima de $D_{máx}$. Como se quer maximizar $n_x$, deve-se saber os valores mínimos de $n_{quero_i}$, sendo todos iguais. Logo:

$$
n_x + (len_{quero}-1)n_{quero} = len_{quero}\cdot n_x - len_{quero}\cdot D_{máx}
$$

$$
(len_{quero}-1)n_{quero} = (len_{quero}-1)\cdot n_x - len_{quero}\cdot D_{máx}
$$

$$
\therefore n_{quero} = n_x - \dfrac{len_{quero}\cdot D_{máx}}{len_{quero}-1} \:(XII)
$$

Ao analisar $abs()$ em $(I)$, verifica-se que, para $n_x$ assumir valor máximo:

$$
\sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i}+\sum_{i=0}^{len_{quero}-1}n_{quero_i}\cdot p_{quero_i}+n_{max}\cdot p_x = média + E_{rr} \:(XIII)
$$

Substituindo $(XII)$ em $(XIII)$:

$$
\sum_{i=0}^{len_{quero}-1}\left(n_{max} - \dfrac{len_{quero}\cdot D_{máx}}{len_{quero}-1}\right)\cdot p_{quero_i}+n_{max}\cdot p_x = média + E_{rr} - \sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i}
$$

$$
\left(n_{max} - \dfrac{len_{quero}\cdot D_{máx}}{len_{quero}-1}\right)\sum_{i=0}^{len_{quero}-1} p_{quero_i}+n_{max}\cdot p_x = média + E_{rr} - \sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i}
$$

Para facilitar as contas, serão englobadas as mesmas constantes. Portanto:

$$
\left(n_{max} - B\right)C+n_{max}\cdot p_x = A + E_{rr}
$$

Isolando $n_{max}$:

$$
n_{max} \cdot C - B\cdot C + n_{max}\cdot p_x = A + E_{rr}
$$

$$
n_{max} \cdot (C + p_x) = A + E_{rr} + B\cdot C
$$

$$
\therefore n_{max} = \dfrac{A + E_{rr} + B\cdot C}{C + p_x}
$$

Como deve-se descobrir o valor máximo de $n_x$ no domínio de notas, que é discreto:

$$
n_{max} = \dfrac{floor\left(2\cdot \left[\dfrac{A+E_{rr}+B\cdot C}{C + p_x}\right]\right)}{2} \:(XIV)
$$

Portanto, as duas equações que serão montadas na classe Utils serão $(X)$ e $(XIV)$:

$$
n_{min} = \dfrac{ceil\left(2\cdot \left[\dfrac{A-E_{rr}-B\cdot C}{C+p_x}\right]\right)}{2}
$$

$$
n_{max} = \dfrac{floor\left(2\cdot \left[\dfrac{A+E_{rr}+B\cdot C}{C + p_x}\right]\right)}{2}
$$

Com as constantes, a partir das equações $(VII)$, $(VIII)$ e $(IX)$, sendo representadas pelos seguintes valores:

$$
\begin{cases}
A = média  - \sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i} \\
B = \dfrac{len_{quero}\cdot D_{máx}}{len_{quero}-1} \\
C = \sum_{i=0}^{len_{quero}-1}p_{quero_i}
\end{cases}
$$

Um problema ocorre caso queira calcular uma nota apenas, no qual `len(notas_que_quero) = 0`. Portanto, será calculada uma fórmula minimizada para o cálculo de apenas uma nota. Ela será representada pelo valor mínimo que esta nota pode assumir dentro do domínio de notas. Portanto, para uma nota $n_min$ apenas:

$$
\sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i}+n_{min}\cdot p_x = média - E_{rr}
$$

$$
\therefore n_{min} = \dfrac{média - E_{rr} - \sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i}}{p_x} \:(XV)
$$

Comparando com as equações $(X)$ e $(XIV)$, as constantes de simplificação, para a expressão $(XV)$, são representadas por:

$$
\begin{cases}
A = média  - \sum_{i=0}^{len_{tenho}}n_{tenho_i}\cdot p_{tenho_i} \\
B = t, \: t\in \mathbf{R} \\
C = 0
\end{cases}
$$

Assumindo domínio discreto:

$$
n_{min} = \dfrac{ceil\left(2\cdot \left[\dfrac{A-E_{rr}}{p_x}\right]\right)}{2}
$$

Demonstrado todas as fórmulas necessárias para o cálculo dos limites dos domínios que uma certa nota pode possuir, é possível prosseguir com a explicação do algoritmo. O laço de repetição verifica o mínimo e máximo valor que cada nota pode possuir a fim de se obter uma combinação válida de notas. Chamando a função `minimo_valor_no_dominio` e `maximo_valor_no_dominio`, se calculam tais valores para cada nota. Caso o cálculo do valor mínimo retorne `-1`, indica-se que o valor mínimo para a nota procurada naquela iteração foi maior que o valor máximo do domínio de notas (10.0), ou seja, é impossível se obter aquela nota a fim de se obter a média desejada (pois ela nunca alcançará o valor mínimo). Este laço de repetição também possui a análise para uma nota apenas. Neste caso, ao verificar que se quer apenas uma nota, o algoritmo pega o valor mínimo e o retorna como resposta dentro do objeto `Boletim` inicializado anteriormente. Caso mais de uma nota seja buscada, o algoritmo se utiliza da função `limita_dominio` para restringir o domínio de cada nota procurada.

### [73-74]
Para cada nota procurada, após limitar o domínio de cada nota, estes são randomizados a fim de não se analisar os domínios em forma crescente.

### [78]
Cria-se a lista `idx_possiveis_notas`, que representam qual o index do domínio de notas de cada nota que quero que será analisado por vez. Ficará mais claro como que esta lista de indexes será utilizada posteriormente. Esta linha preenche esta lista com '0', representando que cada nota começará com o valor do index '0' de seu domínio, previamente randomizado.

### [82-83]
Passa pela lista de notas que quero e atribui a cada atributo `valor` de cada nota o primeiro valor do domínio previamente limitado e randomizado, utilizando a lista `idx_possiveis_notas`.

### [86]
Cria-se uma variável que representa se todas as notas foram verificadas, ou seja, se todas as combinações, para aquelas limitações de domínio, foram verificadas. Inicialmente, esta variável é `False`, pois ainda não se verificou todas as combinações.

### [89]
Inicia-se o segundo laço de repetição, que faz a verificação, para um certo `aumento_range`, se existem, pelo menos, uma combinação válida de notas.

### [92-94]
Este condicional verifica se todas as notas foram verificadas. Esta verificação ocorre se todos os valores de notas são os últimos valores do domínio de notas de cada nota, fazendo com que a lista `idx_possiveis_notas` represente, para cada nota, o último index do domínio de notas delas.

### [97]
Calcula-se a média final a partir do método da classe `Boletim`.

### [100-104]
Verifica se a combinação em análise, no segundo laço de repetição, é valida. Inicialmente, veririca-se se a média varia de 0.04 negativamente em relação à média desejada, e `0.04 + aumento_range` positivamente em relação à média desejada. Caso seja verdadeiro, verifica-se se a distância entre as notas varia de um valor `Solucionador.MENOR_DIST` da média aritimética entre as notas procuradas. Vale ressaltar que ambos os condicionais são utilizados no raciocínio do desenvolvimento do cálculo do valor mínimo e máximo de cada nota (explicados anteriormente), sendo o primeiro condicional exemplificado pela equação $(I)$ (com algumas alterações explicadas anteriormente) e o segundo por $(II)$. Caso seja verificado que tal combinação é válida, a combinação é adicionada como `tupla` na lista `notas_possiveis`.

### [108-132]
O condicional inicial verifica se o tamanho máximo de `notas_possíveis` (delimitado pelo parâmetro `Solucionador.NOTAS_TOTAIS` do algoritmo) foi atingido. Tal parâmetro foi criado a fim de se acelerar o processamento do algoritmo. Caso este valor seja atingido, verifica-se a melhor combinação dentre as `notas_possiveis`. Inicialmente, escolhe-se a primeira combinação como a melhor e, em seguida, compara esta combinação com as demais. Caso verifique-se que outra combinação seja melhor, esta nova combinação substitui a anterior, até se percorrer a lista inteira. Para verificar se uma combinação é melhor que a outra, verifica-se a combinação de menor desvio padrão entre as notas procuradas. Caso o desvio padrão seja igual (existem testes nos quais acontece isso), verifica-se, dentre o intervalo delimitado por `aumento_range`, qual combinação possui a menor média final, utilizando o método `media_final_externo` de `Boletim`. No final deste condicional, retorna-se o boletim com a melhor combinação.

### [140-156]
Caso este laço de repetição chegue ao fim (sem atingir o limite de notas), a lista `idx_possiveis_notas` é alterada. O objetivo deste trecho é somar em '1' o último index de nota e, caso ultrapasse o maior index do domínio daquela nota, soma-se '1' no index anterior, e zera o último index. Caso o penultimo index ultrapasse o maior index do domínio daquela nota, soma-se '1' no index anterior e zera o penúltimo index, e assim por diante. A fim de se explicar o objetivo deste trecho de código, alguns exemplos serão expostos:

_ex1:_ `[0, 0, 0, ..., 0, 0] --(+1)--> [0, 0, 0, ..., 0, 1]`

_ex2:_ `[0, 0, 0, ..., 0, 19] --(+1)--> [0, 0, 0, ..., 0, 20] -> [0, 0, 0, ..., 1, 0]`

_ex3:_ `[0, 0, 0, ..., 0, 19, 19] --(+1)--> [0, 0, 0, ..., 0, 19, 20] -> [0, 0, 0, ..., 0, 20, 0] -> [0, 0, 0, ..., 1, 0, 0]`

### [161-182]
Caso o primeiro laço de repetição chegue ao fim, deve-se verificar se, dentro daquele `aumento_range`, foi encontrada, pelo menos, uma nota possível. Caso seja encontrada, entra-se em um laço de repetição para verificar a melhor combinação de notas, utilizando as análises feitas nas linhas [108-132] explicadas anteriormente.

### [185-186]
Caso não tenha sido encontrada nenhuma nota, este condicional verificará se `media_desejada + Solucionador.ERR_MAX + Solucionador.aumento_range` é um múltiplo inteiro de `0.5`. Caso não seja, ele fará a primeira soma do `aumento_range`, a fim de que este condicional, na próxima verificação, não seja executado.

### [189-90]
Caso `aumento_range` já tenha sido somado uma vez, entra-se neste condicional a fim de que o valor máximo da média desejada seja múltipla de 0.5.

### [193]
Caso o algoritmo não encontre nenhuma nota possível, após as diversas verificações, retorna-se Nulo.

