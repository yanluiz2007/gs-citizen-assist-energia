TARIFA_KWH = 1.01883
FATOR_CO2_KG_POR_KWH = 0.0385
DIAS_NO_MES = 30
MESES_NO_ANO = 12

POTENCIA_INVERNO_W = 5500
POTENCIA_VERAO_W = 3500

MINUTOS_BANHO_ATUAL = 8
MINUTOS_BANHO_CONSCIENTE = 5

FRACAO_ECONOMIA_SOLAR = 0.50
CUSTO_AQUECEDOR_SOLAR = 3300.00
CUSTO_SOLAR_MIN = 2300.00
CUSTO_SOLAR_MAX = 4300.00
CUSTO_AQUECEDOR_GRANDE = 3800.00
PESSOAS_AQUECEDOR_PEQUENO = 4
BANHO_MEDIO_ESTUDO = 5.15

LIMITE_TARIFA_SOCIAL_KWH = 80

HISTORICO_CONSUMO = {
    "out/25": 520, "nov/25": 493, "dez/25": 485, "jan/26": 536,
    "fev/26": 488, "mar/26": 481, "abr/26": 560, "mai/26": 492,
    "jun/26": 435, "jul/26": 573, "ago/26": 502, "set/26": 609,
}

FONTES = [
    "Tarifa: conta de luz Enel SP, classe B1 residencial, set/2026",
    "Reajuste Enel SP 2026: InfoMoney, 30/06/2026",
    "Chuveiro = 24% do consumo residencial: Eletrobras/Procel (citado na RBENS, 2011)",
    "Banho médio de 5,15 min e economia do aquecedor solar: RBENS, 2011",
    "Preço do aquecedor solar: Cronoshare, preços 2026",
    "Emissão de CO2 da rede elétrica: MCTI (O Setor Elétrico, 2024)",
    "Tarifa Social: SBT News, 04/07/2025",
]

LIMITACOES = [
    "Os valores são estimativas e não garantem economia.",
    "O consumo real depende do modelo do chuveiro, do clima e dos hábitos da família.",
    "A potência do chuveiro (5.500 W inverno / 3.500 W verão) é um valor comum, não medido.",
    "O aquecedor solar rende menos no inverno e em dias nublados.",
    "O estudo do aquecedor solar foi feito em Florianópolis, com clima diferente de SP.",
    "Bandeiras tarifárias, iluminação pública (COSIP) e reajustes futuros não foram incluídos.",
    "O payback não considera juros, inflação nem manutenção.",
    "Na Tarifa Social, consideramos que o consumo acima de 80 kWh é cobrado com a tarifa normal.",
]


def consumo_chuveiro_kwh(potencia_w, minutos, pessoas, banhos_por_dia=1):
    potencia_kw = potencia_w / 1000
    horas_por_banho = minutos / 60
    total_banhos = pessoas * banhos_por_dia * DIAS_NO_MES
    return potencia_kw * horas_por_banho * total_banhos


def custo_reais(consumo_kwh, tarifa=TARIFA_KWH):
    return consumo_kwh * tarifa


def co2_kg(consumo_kwh):
    return consumo_kwh * FATOR_CO2_KG_POR_KWH


def payback_meses(investimento, economia_mensal):
    if economia_mensal <= 0:
        return None
    return investimento / economia_mensal


def economia_cobrada_kwh(consumo_total, economia_kwh, tarifa_social):
    if not tarifa_social:
        return economia_kwh
    cobrado_antes = max(0, consumo_total - LIMITE_TARIFA_SOCIAL_KWH)
    cobrado_depois = max(0, consumo_total - economia_kwh - LIMITE_TARIFA_SOCIAL_KWH)
    return cobrado_antes - cobrado_depois


def comparar_alternativas(pessoas, minutos_banho=MINUTOS_BANHO_ATUAL, tarifa_social=False, consumo_total=None):
    consumo_atual = consumo_chuveiro_kwh(POTENCIA_INVERNO_W, minutos_banho, pessoas)
    minutos_consciente = min(minutos_banho, MINUTOS_BANHO_CONSCIENTE)
    consumo_consciente = consumo_chuveiro_kwh(POTENCIA_VERAO_W, minutos_consciente, pessoas)
    consumo_solar = consumo_atual * (1 - FRACAO_ECONOMIA_SOLAR)

    if consumo_total is None:
        consumo_total = consumo_atual

    investimento_solar = CUSTO_AQUECEDOR_SOLAR
    if pessoas > PESSOAS_AQUECEDOR_PEQUENO:
        investimento_solar = CUSTO_AQUECEDOR_GRANDE

    alternativas = [
        {"nome": "Situação atual", "consumo": consumo_atual, "investimento": 0},
        {"nome": "Alt. 1 - Uso consciente", "consumo": consumo_consciente, "investimento": 0},
        {"nome": "Alt. 2 - Aquecedor solar", "consumo": consumo_solar, "investimento": investimento_solar},
    ]

    for alternativa in alternativas:
        economia_kwh = max(0, consumo_atual - alternativa["consumo"])
        kwh_pago = economia_cobrada_kwh(consumo_total, economia_kwh, tarifa_social)
        economia_reais = custo_reais(kwh_pago)

        alternativa["custo_mes"] = custo_reais(alternativa["consumo"])
        alternativa["economia_kwh_mes"] = economia_kwh
        alternativa["economia_reais_mes"] = economia_reais
        alternativa["economia_reais_ano"] = economia_reais * MESES_NO_ANO
        alternativa["co2_evitado_ano"] = co2_kg(economia_kwh) * MESES_NO_ANO

        if alternativa["investimento"] > 0:
            alternativa["payback"] = payback_meses(alternativa["investimento"], economia_reais)
        else:
            alternativa["payback"] = None

    return alternativas


def analisar_historico(historico, pessoas, minutos_banho=MINUTOS_BANHO_ATUAL):
    total = sum(historico.values())
    media = total / len(historico)
    mes_menor = min(historico, key=historico.get)
    mes_maior = max(historico, key=historico.get)

    chuveiro = consumo_chuveiro_kwh(POTENCIA_INVERNO_W, minutos_banho, pessoas)
    percentual_chuveiro = chuveiro / media * 100

    return {
        "total": total,
        "media": media,
        "mes_menor": mes_menor,
        "mes_maior": mes_maior,
        "chuveiro": chuveiro,
        "percentual_chuveiro": percentual_chuveiro,
    }


def formatar_reais(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


def formatar_numero(valor, casas=1):
    return f"{valor:.{casas}f}".replace(".", ",")


def ler_inteiro(pergunta, minimo, maximo):
    while True:
        resposta = input(pergunta).strip()
        numeros = "".join(c for c in resposta if c.isdigit())
        if numeros != "" and minimo <= int(numeros) <= maximo:
            return int(numeros)
        print(f"Digite um número entre {minimo} e {maximo}.")


def ler_sim_nao(pergunta):
    while True:
        resposta = input(pergunta).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Responda com S ou N.")


def linha():
    print("-" * 60)


def calcular_meu_chuveiro():
    linha()
    print("Vamos calcular quanto o chuveiro pesa na sua conta.\n")
    pessoas = ler_inteiro("Quantas pessoas moram na casa? ", 1, 15)
    minutos = ler_inteiro("Em média, quantos minutos dura cada banho? ", 1, 60)
    tarifa_social = ler_sim_nao("Sua família recebe a Tarifa Social de energia? (S/N) ")

    consumo_total = None
    if tarifa_social:
        consumo_total = ler_inteiro("Quantos kWh veio na sua última conta? ", 1, 2000)

    alternativas = comparar_alternativas(pessoas, minutos, tarifa_social, consumo_total)
    atual, consciente, solar = alternativas

    linha()
    print(f"Seu chuveiro gasta cerca de {formatar_numero(atual['consumo'])} kWh por mês.")
    if tarifa_social:
        kwh_pago = economia_cobrada_kwh(consumo_total, atual["consumo"], True)
        print(f"Com a Tarifa Social, a parte do chuveiro que você paga é cerca de "
              f"{formatar_reais(custo_reais(kwh_pago))}.\n")
    else:
        print(f"Isso dá aproximadamente {formatar_reais(atual['custo_mes'])} na conta.\n")

    if consumo_total is not None and atual["consumo"] > consumo_total:
        print(f"Aviso: a estimativa do chuveiro passou do total da sua conta ({consumo_total} kWh).")
        print("Seu chuveiro deve ter potência menor ou os banhos são mais curtos.")
        print("Os valores abaixo podem estar acima do real.\n")

    if minutos > 15:
        vezes = minutos / BANHO_MEDIO_ESTUDO
        print(f"Seu banho de {minutos} min é cerca de {formatar_numero(vezes)} vezes a média de "
              f"{formatar_numero(BANHO_MEDIO_ESTUDO, 2)} min")
        print("encontrada em estudo com famílias de baixa renda.\n")

    kwh_por_minuto = consumo_chuveiro_kwh(POTENCIA_INVERNO_W, 1, pessoas)
    print(f"Cada minuto a menos no banho de todos economiza cerca de "
          f"{formatar_numero(kwh_por_minuto)} kWh")
    print(f"= {formatar_reais(custo_reais(kwh_por_minuto))} por mês (sem Tarifa Social).\n")

    print("Comparando as alternativas (por mês):\n")
    print(f"1) Uso consciente (banho de {MINUTOS_BANHO_CONSCIENTE} min + chave no modo verão)")
    print(f"   Economia: {formatar_numero(consciente['economia_kwh_mes'])} kWh = "
          f"{formatar_reais(consciente['economia_reais_mes'])}/mês "
          f"({formatar_reais(consciente['economia_reais_ano'])}/ano)")
    print("   Custo para começar: nenhum\n")

    print("2) Aquecedor solar de água (energia renovável)")
    print(f"   Economia: {formatar_numero(solar['economia_kwh_mes'])} kWh = "
          f"{formatar_reais(solar['economia_reais_mes'])}/mês "
          f"({formatar_reais(solar['economia_reais_ano'])}/ano)")
    print(f"   Investimento: cerca de {formatar_reais(solar['investimento'])} instalado")
    if pessoas > PESSOAS_AQUECEDOR_PEQUENO:
        print("   (para mais de 4 pessoas foi considerado um reservatório maior, de 300 L)")
    if solar["payback"] is not None:
        anos = solar["payback"] / 12
        print(f"   Se paga em cerca de {formatar_numero(anos)} anos")
    else:
        print("   Com a Tarifa Social, não há economia em reais para pagar o investimento.")
    if minutos > 15 or pessoas > PESSOAS_AQUECEDOR_PEQUENO:
        print("   Com muitos banhos ou banhos longos, a água quente do reservatório pode")
        print("   acabar e o chuveiro elétrico volta a ligar. A economia real pode ser menor.")
    print()

    if tarifa_social and consumo_total > LIMITE_TARIFA_SOCIAL_KWH:
        kwh_cobrado = consumo_total - LIMITE_TARIFA_SOCIAL_KWH
        print(f"Com a Tarifa Social, só os {kwh_cobrado} kWh acima de 80 são cobrados.")
        print("Por isso a economia em reais nunca passa do valor dessa parte cobrada.\n")

    linha()
    print("RECOMENDAÇÃO:")
    if minutos <= MINUTOS_BANHO_CONSCIENTE:
        print("Seus banhos já são curtos. Usar a chave no modo verão nos dias quentes")
        print("ainda ajuda a economizar.")
    elif minutos > 15:
        print("Comece reduzindo o banho aos poucos, um ou dois minutos por vez.")
        print("Não precisa chegar a 5 minutos de uma vez: cada minuto já conta.")
    elif consciente["economia_reais_mes"] >= solar["economia_reais_mes"]:
        print("Comece pelo uso consciente: ele economiza tanto ou mais que o aquecedor")
        print("solar e não custa nada.")
    else:
        print("Comece pelo uso consciente, que não custa nada. O aquecedor solar")
        print("economiza mais, mas exige investimento.")

    sobra_cobrada = 0
    if tarifa_social:
        sobra_cobrada = max(0, consumo_total - consciente["economia_kwh_mes"] - LIMITE_TARIFA_SOCIAL_KWH)

    if tarifa_social and consumo_total > LIMITE_TARIFA_SOCIAL_KWH and sobra_cobrada == 0:
        print("Só com o uso consciente sua conta já pode ficar dentro dos 80 kWh gratuitos.")
        print("Nesse caso, o aquecedor solar não traria economia extra em reais.")
    elif solar["payback"] is not None:
        print(f"O aquecedor solar leva cerca de {formatar_numero(solar['payback'] / 12)} anos para se pagar.")
        if solar["payback"] > 120:
            print("Como passa de 10 anos, no seu caso ele não compensa financeiramente.")
        else:
            print("Pode valer a pena se a casa tiver telhado com sol e a família puder investir.")

    if tarifa_social and consumo_total <= LIMITE_TARIFA_SOCIAL_KWH:
        print("\nComo seu consumo está dentro dos 80 kWh gratuitos da Tarifa Social,")
        print("economizar energia não reduz o valor da conta. Ainda assim, ajuda a")
        print("manter o consumo dentro do limite.")

    print("\nAtenção: são estimativas, não garantia de economia (veja a opção 4).")
    linha()


def dicas_uso_consciente():
    linha()
    print("DICAS PARA GASTAR MENOS COM O CHUVEIRO\n")
    print(f"- Tente banhos de até {MINUTOS_BANHO_CONSCIENTE} minutos. Cada minuto a menos economiza.")
    print("- Nos dias quentes, use a chave no modo VERÃO: ela gasta bem menos energia.")
    print("- Desligue o chuveiro enquanto se ensaboa.")
    print("- Evite banho entre 18h e 21h, quando a rede elétrica está mais carregada.")
    print("- Não mude a chave de posição com o chuveiro ligado: isso pode queimar a resistência.")
    print("\nO chuveiro elétrico responde, em média, por 24% do consumo de uma casa")
    print("no Brasil (Eletrobras/Procel).")
    linha()


def sobre_aquecedor_solar():
    linha()
    print("AQUECEDOR SOLAR DE ÁGUA\n")
    print("Ele usa placas no telhado para esquentar a água com a luz do sol e guarda")
    print("essa água quente em um reservatório (boiler). Assim, o chuveiro elétrico")
    print("é menos usado.\n")
    print(f"- Preço de um modelo de 150 a 200 litros, instalado: "
          f"{formatar_reais(CUSTO_SOLAR_MIN)} a {formatar_reais(CUSTO_SOLAR_MAX)}")
    print(f"- Economia estimada no chuveiro: cerca de {int(FRACAO_ECONOMIA_SOLAR * 100)}% "
          "(varia de 30% a 71% conforme o mês)")
    print("- Funciona melhor em casas com telhado ensolarado e sem sombra.")
    print("- Em dias nublados e no inverno, o chuveiro elétrico continua sendo usado.\n")
    print("Para saber se compensa na sua casa, use a opção 1 do menu.")
    linha()


def fontes_e_limitacoes():
    linha()
    print("DE ONDE VÊM OS NÚMEROS\n")
    for fonte in FONTES:
        print(f"- {fonte}")
    print("\nLIMITAÇÕES DAS ESTIMATIVAS\n")
    for limitacao in LIMITACOES:
        print(f"- {limitacao}")
    print("\nDetalhes completos em: dados/dados_energia.md")
    linha()


def analise_completa():
    alternativas = comparar_alternativas(pessoas=4)

    print("=" * 78)
    print(f"COMPARAÇÃO DE ALTERNATIVAS - 4 pessoas, banho de {MINUTOS_BANHO_ATUAL} min")
    print(f"Tarifa: {formatar_reais(TARIFA_KWH)}/kWh | Período: 1 mês (30 dias)")
    print("=" * 78)
    print(f"{'Alternativa':<26}{'kWh/mês':>9}{'Custo/mês':>14}{'Economia/ano':>15}{'CO2 evit./ano':>14}")
    print("-" * 78)

    for alt in alternativas:
        print(f"{alt['nome']:<26}"
              f"{formatar_numero(alt['consumo']):>9}"
              f"{formatar_reais(alt['custo_mes']):>14}"
              f"{formatar_reais(alt['economia_reais_ano']):>15}"
              f"{formatar_numero(alt['co2_evitado_ano']):>11} kg")

    print("-" * 78)
    for alt in alternativas:
        if alt["payback"] is not None:
            anos = alt["payback"] / 12
            print(f"Payback do aquecedor solar ({formatar_reais(alt['investimento'])}): "
                  f"{alt['payback']:.0f} meses (~{formatar_numero(anos)} anos)")

    resultado = analisar_historico(HISTORICO_CONSUMO, pessoas=2)

    print()
    print("=" * 78)
    print("ANÁLISE DO HISTÓRICO REAL - residência com 2 pessoas (Enel SP)")
    print("=" * 78)
    print(f"Consumo total em 12 meses: {resultado['total']} kWh")
    print(f"Média mensal: {formatar_numero(resultado['media'])} kWh "
          f"(custo médio: {formatar_reais(custo_reais(resultado['media']))})")
    print(f"Menor mês: {resultado['mes_menor']} ({HISTORICO_CONSUMO[resultado['mes_menor']]} kWh) | "
          f"Maior mês: {resultado['mes_maior']} ({HISTORICO_CONSUMO[resultado['mes_maior']]} kWh)")
    print(f"Chuveiro estimado: {formatar_numero(resultado['chuveiro'])} kWh/mês = "
          f"{formatar_numero(resultado['percentual_chuveiro'])}% do consumo médio")
    print("Média nacional do chuveiro (Procel): 24% do consumo residencial")
    print("=" * 78)


def menu():
    print("=" * 60)
    print("CITIZEN ASSIST AI - Energia em casa")
    print("Orientações para gastar menos com o chuveiro elétrico")
    print("=" * 60)

    while True:
        print("\nO que você quer saber?")
        print("1 - Calcular o gasto do meu chuveiro e ver alternativas")
        print("2 - Dicas de uso consciente")
        print("3 - Vale a pena um aquecedor solar?")
        print("4 - De onde vêm os números e limitações")
        print("5 - Ver a análise completa (tabela de comparação)")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            calcular_meu_chuveiro()
        elif opcao == "2":
            dicas_uso_consciente()
        elif opcao == "3":
            sobre_aquecedor_solar()
        elif opcao == "4":
            fontes_e_limitacoes()
        elif opcao == "5":
            analise_completa()
        elif opcao == "0":
            print("Até mais! Economizar energia também é cuidar do bolso e do planeta.")
            break
        else:
            print("Opção inválida. Digite um número de 0 a 5.")


if __name__ == "__main__":
    menu()
