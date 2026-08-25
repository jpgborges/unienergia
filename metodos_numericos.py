# -*- coding: utf-8 -*-
"""
=============================================================================
 METODOS NUMERICOS APLICADOS AO CONSUMO DE ENERGIA DA SALA DE AULA
=============================================================================
 Segunda parte do trabalho. A primeira (analise_consumo.py) resolve o
 enunciado com estatistica descritiva; aqui aplicamos os metodos numericos
 vistos na disciplina sobre a mesma situacao-problema.

 CONTEUDO DA DISCIPLINA APLICADO
   PARTE 1 - SISTEMAS DE EQUACOES LINEARES
       1.1  Modelagem: quanto cada grupo de equipamentos consome
       1.2  Metodo DIRETO: Eliminacao de Gauss com pivotamento parcial
       1.3  Metodo DIRETO: Fatoracao LU (Doolittle)
       1.4  Metodo ITERATIVO: Jacobi
       1.5  Metodo ITERATIVO: Gauss-Seidel
       1.6  Comparacao dos quatro metodos (residuo e n. de iteracoes)
       1.7  Aplicacao: ajuste de curva por minimos quadrados
            (o sistema normal tambem e resolvido por Gauss)

   PARTE 2 - INTERPOLACAO POLINOMIAL
       2.1  Interpolacao de NEWTON (tabela de diferencas divididas)
       2.2  Interpolacao de LAGRANGE (polinomios base)
       2.3  Estimativas em instantes nao medidos e fenomeno de Runge

   PARTE 3 - ZEROS DE FUNCOES
       3.1  Isolamento de raizes (teorema de Bolzano)
       3.2  Metodo da BISSECAO (com criterio de parada e tabela)
       3.3  Numero teorico de iteracoes da bissecao
       3.4  Comparacao com Newton-Raphson

 Tudo implementado do zero, sem bibliotecas externas.
 Apresentacao: Joao Pedro e Vitor
=============================================================================
"""

import os

from analise_consumo import DIAS, CONSUMOS, br, linha

# ---------------------------------------------------------------------------
# DADOS DA SITUACAO-PROBLEMA
# ---------------------------------------------------------------------------
# Variavel independente: o dia (t = 1 -> segunda ... t = 7 -> domingo).
# Convencao: t inteiro marca o INICIO do dia (t = 5,0 e a abertura da sexta).
T = [float(i + 1) for i in range(len(CONSUMOS))]
Y = [float(v) for v in CONSUMOS]

TOLERANCIA = 1e-6      # criterio de parada dos metodos iterativos
MAX_ITERACOES = 200


# =============================================================================
# PARTE 1 - SISTEMAS DE EQUACOES LINEARES
# =============================================================================

# -----------------------------------------------------------------------------
# 1.1 MODELAGEM
# -----------------------------------------------------------------------------
# Alem do consumo diario, a escola registrou quantas HORAS cada grupo de
# equipamentos ficou ligado em tres dias da semana:
#
#              ar-condicionado   iluminacao   tomadas/projetor   consumo medido
#   Segunda          6 h            3 h             2 h              18 kWh
#   Quinta           3 h            8 h             4 h              25 kWh
#   Terca            2 h            3 h             7 h              22 kWh
#
# Chamando de x1, x2 e x3 a POTENCIA MEDIA (em kW) de cada grupo, cada dia
# vira uma equacao (horas x potencia = energia), formando o sistema A.x = b:
#
#       6.x1 + 3.x2 + 2.x3 = 18
#       3.x1 + 8.x2 + 4.x3 = 25
#       2.x1 + 3.x2 + 7.x3 = 22
#
# Descobrindo x1, x2 e x3, a escola sabe qual equipamento pesa mais na conta.
MATRIZ_A = [[6.0, 3.0, 2.0],
            [3.0, 8.0, 4.0],
            [2.0, 3.0, 7.0]]
VETOR_B = [18.0, 25.0, 22.0]
INCOGNITAS = ["x1 (ar-condicionado)", "x2 (iluminacao)", "x3 (tomadas/projetor)"]
DIAS_SISTEMA = ["Segunda", "Quinta", "Terca"]


def mostrar_sistema(a, b, titulo=""):
    if titulo:
        print(f"  {titulo}")
    for i in range(len(b)):
        equacao = "  ".join(f"{a[i][j]:>7.3f}" for j in range(len(a[i])))
        print(f"      [ {equacao} | {b[i]:>8.3f} ]")


def residuo_maximo(a, b, x):
    """Verificacao da solucao: calcula max|A.x - b| (deve dar praticamente 0)."""
    maior = 0.0
    for i in range(len(b)):
        soma = sum(a[i][j] * x[j] for j in range(len(x)))
        maior = max(maior, abs(soma - b[i]))
    return maior


# -----------------------------------------------------------------------------
# 1.2 METODO DIRETO: ELIMINACAO DE GAUSS COM PIVOTAMENTO PARCIAL
# -----------------------------------------------------------------------------
def eliminacao_gauss(matriz_a, vetor_b, mostrar_etapas=False):
    """
    METODO DIRETO: chega a solucao exata em um numero finito de operacoes.

    Fase 1 - Eliminacao: usa operacoes elementares entre linhas para
             transformar A em uma matriz triangular superior.
    Fase 2 - Substituicao retroativa: resolve de baixo para cima.

    PIVOTAMENTO PARCIAL: antes de eliminar cada coluna, troca as linhas para
    que o pivo seja o maior valor em modulo da coluna. Isso evita pivo nulo e
    reduz a propagacao do erro de arredondamento.
    """
    n = len(vetor_b)
    a = [linha_atual[:] for linha_atual in matriz_a]   # copia (nao altera o original)
    b = vetor_b[:]
    trocas = 0

    # ---- Fase 1: eliminacao -------------------------------------------------
    for k in range(n - 1):
        # escolha do pivo (maior valor em modulo da coluna k)
        linha_pivo = k
        for i in range(k + 1, n):
            if abs(a[i][k]) > abs(a[linha_pivo][k]):
                linha_pivo = i
        if linha_pivo != k:
            a[k], a[linha_pivo] = a[linha_pivo], a[k]
            b[k], b[linha_pivo] = b[linha_pivo], b[k]
            trocas += 1
            if mostrar_etapas:
                print(f"      pivotamento: troca da linha {k + 1} com a linha {linha_pivo + 1}")

        if abs(a[k][k]) < 1e-14:
            raise ZeroDivisionError("Pivo nulo: o sistema nao tem solucao unica.")

        # zera os elementos abaixo do pivo
        for i in range(k + 1, n):
            multiplicador = a[i][k] / a[k][k]
            for j in range(k, n):
                a[i][j] -= multiplicador * a[k][j]
            b[i] -= multiplicador * b[k]

        if mostrar_etapas:
            mostrar_sistema(a, b, f"apos eliminar a coluna {k + 1}:")

    # ---- Fase 2: substituicao retroativa ------------------------------------
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = b[i]
        for j in range(i + 1, n):
            soma -= a[i][j] * x[j]
        x[i] = soma / a[i][i]

    return x, a, b, trocas


# -----------------------------------------------------------------------------
# 1.3 METODO DIRETO: FATORACAO LU (DOOLITTLE)
# -----------------------------------------------------------------------------
def fatoracao_lu(matriz_a):
    """
    Decompoe A = L.U, com L triangular inferior (diagonal 1) e U triangular
    superior. Vantagem sobre Gauss: fatora UMA vez e resolve para varios
    vetores b diferentes (ex.: recalcular para outro dia da semana), sem
    repetir a eliminacao.
    """
    n = len(matriz_a)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        # linha i de U
        for j in range(i, n):
            U[i][j] = matriz_a[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        # coluna i de L
        for j in range(i + 1, n):
            if abs(U[i][i]) < 1e-14:
                raise ZeroDivisionError("Pivo nulo: use pivotamento antes de fatorar.")
            L[j][i] = (matriz_a[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]
    return L, U


def resolver_lu(L, U, vetor_b):
    """
    Resolve A.x = b em dois passos, ambos triviais por serem triangulares:
        1) L.y = b  -> substituicao PROGRESSIVA (de cima para baixo)
        2) U.x = y  -> substituicao RETROATIVA  (de baixo para cima)
    """
    n = len(vetor_b)
    y = [0.0] * n
    for i in range(n):
        y[i] = vetor_b[i] - sum(L[i][j] * y[j] for j in range(i))
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x, y


# -----------------------------------------------------------------------------
# 1.4 e 1.5 METODOS ITERATIVOS: JACOBI E GAUSS-SEIDEL
# -----------------------------------------------------------------------------
def criterio_das_linhas(matriz_a):
    """
    Criterio das linhas (diagonal estritamente dominante): para cada linha,
    |a_ii| deve ser maior que a soma dos demais elementos da linha.
    Se vale, Jacobi e Gauss-Seidel CONVERGEM para qualquer chute inicial.
    Devolve (atende_ao_criterio, lista dos alfas de cada linha).
    """
    n = len(matriz_a)
    alfas = []
    for i in range(n):
        soma_outros = sum(abs(matriz_a[i][j]) for j in range(n) if j != i)
        alfas.append(soma_outros / abs(matriz_a[i][i]))
    return max(alfas) < 1, alfas


def jacobi(matriz_a, vetor_b, chute=None, tolerancia=TOLERANCIA,
           max_iteracoes=MAX_ITERACOES):
    """
    METODO ITERATIVO DE JACOBI:
        x_i^(k+1) = ( b_i - soma_(j != i) a_ij * x_j^(k) ) / a_ii

    Todas as incognitas sao atualizadas a partir da iteracao ANTERIOR
    (por isso precisa guardar o vetor antigo inteiro).
    """
    n = len(vetor_b)
    x = chute[:] if chute else [0.0] * n
    historico = []
    for iteracao in range(1, max_iteracoes + 1):
        novo = [0.0] * n
        for i in range(n):
            soma = sum(matriz_a[i][j] * x[j] for j in range(n) if j != i)
            novo[i] = (vetor_b[i] - soma) / matriz_a[i][i]
        erro = max(abs(novo[i] - x[i]) for i in range(n))
        historico.append((iteracao, novo[:], erro))
        x = novo
        if erro < tolerancia:
            break
    return x, len(historico), historico


def gauss_seidel(matriz_a, vetor_b, chute=None, tolerancia=TOLERANCIA,
                 max_iteracoes=MAX_ITERACOES):
    """
    METODO ITERATIVO DE GAUSS-SEIDEL:
        x_i^(k+1) = ( b_i - soma_(j < i) a_ij*x_j^(k+1)
                          - soma_(j > i) a_ij*x_j^(k) ) / a_ii

    Diferenca para Jacobi: ja usa os valores ATUALIZADOS na propria iteracao,
    o que normalmente o faz convergir com menos passos.
    """
    n = len(vetor_b)
    x = chute[:] if chute else [0.0] * n
    historico = []
    for iteracao in range(1, max_iteracoes + 1):
        anterior = x[:]
        for i in range(n):
            soma = sum(matriz_a[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (vetor_b[i] - soma) / matriz_a[i][i]   # atualizacao imediata
        erro = max(abs(x[i] - anterior[i]) for i in range(n))
        historico.append((iteracao, x[:], erro))
        if erro < tolerancia:
            break
    return x, len(historico), historico


# -----------------------------------------------------------------------------
# 1.7 APLICACAO: AJUSTE DE CURVA POR MINIMOS QUADRADOS
# -----------------------------------------------------------------------------
def ajuste_minimos_quadrados(t, y, grau):
    """
    Monta o SISTEMA NORMAL do metodo dos minimos quadrados e o resolve com o
    mesmo eliminacao_gauss da secao 1.2 - ou seja, e mais uma aplicacao de
    sistemas lineares. Devolve os coeficientes de a0 + a1*t + a2*t^2 + ...
    """
    n = grau + 1
    somas_t = [sum(ti ** k for ti in t) for k in range(2 * grau + 1)]
    somas_ty = [sum((ti ** k) * yi for ti, yi in zip(t, y)) for k in range(n)]
    matriz = [[somas_t[i + j] for j in range(n)] for i in range(n)]
    solucao, _, _, _ = eliminacao_gauss(matriz, somas_ty)
    return solucao, matriz, somas_ty


def avaliar_polinomio(coeficientes, x):
    """Avalia o polinomio pelo metodo de Horner (menos operacoes, menos erro)."""
    resultado = 0.0
    for coeficiente in reversed(coeficientes):
        resultado = resultado * x + coeficiente
    return resultado


def coeficiente_determinacao(t, y, coeficientes):
    """R2: fracao da variacao dos dados que o modelo explica (0 a 1)."""
    media = sum(y) / len(y)
    soma_total = sum((yi - media) ** 2 for yi in y)
    soma_residuos = sum((yi - avaliar_polinomio(coeficientes, ti)) ** 2
                        for ti, yi in zip(t, y))
    return 1 - soma_residuos / soma_total


def polinomio_em_texto(coeficientes):
    partes = []
    for grau, coeficiente in enumerate(coeficientes):
        if grau == 0:
            partes.append(br(coeficiente))
        else:
            sinal = "+" if coeficiente >= 0 else "-"
            potencia = "t" if grau == 1 else f"t^{grau}"
            partes.append(f"{sinal} {br(abs(coeficiente))}{potencia}")
    return " ".join(partes)


# =============================================================================
# PARTE 2 - INTERPOLACAO POLINOMIAL
# =============================================================================

# -----------------------------------------------------------------------------
# 2.1 INTERPOLACAO DE NEWTON (DIFERENCAS DIVIDIDAS)
# -----------------------------------------------------------------------------
def diferencas_divididas(t, y):
    """
    Monta a tabela de diferencas divididas:
        ordem 1: f[xi, xi+1]   = (f[xi+1] - f[xi]) / (xi+1 - xi)
        ordem k: f[xi,...,xi+k] = (dif. anterior a direita - a esquerda)
                                  / (xi+k - xi)
    Os coeficientes do polinomio de Newton sao os primeiros de cada ordem.
    """
    n = len(t)
    tabela = [y[:]]
    for ordem in range(1, n):
        anterior = tabela[ordem - 1]
        coluna = [(anterior[i + 1] - anterior[i]) / (t[i + ordem] - t[i])
                  for i in range(n - ordem)]
        tabela.append(coluna)
    coeficientes = [tabela[ordem][0] for ordem in range(n)]
    return coeficientes, tabela


def avaliar_newton(coeficientes, t, x):
    """
    P(x) = c0 + c1(x-t0) + c2(x-t0)(x-t1) + ... + cn(x-t0)...(x-t(n-1))
    Avaliado na forma aninhada, de tras para frente (mais eficiente e estavel).
    VANTAGEM de Newton: para acrescentar um novo ponto (um oitavo dia, por
    exemplo), basta calcular UM coeficiente novo - os outros continuam valendo.
    """
    resultado = coeficientes[-1]
    for i in range(len(coeficientes) - 2, -1, -1):
        resultado = resultado * (x - t[i]) + coeficientes[i]
    return resultado


# -----------------------------------------------------------------------------
# 2.2 INTERPOLACAO DE LAGRANGE
# -----------------------------------------------------------------------------
def base_lagrange(t, i, x):
    """
    Polinomio base L_i(x) = produto de (x - t_j)/(t_i - t_j) para j != i.
    Vale 1 em x = t_i e 0 em todos os outros nos.
    """
    base = 1.0
    for j in range(len(t)):
        if j != i:
            base *= (x - t[j]) / (t[i] - t[j])
    return base


def avaliar_lagrange(t, y, x):
    """
    P(x) = soma de y_i * L_i(x).
    Nao precisa montar tabela nenhuma, mas para acrescentar um ponto e
    preciso refazer TODAS as bases - ao contrario de Newton.
    """
    return sum(y[i] * base_lagrange(t, i, x) for i in range(len(t)))


def interpolacao_linear(t, y, x):
    """Interpolacao de grau 1 entre os dois pontos vizinhos de x."""
    for i in range(len(t) - 1):
        if t[i] <= x <= t[i + 1]:
            return y[i] + (x - t[i]) / (t[i + 1] - t[i]) * (y[i + 1] - y[i])
    return None


# =============================================================================
# PARTE 3 - ZEROS DE FUNCOES
# =============================================================================
def isolar_raizes(funcao, inicio, fim, passo=0.05):
    """
    ISOLAMENTO pelo teorema de Bolzano: se f e continua e f(a).f(b) < 0,
    entao existe pelo menos uma raiz no intervalo [a, b].
    """
    intervalos = []
    x = inicio
    while x < fim - 1e-12:
        proximo = min(x + passo, fim)
        if funcao(x) * funcao(proximo) < 0:
            intervalos.append((x, proximo))
        x = proximo
    return intervalos


def bissecao(funcao, a, b, tolerancia=TOLERANCIA, max_iteracoes=MAX_ITERACOES):
    """
    METODO DA BISSECAO
      1) parte de [a, b] com f(a).f(b) < 0
      2) calcula o ponto medio x = (a+b)/2
      3) fica com o subintervalo onde a troca de sinal continua
      4) repete ate (b-a)/2 < tolerancia

    Converge SEMPRE (se ha troca de sinal), porem devagar: o erro cai
    exatamente pela metade a cada iteracao.
    """
    if funcao(a) * funcao(b) >= 0:
        raise ValueError("Nao ha troca de sinal em [a, b]: bissecao nao se aplica.")

    historico = []
    for iteracao in range(1, max_iteracoes + 1):
        meio = (a + b) / 2
        f_meio = funcao(meio)
        erro = (b - a) / 2
        historico.append((iteracao, a, b, meio, f_meio, erro))
        if erro < tolerancia or f_meio == 0.0:
            return meio, iteracao, historico
        if funcao(a) * f_meio < 0:
            b = meio
        else:
            a = meio
    return (a + b) / 2, max_iteracoes, historico


def iteracoes_teoricas_bissecao(a, b, tolerancia=TOLERANCIA):
    """
    Numero MINIMO de iteracoes previsto pela teoria:
        k > log2( (b - a) / tolerancia )
    Uma das vantagens da bissecao: da para saber o custo antes de rodar.
    """
    import math
    return math.ceil(math.log2((b - a) / tolerancia))


def newton_raphson(funcao, derivada, x0, tolerancia=TOLERANCIA,
                   max_iteracoes=MAX_ITERACOES):
    """
    Newton-Raphson, usado aqui so para COMPARAR a velocidade com a bissecao:
        x(k+1) = x(k) - f(x(k)) / f'(x(k))
    Converge quadraticamente, mas exige a derivada e um bom chute inicial.
    """
    x = x0
    historico = []
    for iteracao in range(1, max_iteracoes + 1):
        fx, dfx = funcao(x), derivada(x)
        if abs(dfx) < 1e-14:
            raise ZeroDivisionError("Derivada nula: Newton-Raphson nao se aplica.")
        novo = x - fx / dfx
        erro = abs(novo - x)
        historico.append((iteracao, x, fx, dfx, novo, erro))
        x = novo
        if erro < tolerancia:
            return x, iteracao, historico
    return x, max_iteracoes, historico


def derivada_central(funcao, x, h=1e-6):
    """Derivada aproximada por diferenca central, usada no Newton-Raphson."""
    return (funcao(x + h) - funcao(x - h)) / (2 * h)


# =============================================================================
# ERROS
# =============================================================================
def erro_absoluto(exato, aproximado):
    return abs(exato - aproximado)


def erro_relativo_percentual(exato, aproximado):
    return float("inf") if exato == 0 else abs((exato - aproximado) / exato) * 100


# =============================================================================
# RELATORIO
# =============================================================================
def parte_1_sistemas_lineares():
    print()
    print(linha())
    print("  PARTE 1 - SISTEMAS DE EQUACOES LINEARES")
    print(linha())
    print()
    print("  1.1 MODELAGEM DO PROBLEMA")
    print()
    print("  A escola tambem anotou quantas HORAS cada grupo de equipamentos")
    print("  ficou ligado em tres dias da semana:")
    print()
    print(f"      {'dia':<9}{'ar-cond.':>10}{'iluminacao':>12}{'tomadas':>10}"
          f"{'consumo':>10}")
    for i, dia in enumerate(DIAS_SISTEMA):
        print(f"      {dia:<9}{MATRIZ_A[i][0]:>9.0f}h{MATRIZ_A[i][1]:>11.0f}h"
              f"{MATRIZ_A[i][2]:>9.0f}h{VETOR_B[i]:>8.0f} kWh")
    print()
    print("  Sendo x1, x2 e x3 a potencia media de cada grupo (em kW), cada dia")
    print("  vira uma equacao (horas x potencia = energia consumida):")
    print()
    print("      6.x1 + 3.x2 + 2.x3 = 18")
    print("      3.x1 + 8.x2 + 4.x3 = 25")
    print("      2.x1 + 3.x2 + 7.x3 = 22")
    print()
    print("  Resolver esse sistema responde: qual equipamento pesa mais na conta?")

    # ---- 1.2 Gauss ---------------------------------------------------------
    print()
    print(linha("-"))
    print("  1.2 METODO DIRETO - ELIMINACAO DE GAUSS COM PIVOTAMENTO PARCIAL")
    print(linha("-"))
    print()
    mostrar_sistema(MATRIZ_A, VETOR_B, "Matriz aumentada [A | b] inicial:")
    print()
    x_gauss, triangular, b_final, trocas = eliminacao_gauss(
        MATRIZ_A, VETOR_B, mostrar_etapas=True)
    print()
    print(f"  Trocas de linha realizadas pelo pivotamento: {trocas}")
    print("  Substituicao retroativa na matriz triangular:")
    print()
    for nome, valor in zip(INCOGNITAS, x_gauss):
        print(f"      {nome:<26} = {br(valor, 4)} kW")
    print()
    print(f"  Verificacao: max|A.x - b| = {residuo_maximo(MATRIZ_A, VETOR_B, x_gauss):.2e}")

    # ---- 1.3 LU ------------------------------------------------------------
    print()
    print(linha("-"))
    print("  1.3 METODO DIRETO - FATORACAO LU (DOOLITTLE)")
    print(linha("-"))
    L, U = fatoracao_lu(MATRIZ_A)
    print()
    print("      Matriz L (triangular inferior)      Matriz U (triangular superior)")
    for i in range(3):
        esquerda = "  ".join(f"{L[i][j]:>7.4f}" for j in range(3))
        direita = "  ".join(f"{U[i][j]:>7.4f}" for j in range(3))
        print(f"      [{esquerda} ]        [{direita} ]")
    x_lu, y_lu = resolver_lu(L, U, VETOR_B)
    print()
    print(f"      1o passo  L.y = b  ->  y = "
          f"[{', '.join(br(v, 4) for v in y_lu)}]   (substituicao progressiva)")
    print(f"      2o passo  U.x = y  ->  x = "
          f"[{', '.join(br(v, 4) for v in x_lu)}]   (substituicao retroativa)")
    print()
    print(f"      Diferenca para a solucao de Gauss: "
          f"{max(erro_absoluto(g, l) for g, l in zip(x_gauss, x_lu)):.2e}")
    print("      Vantagem do LU: fatora A uma unica vez e resolve para varios b")
    print("      diferentes (outros dias da semana) sem repetir a eliminacao.")

    # ---- 1.4 e 1.5 Jacobi e Gauss-Seidel -----------------------------------
    print()
    print(linha("-"))
    print("  1.4 e 1.5 METODOS ITERATIVOS - JACOBI E GAUSS-SEIDEL")
    print(linha("-"))

    converge, alfas = criterio_das_linhas(MATRIZ_A)
    print()
    print("  CRITERIO DAS LINHAS (diagonal estritamente dominante):")
    for i, alfa in enumerate(alfas):
        outros = " + ".join(f"|{MATRIZ_A[i][j]:.0f}|" for j in range(3) if j != i)
        print(f"      linha {i + 1}: ({outros}) / |{MATRIZ_A[i][i]:.0f}| = "
              f"{br(alfa, 4)}  {'< 1  OK' if alfa < 1 else '>= 1  FALHA'}")
    print(f"      alfa maximo = {br(max(alfas), 4)}  ->  "
          f"{'convergencia GARANTIDA' if converge else 'convergencia NAO garantida'}")
    print("      (a diagonal domina porque cada dia tem um equipamento que")
    print("      predomina: ar-condicionado na segunda, iluminacao na quinta")
    print("      e o projetor na terca)")

    chute = [0.0, 0.0, 0.0]
    x_jacobi, n_jacobi, hist_jacobi = jacobi(MATRIZ_A, VETOR_B, chute)
    x_seidel, n_seidel, hist_seidel = gauss_seidel(MATRIZ_A, VETOR_B, chute)

    for nome, historico in (("JACOBI", hist_jacobi), ("GAUSS-SEIDEL", hist_seidel)):
        print()
        print(f"  {nome} - chute inicial x(0) = (0, 0, 0), tolerancia {TOLERANCIA:g}")
        print(f"      {'k':>3} {'x1':>10} {'x2':>10} {'x3':>10} {'erro':>11}")
        for iteracao, valores, erro in historico[:6]:
            print(f"      {iteracao:>3} {valores[0]:>10.6f} {valores[1]:>10.6f} "
                  f"{valores[2]:>10.6f} {erro:>11.2e}")
        if len(historico) > 7:
            print(f"      {'...':>3}")
        iteracao, valores, erro = historico[-1]
        print(f"      {iteracao:>3} {valores[0]:>10.6f} {valores[1]:>10.6f} "
              f"{valores[2]:>10.6f} {erro:>11.2e}   <- convergiu")

    # ---- 1.6 Comparacao ----------------------------------------------------
    print()
    print(linha("-"))
    print("  1.6 COMPARACAO DOS QUATRO METODOS")
    print(linha("-"))
    print()
    print(f"      {'metodo':<18}{'tipo':<12}{'x1':>10}{'x2':>10}{'x3':>10}"
          f"{'iteracoes':>11}{'residuo':>11}")
    tabela_metodos = [
        ("Gauss", "direto", x_gauss, "-"),
        ("Fatoracao LU", "direto", x_lu, "-"),
        ("Jacobi", "iterativo", x_jacobi, str(n_jacobi)),
        ("Gauss-Seidel", "iterativo", x_seidel, str(n_seidel)),
    ]
    for nome, tipo, solucao, iteracoes in tabela_metodos:
        residuo = residuo_maximo(MATRIZ_A, VETOR_B, solucao)
        print(f"      {nome:<18}{tipo:<12}{solucao[0]:>10.6f}{solucao[1]:>10.6f}"
              f"{solucao[2]:>10.6f}{iteracoes:>11}{residuo:>11.1e}")

    print()
    print(f"  Gauss-Seidel precisou de {n_seidel} iteracoes contra {n_jacobi} de Jacobi")
    print("  para a mesma tolerancia, porque ja aproveita os valores atualizados")
    print("  dentro da propria iteracao. Os metodos diretos dao a resposta exata")
    print("  em um numero fixo de operacoes; os iterativos chegam perto dela com")
    print("  a precisao que a gente pedir - e sao os indicados para sistemas")
    print("  grandes e esparsos, onde a eliminacao ficaria cara demais.")

    print()
    print("  RESPOSTA DO PROBLEMA:")
    ordenados = sorted(zip(INCOGNITAS, x_gauss), key=lambda par: -par[1])
    for nome, valor in ordenados:
        print(f"      {nome:<26} = {br(valor, 3)} kW")
    nome_maior = ordenados[0][0].split("(")[1].rstrip(")")
    print(f"  O grupo de maior potencia media e a linha de {nome_maior}, "
          f"com {br(ordenados[0][1], 2)} kW.")

    return x_gauss


def parte_1_ajuste():
    print()
    print(linha("-"))
    print("  1.7 APLICACAO - AJUSTE DE CURVA POR MINIMOS QUADRADOS")
    print("      (o sistema normal tambem cai em um sistema linear)")
    print(linha("-"))

    coeficientes_por_grau = {}
    for grau, nome in ((1, "RETA"), (2, "PARABOLA")):
        coeficientes, matriz, termos = ajuste_minimos_quadrados(T, Y, grau)
        r2 = coeficiente_determinacao(T, Y, coeficientes)
        coeficientes_por_grau[grau] = (coeficientes, r2)
        print()
        print(f"  {nome} (grau {grau}) - sistema normal {len(matriz)}x{len(matriz)} "
              f"resolvido por Gauss:")
        mostrar_sistema(matriz, termos)
        print(f"      P(t) = {polinomio_em_texto(coeficientes)}")
        print(f"      R2 = {br(r2, 4)}")

    print()
    print(f"  A reta explica apenas {br(coeficientes_por_grau[1][1] * 100, 1)}% da variacao "
          f"e a parabola, {br(coeficientes_por_grau[2][1] * 100, 1)}%:")
    print("  o consumo nao e linear - sobe nos dias letivos e cai no fim de semana.")
    return coeficientes_por_grau[2][0]


def parte_2_interpolacao():
    print()
    print(linha())
    print("  PARTE 2 - INTERPOLACAO POLINOMIAL")
    print(linha())
    print()
    print("  Objetivo: obter o polinomio que passa EXATAMENTE pelos 7 pontos")
    print("  medidos, para estimar o consumo em instantes nao medidos.")
    print()
    print(f"  {'i':>2} {'t':>4} {'y (kWh)':>9}   dia")
    for i in range(len(T)):
        print(f"  {i:>2} {T[i]:>4.0f} {Y[i]:>9.0f}   {DIAS[i]}")

    # ---- 2.1 Newton --------------------------------------------------------
    print()
    print(linha("-"))
    print("  2.1 INTERPOLACAO DE NEWTON - DIFERENCAS DIVIDIDAS")
    print(linha("-"))
    coeficientes, tabela = diferencas_divididas(T, Y)
    print()
    print("  Tabela de diferencas divididas (o 1o valor de cada ordem e o")
    print("  coeficiente do polinomio):")
    print()
    for ordem in range(len(tabela)):
        valores = " ".join(f"{v:>9.4f}" for v in tabela[ordem])
        print(f"      ordem {ordem}: {valores}")
    print()
    print("  Polinomio interpolador de Newton (grau 6):")
    print(f"      P(t) = {br(coeficientes[0], 4)}")
    for ordem in range(1, len(coeficientes)):
        produtos = "".join(f"(t-{T[i]:.0f})" for i in range(ordem))
        sinal = "+" if coeficientes[ordem] >= 0 else "-"
        print(f"             {sinal} {br(abs(coeficientes[ordem]), 4)}{produtos}")

    desvio = max(abs(avaliar_newton(coeficientes, T, ti) - yi) for ti, yi in zip(T, Y))
    print()
    print(f"  Verificacao: max|P(ti) - yi| = {desvio:.2e}  (passa por todos os pontos)")

    # ---- 2.2 Lagrange ------------------------------------------------------
    print()
    print(linha("-"))
    print("  2.2 INTERPOLACAO DE LAGRANGE")
    print(linha("-"))
    print()
    print("  P(t) = soma de y_i * L_i(t), com L_i(t_i) = 1 e L_i(t_j) = 0.")
    print("  Conferindo os polinomios base em t = 3,5:")
    print()
    print(f"      {'i':>2} {'t_i':>5} {'y_i':>6} {'L_i(3,5)':>12} {'y_i * L_i(3,5)':>16}")
    soma = 0.0
    for i in range(len(T)):
        base = base_lagrange(T, i, 3.5)
        soma += Y[i] * base
        print(f"      {i:>2} {T[i]:>5.0f} {Y[i]:>6.0f} {base:>12.6f} {Y[i] * base:>16.6f}")
    print(f"      {'':>2} {'':>5} {'':>6} {'soma =':>12} {soma:>16.6f} kWh")

    print()
    print("  COMPARACAO NEWTON x LAGRANGE em varios instantes:")
    print()
    print(f"      {'t':>5} {'Newton':>12} {'Lagrange':>12} {'diferenca':>12} "
          f"{'linear':>10}")
    for x in (1.5, 3.5, 4.5, 5.5, 6.5):
        vn = avaliar_newton(coeficientes, T, x)
        vl = avaliar_lagrange(T, Y, x)
        vi = interpolacao_linear(T, Y, x)
        print(f"      {x:>5.1f} {vn:>12.6f} {vl:>12.6f} "
              f"{erro_absoluto(vn, vl):>12.1e} {vi:>10.4f}")
    print()
    print("  Os dois metodos dao o MESMO polinomio (as diferencas sao so erro de")
    print("  arredondamento): o interpolador de grau 6 por 7 pontos e unico.")
    print("  Newton e melhor quando novos pontos vao sendo acrescentados - basta")
    print("  um coeficiente novo; Lagrange exige refazer todas as bases.")

    # ---- 2.3 Runge ---------------------------------------------------------
    print()
    print(linha("-"))
    print("  2.3 CUIDADO COM O GRAU ALTO - FENOMENO DE RUNGE")
    print(linha("-"))
    amostras = [avaliar_newton(coeficientes, T, 1 + 0.01 * k) for k in range(601)]
    minimo, maximo = min(amostras), max(amostras)
    print()
    print(f"  Faixa dos dados medidos       : {min(Y):.0f} a {max(Y):.0f} kWh")
    print(f"  Faixa do polinomio de grau 6  : {br(minimo)} a {br(maximo)} kWh")
    print()
    print("  Entre o sabado e o domingo o polinomio despenca para perto de zero,")
    print("  um valor sem sentido fisico. Ele passa por todos os pontos, mas")
    print("  oscila entre eles. Por isso, para estimar valores intermediarios,")
    print("  a interpolacao linear ou o ajuste de grau baixo sao mais confiaveis.")
    return coeficientes


def parte_3_zeros(coeficientes_newton):
    media = sum(Y) / len(Y)

    print()
    print(linha())
    print("  PARTE 3 - ZEROS DE FUNCOES: METODO DA BISSECAO")
    print(linha())
    print()
    print("  PERGUNTA: em que momento exato o consumo da sala cruza a media")
    print(f"  semanal de {br(media)} kWh?")
    print()
    print("  Isso e achar as raizes de   f(t) = P(t) - media,")
    print("  onde P(t) e o polinomio interpolador obtido na Parte 2.")
    print("  (t inteiro marca o inicio do dia: t = 5,0 e a abertura da sexta)")

    def f(x):
        return avaliar_newton(coeficientes_newton, T, x) - media

    # ---- 3.1 Isolamento ----------------------------------------------------
    print()
    print(linha("-"))
    print("  3.1 ISOLAMENTO DAS RAIZES - TEOREMA DE BOLZANO")
    print(linha("-"))
    print()
    print("  Varrendo [1, 7] de 0,05 em 0,05 a procura de f(a).f(b) < 0:")
    intervalos = isolar_raizes(f, T[0], T[-1], passo=0.05)
    print()
    for a, b in intervalos:
        print(f"      [{a:.2f}, {b:.2f}]   f(a) = {f(a):>9.5f}   f(b) = {f(b):>9.5f}"
              f"   produto < 0  ->  ha raiz")
    print(f"      {len(intervalos)} raizes isoladas.")

    # ---- 3.2 Bissecao ------------------------------------------------------
    print()
    print(linha("-"))
    print("  3.2 REFINAMENTO PELO METODO DA BISSECAO")
    print(linha("-"))

    raizes = []
    for numero, (a, b) in enumerate(intervalos, start=1):
        raiz, iteracoes, historico = bissecao(f, a, b)
        raizes.append(raiz)
        print()
        print(f"  RAIZ {numero} - intervalo inicial [{a:.2f}, {b:.2f}]")
        print(f"      {'k':>3} {'a':>10} {'b':>10} {'x=(a+b)/2':>12} {'f(x)':>12} "
              f"{'erro':>10}")
        for k, ai, bi, meio, f_meio, erro in historico[:5]:
            print(f"      {k:>3} {ai:>10.6f} {bi:>10.6f} {meio:>12.6f} "
                  f"{f_meio:>12.6f} {erro:>10.2e}")
        if len(historico) > 6:
            print(f"      {'...':>3}")
        k, ai, bi, meio, f_meio, erro = historico[-1]
        print(f"      {k:>3} {ai:>10.6f} {bi:>10.6f} {meio:>12.6f} "
              f"{f_meio:>12.6f} {erro:>10.2e}  <- parou")

        hora = (raiz - int(raiz)) * 24
        print(f"      RAIZ = {raiz:.6f}  em {iteracoes} iteracoes")
        print(f"      Significado: {DIAS[int(raiz) - 1]}, por volta das "
              f"{int(hora):02d}h{int((hora % 1) * 60):02d}")

    # ---- 3.3 Iteracoes teoricas -------------------------------------------
    print()
    print(linha("-"))
    print("  3.3 NUMERO DE ITERACOES PREVISTO PELA TEORIA")
    print(linha("-"))
    a, b = intervalos[-1]
    previsto = iteracoes_teoricas_bissecao(a, b)
    _, real, _ = bissecao(f, a, b)
    print()
    print(f"      k > log2( (b - a) / tol ) = log2( {b - a:.2f} / {TOLERANCIA:g} ) "
          f"= {previsto}")
    print(f"      iteracoes realmente gastas na ultima raiz: {real}")
    print("      Confere. Essa e uma vantagem da bissecao: da para prever o")
    print("      custo antes de rodar, porque o erro cai pela metade a cada passo.")

    # ---- 3.4 Comparacao com Newton-Raphson --------------------------------
    print()
    print(linha("-"))
    print("  3.4 COMPARACAO COM NEWTON-RAPHSON")
    print(linha("-"))
    chute = (a + b) / 2
    raiz_newton, iteracoes_newton, historico_newton = newton_raphson(
        f, lambda x: derivada_central(f, x), chute)
    print()
    print(f"      {'k':>3} {'x(k)':>12} {'f(x)':>12} {'derivada':>12} {'erro':>11}")
    for k, x, fx, dfx, novo, erro in historico_newton:
        print(f"      {k:>3} {x:>12.6f} {fx:>12.6f} {dfx:>12.5f} {erro:>11.2e}")
    print()
    print(f"      Bissecao       : t = {raizes[-1]:.8f}  em {real:>2} iteracoes")
    print(f"      Newton-Raphson : t = {raiz_newton:.8f}  em {iteracoes_newton:>2} iteracoes")
    print(f"      Diferenca entre as raizes: "
          f"{erro_absoluto(raizes[-1], raiz_newton):.2e}")
    print()
    print("      A bissecao e mais lenta, mas so precisa da troca de sinal e")
    print("      nunca diverge. Newton e bem mais rapido, porem depende da")
    print("      derivada e de um bom chute inicial.")
    return raizes, media


def relatorio():
    print()
    print(linha())
    print("   METODOS NUMERICOS APLICADOS A ANALISE DO CONSUMO DE ENERGIA")
    print("   Sistemas lineares (diretos e iterativos) | Interpolacao de")
    print("   Newton e Lagrange | Zeros de funcoes pela bissecao")
    print(linha())

    solucao_sistema = parte_1_sistemas_lineares()
    coeficientes_parabola = parte_1_ajuste()
    coeficientes_newton = parte_2_interpolacao()
    raizes, media = parte_3_zeros(coeficientes_newton)

    print()
    print(linha())
    print("  RESUMO DO QUE FOI APLICADO")
    print(linha())
    print("   PARTE 1  Sistemas lineares 3x3 (potencia de cada equipamento)")
    print("            - diretos   : Eliminacao de Gauss e Fatoracao LU")
    print("            - iterativos: Jacobi e Gauss-Seidel (criterio das linhas)")
    print(f"            - solucao   : x = ({br(solucao_sistema[0], 3)}, "
          f"{br(solucao_sistema[1], 3)}, {br(solucao_sistema[2], 3)}) kW")
    print("   PARTE 2  Interpolacao de Newton e de Lagrange (grau 6, identicas)")
    print("            - risco do grau alto: fenomeno de Runge")
    print("   PARTE 3  Zeros de funcoes: isolamento por Bolzano + bissecao")
    print(f"            - raizes    : " +
          ", ".join(f"t = {r:.4f}" for r in raizes))
    print(linha())
    print()

    return {
        "media": media,
        "coef_parabola": coeficientes_parabola,
        "coef_newton": coeficientes_newton,
        "raizes": raizes,
        "solucao_sistema": solucao_sistema,
    }


# =============================================================================
# GRAFICOS (SVG puro - abrem no navegador, sem instalar nada)
# =============================================================================
def grafico_interpolacao(resultados, caminho_svg):
    """
    Pontos medidos + polinomio interpolador de Newton/Lagrange (grau 6) +
    ajuste de minimos quadrados + linha da media + raizes achadas na bissecao.
    """
    largura, altura = 960, 560
    m_esq, m_dir, m_topo, m_base = 72, 34, 78, 96
    area_l, area_a = largura - m_esq - m_dir, altura - m_topo - m_base

    media = resultados["media"]
    coef_newton = resultados["coef_newton"]
    coef_parabola = resultados["coef_parabola"]

    amostras = [avaliar_newton(coef_newton, T, 1 + 0.01 * k) for k in range(601)]
    y_min = min(min(amostras), 0.0)
    y_max = max(max(amostras), max(Y)) * 1.06

    def px(t):
        return m_esq + (t - T[0]) / (T[-1] - T[0]) * area_l

    def py(v):
        return m_topo + area_a - (v - y_min) / (y_max - y_min) * area_a

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" '
           f'viewBox="0 0 {largura} {altura}" font-family="Segoe UI, Arial, sans-serif">',
           f'<rect width="{largura}" height="{altura}" fill="#ffffff"/>',
           f'<text x="{largura/2}" y="30" text-anchor="middle" font-size="19" '
           f'font-weight="700" fill="#1b1b1b">Interpolacao polinomial e zeros de '
           f'funcoes</text>',
           f'<text x="{largura/2}" y="52" text-anchor="middle" font-size="12.5" '
           f'fill="#666">Newton e Lagrange (grau 6) sobre os 7 pontos medidos; '
           f'raizes de f(t) = P(t) - media pelo metodo da bissecao</text>']

    valor = int(y_min // 10) * 10
    while valor <= y_max:
        yy = py(valor)
        if m_topo - 2 <= yy <= m_topo + area_a + 2:
            svg.append(f'<line x1="{m_esq}" y1="{yy:.1f}" x2="{largura - m_dir}" '
                       f'y2="{yy:.1f}" stroke="#ededed"/>')
            svg.append(f'<text x="{m_esq - 10}" y="{yy + 4:.1f}" text-anchor="end" '
                       f'font-size="11.5" fill="#777">{valor}</text>')
        valor += 10

    svg.append(f'<line x1="{m_esq}" y1="{py(0):.1f}" x2="{largura - m_dir}" '
               f'y2="{py(0):.1f}" stroke="#1b1b1b" stroke-width="1.5"/>')
    for t, dia in zip(T, DIAS):
        svg.append(f'<line x1="{px(t):.1f}" y1="{py(0):.1f}" x2="{px(t):.1f}" '
                   f'y2="{py(0) + 5:.1f}" stroke="#1b1b1b"/>')
        svg.append(f'<text x="{px(t):.1f}" y="{m_topo + area_a + 26:.1f}" '
                   f'text-anchor="middle" font-size="12" fill="#1b1b1b">{dia}</text>')
        svg.append(f'<text x="{px(t):.1f}" y="{m_topo + area_a + 42:.1f}" '
                   f'text-anchor="middle" font-size="10.5" fill="#999">t={t:.0f}</text>')

    curva = " ".join(f"{px(1 + 0.01 * k):.1f},{py(amostras[k]):.1f}" for k in range(601))
    svg.append(f'<polyline points="{curva}" fill="none" stroke="#e4572e" stroke-width="2.4"/>')

    curva2 = " ".join(f"{px(1 + 0.01 * k):.1f},"
                      f"{py(avaliar_polinomio(coef_parabola, 1 + 0.01 * k)):.1f}"
                      for k in range(601))
    svg.append(f'<polyline points="{curva2}" fill="none" stroke="#7048e8" '
               f'stroke-width="2.1" stroke-dasharray="8,5"/>')

    svg.append(f'<line x1="{m_esq}" y1="{py(media):.1f}" x2="{largura - m_dir}" '
               f'y2="{py(media):.1f}" stroke="#2b9348" stroke-width="2" '
               f'stroke-dasharray="4,4"/>')

    for raiz in resultados["raizes"]:
        svg.append(f'<circle cx="{px(raiz):.1f}" cy="{py(media):.1f}" r="6.5" '
                   f'fill="#ffffff" stroke="#2b9348" stroke-width="3"/>')
        svg.append(f'<text x="{px(raiz):.1f}" y="{py(media) + 22:.1f}" '
                   f'text-anchor="middle" font-size="11.5" font-weight="700" '
                   f'fill="#2b9348">raiz t={raiz:.3f}</text>')

    for t, v in zip(T, Y):
        svg.append(f'<circle cx="{px(t):.1f}" cy="{py(v):.1f}" r="6" fill="#1b1b1b"/>')
        svg.append(f'<text x="{px(t):.1f}" y="{py(v) - 13:.1f}" text-anchor="middle" '
                   f'font-size="12.5" font-weight="700" fill="#1b1b1b">{v:.0f}</text>')

    itens = [("#1b1b1b", "Pontos medidos"),
             ("#e4572e", "Interpolador de Newton/Lagrange (grau 6)"),
             ("#7048e8", "Ajuste por minimos quadrados (grau 2)"),
             ("#2b9348", f"Media = {br(media)} kWh e raizes")]
    x_legenda = m_esq
    for cor, texto in itens:
        svg.append(f'<rect x="{x_legenda}" y="{altura - 34}" width="15" height="4" '
                   f'rx="2" fill="{cor}"/>')
        svg.append(f'<text x="{x_legenda + 21}" y="{altura - 27}" font-size="12" '
                   f'fill="#444">{texto}</text>')
        x_legenda += 22 + len(texto) * 6.5

    svg.append(f'<text x="20" y="{m_topo + area_a / 2}" font-size="12.5" fill="#444" '
               f'transform="rotate(-90 20 {m_topo + area_a / 2})" '
               f'text-anchor="middle">Consumo (kWh)</text>')
    svg.append("</svg>")

    with open(caminho_svg, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(svg))
    print(f"  [OK] Grafico salvo em: {caminho_svg}")


def grafico_convergencia(caminho_svg):
    """
    Compara a convergencia de Jacobi e Gauss-Seidel: erro de cada iteracao
    em escala logaritmica (uma linha reta para baixo = convergencia linear).
    """
    import math

    _, _, hist_jacobi = jacobi(MATRIZ_A, VETOR_B, [0.0, 0.0, 0.0])
    _, _, hist_seidel = gauss_seidel(MATRIZ_A, VETOR_B, [0.0, 0.0, 0.0])

    largura, altura = 900, 500
    m_esq, m_dir, m_topo, m_base = 76, 36, 78, 84
    area_l, area_a = largura - m_esq - m_dir, altura - m_topo - m_base

    max_iteracoes = max(len(hist_jacobi), len(hist_seidel))
    exp_min, exp_max = -7, 2

    def px(k):
        return m_esq + (k - 1) / max(max_iteracoes - 1, 1) * area_l

    def py(erro):
        expoente = math.log10(max(erro, 1e-12))
        expoente = min(max(expoente, exp_min), exp_max)
        return m_topo + area_a - (expoente - exp_min) / (exp_max - exp_min) * area_a

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" '
           f'viewBox="0 0 {largura} {altura}" font-family="Segoe UI, Arial, sans-serif">',
           f'<rect width="{largura}" height="{altura}" fill="#ffffff"/>',
           f'<text x="{largura/2}" y="30" text-anchor="middle" font-size="19" '
           f'font-weight="700" fill="#1b1b1b">Metodos iterativos: Jacobi x '
           f'Gauss-Seidel</text>',
           f'<text x="{largura/2}" y="52" text-anchor="middle" font-size="12.5" '
           f'fill="#666">Erro de cada iteracao (escala logaritmica) no sistema '
           f'3x3 dos equipamentos</text>']

    for expoente in range(exp_min, exp_max + 1):
        yy = py(10.0 ** expoente)
        svg.append(f'<line x1="{m_esq}" y1="{yy:.1f}" x2="{largura - m_dir}" '
                   f'y2="{yy:.1f}" stroke="#ededed"/>')
        svg.append(f'<text x="{m_esq - 10}" y="{yy + 4:.1f}" text-anchor="end" '
                   f'font-size="11.5" fill="#777">1e{expoente}</text>')

    # linha da tolerancia
    y_tol = py(TOLERANCIA)
    svg.append(f'<line x1="{m_esq}" y1="{y_tol:.1f}" x2="{largura - m_dir}" '
               f'y2="{y_tol:.1f}" stroke="#2b9348" stroke-width="2" '
               f'stroke-dasharray="6,5"/>')
    svg.append(f'<text x="{m_esq + 8}" y="{y_tol - 8:.1f}" text-anchor="start" '
               f'font-size="12" font-weight="700" fill="#2b9348">'
               f'tolerancia = {TOLERANCIA:g}</text>')

    svg.append(f'<line x1="{m_esq}" y1="{m_topo + area_a:.1f}" x2="{largura - m_dir}" '
               f'y2="{m_topo + area_a:.1f}" stroke="#1b1b1b" stroke-width="1.5"/>')
    for k in range(1, max_iteracoes + 1):
        if k == 1 or k == max_iteracoes or (k % 5 == 0 and abs(k - max_iteracoes) > 2):
            svg.append(f'<text x="{px(k):.1f}" y="{m_topo + area_a + 20:.1f}" '
                       f'text-anchor="middle" font-size="11.5" fill="#555">{k}</text>')

    for historico, cor, nome in ((hist_jacobi, "#e4572e", "Jacobi"),
                                 (hist_seidel, "#3f8efc", "Gauss-Seidel")):
        pontos = " ".join(f"{px(k):.1f},{py(erro):.1f}" for k, _, erro in historico)
        svg.append(f'<polyline points="{pontos}" fill="none" stroke="{cor}" '
                   f'stroke-width="2.6"/>')
        for k, _, erro in historico:
            svg.append(f'<circle cx="{px(k):.1f}" cy="{py(erro):.1f}" r="3.4" fill="{cor}"/>')
        k_final, _, erro_final = historico[-1]
        x_rotulo = px(k_final)
        ancora = "middle"
        if x_rotulo > largura - m_dir - 90:      # perto da borda direita
            x_rotulo, ancora = x_rotulo - 8, "end"
        svg.append(f'<text x="{x_rotulo:.1f}" y="{py(erro_final) + 24:.1f}" '
                   f'text-anchor="{ancora}" font-size="12" font-weight="700" '
                   f'fill="{cor}">{nome}: {len(historico)} iteracoes</text>')

    svg.append(f'<text x="{largura/2}" y="{altura - 40}" text-anchor="middle" '
               f'font-size="12.5" fill="#555">Numero da iteracao (k)</text>')
    svg.append(f'<text x="22" y="{m_topo + area_a / 2}" font-size="12.5" fill="#444" '
               f'transform="rotate(-90 22 {m_topo + area_a / 2})" text-anchor="middle">'
               f'Erro max|x(k) - x(k-1)|</text>')
    svg.append(f'<text x="{largura/2}" y="{altura - 18}" text-anchor="middle" '
               f'font-size="12" fill="#777">Quanto mais inclinada a linha, mais '
               f'rapida a convergencia</text>')
    svg.append("</svg>")

    with open(caminho_svg, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(svg))
    print(f"  [OK] Grafico salvo em: {caminho_svg}")


def main():
    resultados = relatorio()
    pasta = os.path.dirname(os.path.abspath(__file__))
    print("  GERANDO OS GRAFICOS...")
    grafico_convergencia(os.path.join(pasta, "grafico_convergencia.svg"))
    grafico_interpolacao(resultados, os.path.join(pasta, "grafico_interpolacao.svg"))
    print()


if __name__ == "__main__":
    main()
