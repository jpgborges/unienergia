# Análise do Consumo de Energia Elétrica — Métodos Numéricos

Trabalho da disciplina de **Métodos Numéricos** — **João Pedro e Vitor** — apresentação
em 25/08/26.

## Como rodar

```bash
python3 analise_consumo.py
```

```bash
python3 metodos_numericos.py
```

Não precisa instalar nada: não há dependência externa (nem numpy, nem matplotlib —
todos os métodos e gráficos são feitos do zero).

## Arquivos

| Arquivo | O que é |
|---|---|
| `analise_consumo.py` | Parte 0 — resposta direta ao enunciado (estatística descritiva) |
| `metodos_numericos.py` | Métodos numéricos da disciplina aplicados aos mesmos dados |
| `ROTEIRO_APRESENTACAO.md` | Roteiro com as falas divididas entre João e Vitor |
| `grafico_consumo.svg` | Gráfico de barras do consumo por dia |
| `grafico_convergencia.svg` | Convergência de Jacobi × Gauss-Seidel (escala log) |
| `grafico_interpolacao.svg` | Interpolação de grau 6, ajuste e raízes da bisseção |

## Conteúdo da disciplina aplicado (`metodos_numericos.py`)

### Parte 1 — Sistemas de equações lineares

Modelagem: com as horas de uso de cada grupo de equipamentos em três dias e o consumo
medido, monta-se um sistema 3×3 cuja solução é a **potência média de cada grupo**.

```
6x1 + 3x2 + 2x3 = 18     x1 = ar-condicionado
3x1 + 8x2 + 4x3 = 25     x2 = iluminação
2x1 + 3x2 + 7x3 = 22     x3 = tomadas/projetor
```

| Método | Tipo | Função | Resultado |
|---|---|---|---|
| Eliminação de Gauss com pivotamento parcial | direto | `eliminacao_gauss()` | resíduo 10⁻¹⁵ |
| Fatoração LU (Doolittle) | direto | `fatoracao_lu()` + `resolver_lu()` | idem Gauss |
| Jacobi | iterativo | `jacobi()` | 72 iterações |
| Gauss-Seidel | iterativo | `gauss_seidel()` | 13 iterações |

Convergência verificada antes pelo **critério das linhas** (`criterio_das_linhas()`):
alfa máximo 0,875 < 1 → convergência garantida.
Solução: **x = (1,559 · 1,517 · 2,047) kW**.

Aplicação: o **ajuste por mínimos quadrados** (`ajuste_minimos_quadrados()`) monta o
sistema normal e o resolve com o mesmo Gauss — reta com R² = 0,14 e parábola com
R² = 0,63.

### Parte 2 — Interpolação polinomial

| Método | Função | Observação |
|---|---|---|
| Newton (diferenças divididas) | `diferencas_divididas()`, `avaliar_newton()` | tabela completa até a ordem 6 |
| Lagrange (polinômios base) | `base_lagrange()`, `avaliar_lagrange()` | conta detalhada em t = 3,5 |

Os dois coincidem até 10⁻¹⁵ — o interpolador de grau 6 por 7 pontos é único.
O relatório mostra também o **fenômeno de Runge**: o polinômio de grau 6 oscila até
−0,26 kWh entre sábado e domingo, fora da faixa medida (10 a 30 kWh).

### Parte 3 — Zeros de funções

Pergunta: em que instante o consumo cruza a média de 19,57 kWh, ou seja,
**f(t) = P(t) − média = 0**.

| Etapa | Função | Resultado |
|---|---|---|
| Isolamento (teorema de Bolzano) | `isolar_raizes()` | 2 raízes em [1,25 · 1,30] e [5,70 · 5,75] |
| Bisseção | `bissecao()` | t = 1,2634 e t = 5,7170, 16 iterações cada |
| Nº teórico de iterações | `iteracoes_teoricas_bissecao()` | log₂(0,05/10⁻⁶) = 16, confere |
| Newton-Raphson (comparação) | `newton_raphson()` | mesma raiz em 3 iterações |

## Parte 0 — os 9 itens do enunciado (`analise_consumo.py`)

1. Vetor/lista — `DIAS` e `CONSUMOS`
2. Total da semana — **137 kWh**
3. Média diária — **19,57 kWh/dia**
4. Maior consumo — **Sexta, 30 kWh**
5. Menor consumo — **Domingo, 10 kWh**
6. Acima da média — **Terça, Quarta, Quinta, Sexta**
7. Redução no domingo vs. maior consumo — **66,67%**
8. Resultados organizados — `exibir_relatorio()`
9. Gráfico de barras — `grafico_matplotlib()`, `grafico_svg()`, `grafico_ascii()`

## Observações

- **Sobre os dados**: os consumos diários (18, 22, 20, 25, 30, 12, 10 kWh) são os do
  enunciado. As **horas de uso por equipamento** usadas na Parte 1 são uma extensão feita
  por nós, para que o sistema linear tivesse significado físico.
- **Sobre os gráficos**: são gerados em SVG puro pelo próprio código e abrem no
  navegador. O gráfico de barras tem ainda uma versão em matplotlib (caso a biblioteca
  esteja instalada — `sudo apt install python3-matplotlib`) e uma em ASCII, desenhada no
  terminal.
- **Trocar os dados**: basta editar `DIAS` e `CONSUMOS` em `analise_consumo.py`; os dois
  programas se ajustam sozinhos.
