# Roteiro da Apresentação — Análise do Consumo de Energia

**Disciplina:** Métodos Numéricos · **Dupla:** João Pedro e Vitor · **Data:** 25/08/26
**Duração alvo:** 12 a 15 min

## Preparação (antes de começar)

Dois terminais abertos na pasta do projeto, com os comandos já digitados:

```bash
python3 analise_consumo.py
```

```bash
python3 metodos_numericos.py
```

E três abas do navegador abertas, prontas para projetar:
`grafico_consumo.svg`, `grafico_convergencia.svg` e `grafico_interpolacao.svg`.

---

## Divisão das falas

| # | Quem | Assunto |
|---|---|---|
| 1 | **João** | Abertura e situação-problema |
| 2 | **Vitor** | Parte 0: resposta ao enunciado + gráfico de barras |
| 3 | **João** | Transição: o que os métodos numéricos acrescentam |
| 4 | **João** | Modelagem do sistema linear 3×3 |
| 5 | **João** | Método direto 1: Eliminação de Gauss com pivotamento |
| 6 | **Vitor** | Método direto 2: Fatoração LU |
| 7 | **Vitor** | Critério das linhas + método de Jacobi |
| 8 | **Vitor** | Gauss-Seidel e o gráfico de convergência |
| 9 | **João** | Aplicação: mínimos quadrados (sistema normal) |
| 10 | **João** | Interpolação de Newton (diferenças divididas) |
| 11 | **Vitor** | Interpolação de Lagrange + Runge |
| 12 | **João** | Zeros de funções: isolamento por Bolzano |
| 13 | **Vitor** | Método da bisseção |
| 14 | **João** | Nº teórico de iterações e comparação com Newton-Raphson |
| 15 | **os dois** | Conclusão |

---

## 1 — Abertura *(JOÃO)*

> "Bom dia, professor. Eu sou o João e este é o Vitor. Nosso trabalho parte da
> situação-problema da sala de aula: a escola mediu o consumo de energia elétrica
> durante 7 dias — 18, 22, 20, 25, 30, 12 e 10 kWh, de segunda a domingo — e quer
> analisar esses números.
>
> Nós dividimos em duas partes. A primeira responde direto ao enunciado, com
> estatística descritiva. A segunda, que é o foco desta disciplina, aplica os métodos
> numéricos sobre esses mesmos dados: sistemas de equações lineares por métodos diretos
> e iterativos, interpolação polinomial de Newton e de Lagrange, e zeros de funções pelo
> método da bisseção. Tudo implementado do zero, sem biblioteca pronta.
>
> O Vitor começa mostrando a primeira parte, que é a mais rápida."

---

## 2 — Resposta ao enunciado *(VITOR)*

**Rode `python3 analise_consumo.py` e projete o `grafico_consumo.svg`.**

> "Este primeiro programa guarda os consumos em uma lista e calcula: total de
> **137 kWh** na semana, média de **19,57 kWh por dia**, maior consumo na **sexta com
> 30 kWh**, menor no **domingo com 10 kWh**. Quatro dias ficaram acima da média — terça,
> quarta, quinta e sexta — e o domingo consumiu **66,67% menos** que a sexta.
>
> No gráfico, as barras laranja são os dias acima da média, as azuis abaixo, e a linha
> verde tracejada é a média. Dá para ver a semana inteira: sobe nos dias letivos, cai no
> fim de semana. Essa parte responde ao enunciado, mas ainda é só descrição dos dados."

---

## 3 — Transição *(JOÃO)*

> "É aqui que entram os métodos numéricos. A estatística diz *o que* aconteceu; os
> métodos numéricos permitem **resolver problemas que não têm solução direta** a partir
> desses dados. Nós fizemos três perguntas que o enunciado não responde:
>
> 1. Quanto cada equipamento da sala consome, individualmente? → **sistema linear**
> 2. Qual era o consumo em um instante que não foi medido? → **interpolação polinomial**
> 3. Em que momento exato o consumo cruzou a média? → **zeros de função**
>
> Vou rodar o segundo programa."

**Rode `python3 metodos_numericos.py`.**

---

## 4 — Modelagem do sistema linear *(JOÃO)*

> "A escola também anotou quantas horas cada grupo de equipamentos ficou ligado em três
> dias: na segunda, 6 horas de ar-condicionado, 3 de iluminação e 2 de tomadas e
> projetor; na quinta e na terça, outras combinações.
>
> Chamando de x1, x2 e x3 a **potência média de cada grupo, em kW**, cada dia vira uma
> equação, porque horas × potência = energia consumida:
>
> ```
> 6x1 + 3x2 + 2x3 = 18
> 3x1 + 8x2 + 4x3 = 25
> 2x1 + 3x2 + 7x3 = 22
> ```
>
> É um sistema 3×3, A·x = b. Resolvemos ele de **quatro maneiras**: dois métodos diretos
> e dois iterativos, e no final comparamos."

---

## 5 — Método direto: Eliminação de Gauss *(JOÃO)*

**Mostre a matriz aumentada e as etapas na tela.**

> "O primeiro é a **Eliminação de Gauss com pivotamento parcial**. Ele é um método
> direto: chega à solução exata em um número finito de operações.
>
> São duas fases. Na **eliminação**, usamos operações entre linhas para zerar tudo
> abaixo da diagonal e chegar a uma matriz triangular superior — na tela dá para
> acompanhar a matriz depois de eliminar a coluna 1 e depois a coluna 2. Na
> **substituição retroativa**, resolvemos de baixo para cima: a última linha tem uma
> incógnita só, e vamos subindo.
>
> O **pivotamento parcial** é a parte importante: antes de eliminar cada coluna, o
> programa procura o maior elemento em módulo e traz aquela linha para cima. Isso evita
> divisão por pivô nulo e reduz a propagação do erro de arredondamento. Neste sistema a
> diagonal já era a maior, então foram **zero trocas** — mas o mecanismo está lá.
>
> Resultado: ar-condicionado **1,559 kW**, iluminação **1,517 kW**, tomadas e projetor
> **2,047 kW**. E a verificação: o resíduo máximo de A·x − b deu 10⁻¹⁵, ou seja, zero a
> menos do erro de arredondamento da máquina."

---

## 6 — Método direto: Fatoração LU *(VITOR)*

> "O segundo método direto é a **fatoração LU**, pelo algoritmo de Doolittle. Ele
> decompõe a matriz A no produto de duas triangulares: L, inferior com diagonal de 1, e
> U, superior — que é justamente a matriz que o Gauss produziu na eliminação.
>
> Com A = L·U, resolver A·x = b vira dois sistemas triviais: primeiro **L·y = b** por
> substituição progressiva, de cima para baixo, e depois **U·x = y** por substituição
> retroativa. A solução bate com a de Gauss até a 15ª casa decimal.
>
> A vantagem do LU aparece quando muda só o lado direito: se a escola quiser recalcular
> para os consumos de outra semana, mantendo as mesmas horas de uso, a fatoração é feita
> **uma vez só** e cada novo b custa apenas as duas substituições — não é preciso repetir
> toda a eliminação."

---

## 7 — Método iterativo: Jacobi *(VITOR)*

> "Agora os **métodos iterativos**. Em vez de operar na matriz, eles partem de um chute
> inicial e vão refinando a solução até a precisão que a gente pedir.
>
> Antes de aplicar, verificamos a convergência pelo **critério das linhas**: em cada
> linha, a soma dos elementos fora da diagonal dividida pelo elemento da diagonal precisa
> dar menor que 1. Deu 0,83, 0,88 e 0,71 — o **alfa máximo é 0,875**, menor que 1, então
> a matriz é estritamente diagonal dominante e a convergência está **garantida para
> qualquer chute inicial**. E isso não é sorte: a diagonal domina porque cada um dos três
> dias tem um equipamento que predomina.
>
> No **método de Jacobi**, isolamos cada incógnita na sua equação e calculamos todas
> usando **só os valores da iteração anterior**. Começando de (0, 0, 0), o erro cai a
> cada passo, mas devagar: foram **72 iterações** para atingir a tolerância de 10⁻⁶."

---

## 8 — Gauss-Seidel e convergência *(VITOR)*

**Projete o `grafico_convergencia.svg`.**

> "O **Gauss-Seidel** muda uma coisa só: assim que calcula x1, já usa esse valor novo no
> cálculo do x2 da mesma iteração, em vez de esperar a próxima. Só com isso, o mesmo
> sistema converge em **13 iterações** em vez de 72 — mais de cinco vezes mais rápido.
>
> Este gráfico mostra o erro de cada iteração em escala logarítmica. As duas curvas são
> retas descendentes, o que é a assinatura da convergência linear dos dois métodos; a
> diferença está na **inclinação**. A linha verde é a tolerância: o Gauss-Seidel a cruza
> na iteração 13, o Jacobi só na 72.
>
> Na tabela comparativa, os quatro métodos chegam à mesma solução. A diferença é de
> natureza: os **diretos** dão a resposta exata num número fixo de operações; os
> **iterativos** chegam tão perto quanto se queira e são os indicados para sistemas
> grandes e esparsos, onde a eliminação sairia cara demais em memória e em tempo."

---

## 9 — Aplicação: mínimos quadrados *(JOÃO)*

> "Ainda em sistemas lineares, uma aplicação: o **ajuste de curvas por mínimos
> quadrados** também cai num sistema linear, o chamado sistema normal — e nós o
> resolvemos com o mesmo código da eliminação de Gauss.
>
> Ajustamos uma reta e uma parábola aos 7 pontos. A reta explica só **14%** da variação
> dos dados; a parábola, **63%**. Isso confirma numericamente o que o gráfico já sugeria:
> o consumo não tem comportamento linear ao longo da semana."

---

## 10 — Interpolação de Newton *(JOÃO)*

> "Segunda parte: **interpolação polinomial**. Aqui a pergunta é outra — queremos o
> polinômio que passa **exatamente** pelos 7 pontos medidos, para estimar o consumo em
> instantes que não foram medidos.
>
> Pelo método de **Newton**, montamos a **tabela de diferenças divididas**. A ordem 1 é a
> diferença entre valores vizinhos dividida pela diferença dos t; a ordem 2 usa as de
> ordem 1, e assim por diante, até a ordem 6. Os coeficientes do polinômio são o
> **primeiro valor de cada ordem**: 18, 4, −3, 2,1667, −0,8333, 0,0333 e 0,1028.
>
> O polinômio fica na forma
> `P(t) = 18 + 4(t−1) − 3(t−1)(t−2) + …`, que o programa avalia na forma aninhada, mais
> eficiente e mais estável numericamente.
>
> Verificação: o maior desvio entre P(tᵢ) e os valores medidos é 10⁻¹⁴ — ele realmente
> passa pelos 7 pontos."

---

## 11 — Lagrange e o fenômeno de Runge *(VITOR)*

**Projete o `grafico_interpolacao.svg`.**

> "Pelo método de **Lagrange** chegamos ao mesmo polinômio por um caminho diferente:
> P(t) é a soma de cada yᵢ multiplicado pelo seu polinômio base Lᵢ(t), construído para
> valer **1 no próprio ponto e 0 em todos os outros**. Na tela está a conta completa em
> t = 3,5: cada base, cada produto e a soma, que dá 21,28 kWh.
>
> Comparando os dois métodos em cinco instantes, a diferença é da ordem de 10⁻¹⁵ — puro
> erro de arredondamento. É o esperado: **o polinômio interpolador de grau 6 por 7 pontos
> é único**; Newton e Lagrange apenas o escrevem de formas diferentes. Newton é melhor
> quando novos pontos vão sendo acrescentados, porque basta calcular um coeficiente novo;
> em Lagrange é preciso refazer todas as bases.
>
> E aqui está o cuidado mais importante desta parte — a curva laranja no gráfico. Os
> dados vão de 10 a 30 kWh, mas o polinômio de grau 6 **despenca até −0,26 kWh** entre
> sábado e domingo. É o **fenômeno de Runge**: grau alto passa por todos os pontos, mas
> oscila entre eles. Por isso, para estimar valores intermediários, a interpolação linear
> ou o ajuste de grau baixo — a curva roxa — são mais confiáveis do que o interpolador
> exato."

---

## 12 — Zeros de funções: isolamento *(JOÃO)*

> "Terceira parte: **zeros de funções**. A pergunta é: em que momento exato o consumo
> cruzou a média de 19,57 kWh? Isso é resolver **f(t) = P(t) − média = 0**, com o P(t) da
> interpolação. É uma equação de grau 6 — não dá para resolver na mão.
>
> O primeiro passo é o **isolamento**, pelo **teorema de Bolzano**: se f é contínua e
> f(a)·f(b) < 0, existe pelo menos uma raiz entre a e b. O programa varre o intervalo
> [1, 7] de 0,05 em 0,05 procurando trocas de sinal, e encontrou **duas**: uma em
> [1,25 · 1,30] e outra em [5,70 · 5,75]."

---

## 13 — Método da bisseção *(VITOR)*

> "Com as raízes isoladas, vem o refinamento pelo **método da bisseção**. O algoritmo é
> simples: calcula o ponto médio do intervalo, verifica em qual das duas metades a troca
> de sinal continua, descarta a outra metade e repete.
>
> Na tabela da segunda raiz dá para acompanhar: o intervalo começa em [5,70 · 5,75] e a
> coluna do erro mostra o comportamento característico — **2,5 × 10⁻², 1,25 × 10⁻²,
> 6,25 × 10⁻³** — o erro cai **exatamente pela metade** a cada iteração. O critério de
> parada é (b − a)/2 menor que a tolerância de 10⁻⁶, atingido na **iteração 16**.
>
> As raízes são **t = 1,2634** e **t = 5,7170**. Traduzindo: o consumo cruza a média para
> cima na segunda por volta das 6h19, e cruza para baixo na sexta por volta das 17h12 —
> é ali que começa o período econômico da semana. No gráfico, são os dois círculos verdes
> sobre a linha da média."

---

## 14 — Iterações teóricas e Newton-Raphson *(JOÃO)*

> "Uma vantagem da bisseção é que dá para **prever o custo antes de rodar**. Como o erro
> cai pela metade a cada passo, o número de iterações é k > log₂((b − a)/tolerância).
> Aqui: log₂(0,05 / 10⁻⁶) = **16**. E o programa gastou exatamente 16. A teoria bate com
> a prática.
>
> Para efeito de comparação, resolvemos a mesma raiz por **Newton-Raphson**, que usa a
> reta tangente: ele chegou ao mesmo valor em **3 iterações** em vez de 16, porque a
> convergência é quadrática. Em compensação, precisa da derivada e de um bom chute
> inicial, e pode divergir. A bisseção é mais lenta, mas só exige a troca de sinal e
> **nunca falha**. É a mesma troca entre garantia e velocidade que aparece nos métodos
> iterativos de sistemas lineares."

---

## 15 — Conclusão

***VITOR:***

> "Fechando os resultados: o sistema linear mostrou que a linha de tomadas e projetor é a
> de maior potência média, 2,05 kW — é onde a escola deve olhar primeiro. A interpolação
> permitiu estimar o consumo entre as medições, com a ressalva do fenômeno de Runge. E a
> bisseção localizou o momento exato em que o consumo cruza a média."

***JOÃO:***

> "E, do lado dos métodos, o trabalho aplicou: sistemas lineares por dois métodos diretos
> — Gauss com pivotamento e fatoração LU — e dois iterativos — Jacobi e Gauss-Seidel, com
> o critério das linhas garantindo a convergência; interpolação de Newton e de Lagrange,
> verificando que dão o mesmo polinômio; e zeros de função por isolamento de Bolzano e
> bisseção, com o número de iterações confirmando a previsão teórica.
>
> Cada método foi implementado do zero, e todos foram verificados: resíduo do sistema,
> o interpolador passando pelos pontos e as raízes conferidas por um segundo método.
> Era isso, professor. À disposição para as perguntas."

---

## Perguntas prováveis do professor

**"Por que Jacobi precisou de 72 iterações e Gauss-Seidel de 13?"** — *Vitor*
Porque o Jacobi só usa valores da iteração anterior, enquanto o Gauss-Seidel já aproveita
os valores atualizados dentro da mesma iteração. Com alfa de 0,875, a convergência do
Jacobi é lenta: o erro cai por um fator próximo de 0,875 a cada passo.

**"E se a matriz não fosse diagonal dominante?"** — *Vitor*
O critério das linhas é **suficiente, não necessário**: a falha não garante divergência,
mas tira a garantia de convergência. Poderíamos tentar reordenar as linhas para tornar a
diagonal dominante — e, se não desse, usar um método direto.

**"Por que o pivotamento parcial, se não houve nenhuma troca?"** — *João*
Porque a necessidade depende dos dados. Se a matriz tivesse um zero ou um valor muito
pequeno na diagonal, sem pivotamento haveria divisão por zero ou uma amplificação enorme
do erro de arredondamento. O código está preparado para qualquer entrada.

**"Qual a diferença prática entre Gauss e LU, se os dois são diretos?"** — *Vitor*
O custo por novo lado direito. Gauss refaz toda a eliminação a cada b novo; o LU fatora
uma vez e cada b custa só duas substituições.

**"Newton e Lagrange dão sempre o mesmo resultado?"** — *João*
Sim, matematicamente é o mesmo polinômio — o interpolador de grau n por n+1 pontos é
único. O que muda é o custo e a facilidade de acrescentar pontos, onde Newton leva
vantagem.

**"Por que não usar o polinômio de grau 6 para estimar consumo?"** — *João*
Pelo fenômeno de Runge, que o gráfico mostra: entre sábado e domingo ele cai para
−0,26 kWh, um valor sem sentido físico. Interpolar não é o mesmo que modelar; para
estimar, o ajuste de grau baixo é mais seguro.

**"Quantas iterações a bisseção precisaria para uma tolerância de 10⁻¹⁰?"** — *Vitor*
log₂(0,05 / 10⁻¹⁰) ≈ 29 iterações. Como o erro cai pela metade a cada passo, cada casa
decimal a mais custa cerca de 3,3 iterações.

**"Por que a bisseção, sendo mais lenta, ainda é usada?"** — *João*
Porque é a única que dá garantia: havendo troca de sinal, ela sempre converge, sem
precisar de derivada. Na prática, costuma-se usá-la para chegar perto da raiz e depois
trocar por Newton, que refina rápido.

**"De onde vieram as horas de uso dos equipamentos?"** — *João*
Essa parte é uma extensão que nós fizemos da situação-problema, para ter um sistema
linear com significado físico. Os consumos diários — 18, 25 e 22 kWh — são os do
enunciado; as horas de uso foram estimadas por nós para completar a modelagem.
