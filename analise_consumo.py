# -*- coding: utf-8 -*-
"""
=============================================================================
 ANALISE DO CONSUMO DE ENERGIA ELETRICA - SALA DE AULA (7 DIAS)
=============================================================================
 Situacao-problema:
   Uma escola deseja analisar o consumo de energia eletrica de uma sala de
   aula durante 7 dias (de segunda a domingo).

 O programa:
   1) Armazena os valores de consumo em uma lista (vetor)
   2) Calcula o consumo total da semana
   3) Calcula o consumo medio diario
   4) Identifica o maior consumo e em qual dia ocorreu
   5) Identifica o menor consumo e em qual dia ocorreu
   6) Determina quais dias tiveram consumo acima da media
   7) Calcula a % de reducao do domingo em relacao ao dia de maior consumo
   8) Apresenta os resultados de forma organizada
   9) Gera um grafico de barras com o consumo de cada dia

 Apresentacao: Joao Pedro e Vitor
=============================================================================
"""

import os

# ---------------------------------------------------------------------------
# 1) ARMAZENAMENTO DOS DADOS EM VETORES (LISTAS)
# ---------------------------------------------------------------------------
# Duas listas "paralelas": o indice 0 de uma corresponde ao indice 0 da outra.
#   dias[0]     -> "Segunda"     consumos[0] -> 18
#   dias[1]     -> "Terca"       consumos[1] -> 22   ... e assim por diante.
DIAS = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
CONSUMOS = [18, 22, 20, 25, 30, 12, 10]   # em kWh

UNIDADE = "kWh"


# ---------------------------------------------------------------------------
# FUNCAO AUXILIAR: formata numero no padrao brasileiro (virgula decimal)
# ---------------------------------------------------------------------------
def br(valor, casas=2):
    """Converte 19.571428 -> '19,57' (padrao brasileiro)."""
    return f"{valor:.{casas}f}".replace(".", ",")


# ---------------------------------------------------------------------------
# 2) CONSUMO TOTAL DA SEMANA
# ---------------------------------------------------------------------------
def calcular_total(consumos):
    """Soma todos os consumos da lista e devolve o total da semana."""
    total = 0
    for valor in consumos:       # percorre cada consumo da lista
        total = total + valor    # acumula no total
    return total
    # Obs.: em Python o mesmo resultado sairia com a funcao pronta sum(consumos)


# ---------------------------------------------------------------------------
# 3) CONSUMO MEDIO DIARIO
# ---------------------------------------------------------------------------
def calcular_media(consumos):
    """Media = soma dos consumos dividida pela quantidade de dias."""
    return calcular_total(consumos) / len(consumos)


# ---------------------------------------------------------------------------
# 4) MAIOR CONSUMO E EM QUAL DIA OCORREU
# ---------------------------------------------------------------------------
def encontrar_maior(dias, consumos):
    """Devolve uma tupla (dia, valor) com o maior consumo da semana."""
    indice_maior = 0
    for i in range(1, len(consumos)):
        if consumos[i] > consumos[indice_maior]:
            indice_maior = i
    return dias[indice_maior], consumos[indice_maior]


# ---------------------------------------------------------------------------
# 5) MENOR CONSUMO E EM QUAL DIA OCORREU
# ---------------------------------------------------------------------------
def encontrar_menor(dias, consumos):
    """Devolve uma tupla (dia, valor) com o menor consumo da semana."""
    indice_menor = 0
    for i in range(1, len(consumos)):
        if consumos[i] < consumos[indice_menor]:
            indice_menor = i
    return dias[indice_menor], consumos[indice_menor]


# ---------------------------------------------------------------------------
# 6) DIAS COM CONSUMO ACIMA DA MEDIA
# ---------------------------------------------------------------------------
def dias_acima_da_media(dias, consumos, media):
    """Devolve uma lista de tuplas (dia, valor) dos dias acima da media."""
    acima = []
    for i in range(len(consumos)):
        if consumos[i] > media:
            acima.append((dias[i], consumos[i]))
    return acima


# ---------------------------------------------------------------------------
# 7) PORCENTAGEM DE REDUCAO DO DOMINGO EM RELACAO AO DIA DE MAIOR CONSUMO
# ---------------------------------------------------------------------------
def calcular_reducao(valor_referencia, valor_comparado):
    """
    Formula:  reducao (%) = (referencia - comparado) / referencia * 100

    Ex.: referencia = 30 kWh (sexta)  e  comparado = 10 kWh (domingo)
         (30 - 10) / 30 * 100 = 66,67%  ->  o domingo gastou 66,67% a menos.
    """
    if valor_referencia == 0:              # protecao contra divisao por zero
        return 0.0
    return (valor_referencia - valor_comparado) / valor_referencia * 100


# ---------------------------------------------------------------------------
# 8) APRESENTACAO ORGANIZADA DOS RESULTADOS
# ---------------------------------------------------------------------------
def linha(caractere="=", tamanho=62):
    return caractere * tamanho


def exibir_relatorio(dias, consumos):
    """Imprime o relatorio completo da analise no terminal."""

    total = calcular_total(consumos)
    media = calcular_media(consumos)
    dia_maior, valor_maior = encontrar_maior(dias, consumos)
    dia_menor, valor_menor = encontrar_menor(dias, consumos)
    acima = dias_acima_da_media(dias, consumos, media)

    consumo_domingo = consumos[dias.index("Domingo")]
    reducao = calcular_reducao(valor_maior, consumo_domingo)

    print()
    print(linha())
    print("   ANALISE DO CONSUMO DE ENERGIA ELETRICA - SALA DE AULA")
    print("   Periodo analisado: 7 dias (segunda a domingo)")
    print(linha())

    # ---- Tabela de consumos -------------------------------------------------
    print()
    print("  [1] CONSUMO REGISTRADO EM CADA DIA")
    print()
    print(f"  {'DIA':<12} {'CONSUMO (kWh)':>14}   {'SITUACAO':<18}")
    print(f"  {linha('-', 12)} {linha('-', 14):>14}   {linha('-', 18)}")
    for i in range(len(dias)):
        if consumos[i] > media:
            situacao = "ACIMA da media"
        elif consumos[i] < media:
            situacao = "abaixo da media"
        else:
            situacao = "igual a media"
        print(f"  {dias[i]:<12} {consumos[i]:>14}   {situacao:<18}")

    # ---- Indicadores --------------------------------------------------------
    print()
    print("  [2] CONSUMO TOTAL DA SEMANA")
    print(f"      {br(total)} {UNIDADE}")

    print()
    print("  [3] CONSUMO MEDIO DIARIO")
    print(f"      {br(media)} {UNIDADE}/dia")
    print(f"      (calculo: {total} {UNIDADE} / {len(dias)} dias)")

    print()
    print("  [4] MAIOR CONSUMO DA SEMANA")
    print(f"      {br(valor_maior)} {UNIDADE}  ->  {dia_maior}")

    print()
    print("  [5] MENOR CONSUMO DA SEMANA")
    print(f"      {br(valor_menor)} {UNIDADE}  ->  {dia_menor}")

    print()
    print("  [6] DIAS COM CONSUMO ACIMA DA MEDIA")
    if acima:
        for dia, valor in acima:
            diferenca = valor - media
            print(f"      - {dia:<10} {br(valor)} {UNIDADE}   "
                  f"(+{br(diferenca)} {UNIDADE} acima da media)")
    else:
        print("      - Nenhum dia ficou acima da media.")

    print()
    print("  [7] REDUCAO DO CONSUMO NO DOMINGO")
    print(f"      Dia de maior consumo : {dia_maior} = {br(valor_maior)} {UNIDADE}")
    print(f"      Domingo              : {br(consumo_domingo)} {UNIDADE}")
    print(f"      Calculo: ({valor_maior} - {consumo_domingo}) / {valor_maior} x 100")
    print(f"      >>> REDUCAO DE {br(reducao)}%")

    # ---- Conclusao ----------------------------------------------------------
    print()
    print(linha())
    print("  CONCLUSAO")
    print(linha())
    print(f"  O consumo cresce ao longo dos dias letivos e atinge o pico em")
    print(f"  {dia_maior} ({br(valor_maior)} {UNIDADE}). No fim de semana, sem aulas,")
    print(f"  o consumo cai ate o minimo de {br(valor_menor)} {UNIDADE} em {dia_menor} -")
    print(f"  uma reducao de {br(reducao)}% em relacao ao pico.")
    print(f"  Isso mostra que o gasto esta diretamente ligado a ocupacao da")
    print(f"  sala, e que a acao de economia deve focar nos dias letivos.")
    print(linha())
    print()

    # devolve os resultados para serem usados pelo grafico
    return {
        "total": total,
        "media": media,
        "dia_maior": dia_maior,
        "valor_maior": valor_maior,
        "dia_menor": dia_menor,
        "valor_menor": valor_menor,
        "acima": acima,
        "reducao": reducao,
    }


# ---------------------------------------------------------------------------
# 9) GRAFICO DE BARRAS
# ---------------------------------------------------------------------------
# Sao oferecidas 3 saidas, para o programa nunca ficar sem grafico:
#   (a) matplotlib  -> janela + arquivo PNG   (usado quando a lib existe)
#   (b) SVG         -> arquivo que abre no navegador (sem instalar nada)
#   (c) ASCII       -> grafico desenhado no proprio terminal
# ---------------------------------------------------------------------------

COR_ACIMA = "#e4572e"   # laranja  -> dias acima da media
COR_ABAIXO = "#3f8efc"  # azul     -> dias abaixo da media
COR_MEDIA = "#2b9348"   # verde    -> linha da media


def grafico_matplotlib(dias, consumos, media, dia_maior, dia_menor, caminho_png):
    """Gera o grafico de barras com matplotlib. Retorna True se conseguiu."""
    try:
        import matplotlib
        matplotlib.use("Agg") if not os.environ.get("DISPLAY") else None
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    cores = [COR_ACIMA if v > media else COR_ABAIXO for v in consumos]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    barras = ax.bar(dias, consumos, color=cores, edgecolor="white", linewidth=1.5)

    # valor escrito em cima de cada barra
    for barra, valor in zip(barras, consumos):
        ax.text(barra.get_x() + barra.get_width() / 2, valor + 0.6,
                f"{valor}", ha="center", va="bottom", fontweight="bold")

    # linha da media
    ax.axhline(media, color=COR_MEDIA, linestyle="--", linewidth=2,
               label=f"Media diaria = {br(media)} kWh")

    ax.set_title("Consumo de Energia Eletrica da Sala de Aula (7 dias)",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Dia da semana")
    ax.set_ylabel("Consumo (kWh)")
    ax.set_ylim(0, max(consumos) * 1.20)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left")

    fig.text(0.5, 0.01,
             f"Maior consumo: {dia_maior}  |  Menor consumo: {dia_menor}  |  "
             f"Laranja = acima da media, Azul = abaixo da media",
             ha="center", fontsize=9, color="#555555")

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(caminho_png, dpi=120)
    print(f"  [OK] Grafico salvo em: {caminho_png}")

    if os.environ.get("DISPLAY"):
        plt.show()
    return True


def grafico_svg(dias, consumos, media, dia_maior, dia_menor, caminho_svg):
    """
    Gera o grafico de barras em SVG puro (arquivo que abre no navegador).
    Nao depende de nenhuma biblioteca externa.
    """
    largura, altura = 920, 520
    m_esq, m_dir, m_topo, m_base = 70, 30, 70, 90
    area_l = largura - m_esq - m_dir
    area_a = altura - m_topo - m_base

    maximo = max(consumos)
    topo_escala = ((int(maximo * 1.15) // 5) + 1) * 5   # arredonda p/ multiplo de 5

    def y(valor):
        return m_topo + area_a - (valor / topo_escala) * area_a

    passo = area_l / len(consumos)
    larg_barra = passo * 0.58

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" '
               f'height="{altura}" viewBox="0 0 {largura} {altura}" '
               f'font-family="Segoe UI, Arial, sans-serif">')
    svg.append(f'<rect width="{largura}" height="{altura}" fill="#ffffff"/>')
    svg.append(f'<text x="{largura/2}" y="34" text-anchor="middle" font-size="21" '
               f'font-weight="700" fill="#1b1b1b">Consumo de Energia Eletrica da '
               f'Sala de Aula (7 dias)</text>')
    svg.append(f'<text x="{largura/2}" y="56" text-anchor="middle" font-size="13" '
               f'fill="#666">Laranja = acima da media | Azul = abaixo da media</text>')

    # linhas de grade + eixo Y
    for valor in range(0, topo_escala + 1, 5):
        yy = y(valor)
        svg.append(f'<line x1="{m_esq}" y1="{yy:.1f}" x2="{largura - m_dir}" '
                   f'y2="{yy:.1f}" stroke="#e3e3e3" stroke-width="1"/>')
        svg.append(f'<text x="{m_esq - 12}" y="{yy + 4:.1f}" text-anchor="end" '
                   f'font-size="12" fill="#666">{valor}</text>')

    svg.append(f'<text x="20" y="{m_topo + area_a/2}" font-size="13" fill="#444" '
               f'transform="rotate(-90 20 {m_topo + area_a/2})" '
               f'text-anchor="middle">Consumo (kWh)</text>')

    # barras
    for i, (dia, valor) in enumerate(zip(dias, consumos)):
        x = m_esq + i * passo + (passo - larg_barra) / 2
        topo = y(valor)
        alt = m_topo + area_a - topo
        cor = COR_ACIMA if valor > media else COR_ABAIXO
        svg.append(f'<rect x="{x:.1f}" y="{topo:.1f}" width="{larg_barra:.1f}" '
                   f'height="{alt:.1f}" fill="{cor}" rx="4"/>')

        # se o rotulo bater na linha da media, ele e escrito dentro da barra
        if abs((topo - 9) - y(media)) < 14:
            y_rotulo, cor_rotulo = topo + 20, "#ffffff"
        else:
            y_rotulo, cor_rotulo = topo - 9, "#1b1b1b"
        svg.append(f'<text x="{x + larg_barra/2:.1f}" y="{y_rotulo:.1f}" '
                   f'text-anchor="middle" font-size="14" font-weight="700" '
                   f'fill="{cor_rotulo}">{valor}</text>')

        rotulo = dia
        if dia == dia_maior:
            rotulo = dia + "  (MAIOR)"
        elif dia == dia_menor:
            rotulo = dia + "  (MENOR)"
        svg.append(f'<text x="{x + larg_barra/2:.1f}" y="{m_topo + area_a + 24:.1f}" '
                   f'text-anchor="middle" font-size="12.5" fill="#1b1b1b">{rotulo}</text>')

    # eixo X
    svg.append(f'<line x1="{m_esq}" y1="{m_topo + area_a}" x2="{largura - m_dir}" '
               f'y2="{m_topo + area_a}" stroke="#1b1b1b" stroke-width="1.6"/>')

    # linha da media
    ym = y(media)
    svg.append(f'<line x1="{m_esq}" y1="{ym:.1f}" x2="{largura - m_dir}" '
               f'y2="{ym:.1f}" stroke="{COR_MEDIA}" stroke-width="2.4" '
               f'stroke-dasharray="9,6"/>')
    svg.append(f'<text x="{largura - m_dir - 6}" y="{ym - 8:.1f}" text-anchor="end" '
               f'font-size="13" font-weight="700" fill="{COR_MEDIA}">'
               f'Media = {br(media)} kWh</text>')

    svg.append(f'<text x="{largura/2}" y="{altura - 18}" text-anchor="middle" '
               f'font-size="12.5" fill="#555">Dia da semana</text>')
    svg.append("</svg>")

    with open(caminho_svg, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(svg))
    print(f"  [OK] Grafico salvo em: {caminho_svg}")
    print("       (abra este arquivo no navegador para projetar)")


def grafico_ascii(dias, consumos, media):
    """Desenha o grafico de barras no proprio terminal (sempre funciona)."""
    largura_max = 42
    maximo = max(consumos)

    print()
    print(linha())
    print("   GRAFICO DE BARRAS - CONSUMO POR DIA (kWh)")
    print(linha())
    print()
    for dia, valor in zip(dias, consumos):
        blocos = int(round(valor / maximo * largura_max))
        marca = "<<< MAIOR" if valor == maximo else ""
        if valor == min(consumos):
            marca = "<<< MENOR"
        print(f"  {dia:<9} | {'#' * blocos} {valor:>2} {marca}")
    print(f"  {'':<9} +{'-' * (largura_max + 2)}")

    # regua do eixo horizontal
    escala = "  " + " " * 12
    marcas = ""
    for valor in range(0, maximo + 1, 5):
        pos = int(round(valor / maximo * largura_max))
        marcas = marcas.ljust(pos) + str(valor)
    print(escala + marcas)
    print()
    print(f"  Media diaria = {br(media)} kWh  "
          f"(barras maiores que isso = dias acima da media)")
    print(linha())


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
def main():
    # Passos 1 a 8: calculos e relatorio
    resultados = exibir_relatorio(DIAS, CONSUMOS)

    # Passo 9: grafico de barras
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho_png = os.path.join(pasta, "grafico_consumo.png")
    caminho_svg = os.path.join(pasta, "grafico_consumo.svg")

    print("  [9] GERANDO O GRAFICO DE BARRAS...")
    print()

    usou_matplotlib = grafico_matplotlib(
        DIAS, CONSUMOS, resultados["media"],
        resultados["dia_maior"], resultados["dia_menor"], caminho_png
    )
    if not usou_matplotlib:
        print("  [i] matplotlib nao instalado - gerando o grafico em SVG.")
        print("      (para usar matplotlib: sudo apt install python3-matplotlib)")

    # o SVG e o ASCII sao sempre gerados, como garantia na apresentacao
    grafico_svg(DIAS, CONSUMOS, resultados["media"],
                resultados["dia_maior"], resultados["dia_menor"], caminho_svg)
    grafico_ascii(DIAS, CONSUMOS, resultados["media"])


if __name__ == "__main__":
    main()
