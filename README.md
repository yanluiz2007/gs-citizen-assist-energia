# Citizen Assist AI — Energia em Casa

**Global Solution 2026.2 — Ciência da Computação (1CCPY) — FIAP**
**Disciplina: Soluções em Energias Renováveis e Sustentáveis**

## Integrantes

| Nome | RM |
|---|---|
| Yan Luiz Neves Lemos | 571717 |
| Matheus da Costa Gonçalves | 570756 |
| Guilherme Wadt de Oliveira | 569375 |

## Público e problema

**Público:** famílias de baixa renda da Grande São Paulo.

**Problema:** a conta de luz pesa no orçamento dessas famílias, e o **chuveiro elétrico** é um dos aparelhos que mais consomem energia em casa. Segundo a Eletrobras/Procel, ele responde, em média, por **24% do consumo residencial** no Brasil e está presente em 73,1% dos domicílios.

**Como o assistente ajuda:** o usuário informa quantas pessoas moram na casa, quanto dura o banho e se recebe a Tarifa Social. O Citizen Assist AI calcula o consumo e o custo do chuveiro e compara duas alternativas para a mesma necessidade (banho quente), no mesmo período (1 mês e 1 ano):

1. **Uso consciente:** banho mais curto + chave no modo verão (custo zero).
2. **Aquecedor solar de água** (fonte renovável): reduz o uso do chuveiro elétrico, mas exige investimento.

## Funcionalidades de energia

| Opção do menu | O que faz |
|---|---|
| 1 – Calcular o gasto do meu chuveiro | Calcula kWh e R$ por mês, compara as alternativas, mostra a economia por minuto, o payback e uma recomendação personalizada. Considera a Tarifa Social. |
| 2 – Dicas de uso consciente | Orientações práticas para gastar menos com o chuveiro. |
| 3 – Vale a pena um aquecedor solar? | Explica como funciona, quanto custa e quando compensa. |
| 4 – De onde vêm os números | Mostra as fontes e as limitações das estimativas. |
| 5 – Análise completa | Tabela de comparação (cenário de 4 pessoas) e análise do histórico real de 12 meses de uma residência. |

## Principais resultados (cenário base: 4 pessoas, banho de 8 min)

Tarifa real usada: **R$ 1,01883/kWh** (TUSD + TE com tributos, conta Enel SP de set/2026).

| Alternativa | kWh/mês | Custo/mês | Economia/ano | CO₂ evitado/ano | Investimento |
|---|---|---|---|---|---|
| Situação atual | 88,0 | R$ 89,66 | — | — | — |
| Uso consciente | 35,0 | R$ 35,66 | R$ 647,98 | 24,5 kg | R$ 0 |
| Aquecedor solar | 44,0 | R$ 44,83 | R$ 537,94 | 20,3 kg | R$ 3.300 (payback de ~6,1 anos) |

**Histórico real (residência com 2 pessoas):** média de 514,5 kWh/mês nos últimos 12 meses. O chuveiro estimado representa só 8,6% desse consumo, bem abaixo da média nacional de 24%. Isso mostra que, nessa casa, outros aparelhos pesam mais.

## Recomendações e justificativas

- **Começar pelo uso consciente.** No cenário base, ele economiza mais que o aquecedor solar e não custa nada. É a opção mais viável para famílias de baixa renda.
- **Aquecedor solar como segundo passo.** Compensa para famílias maiores, com telhado ensolarado e condições de investir. Em casas pequenas com banhos curtos, o payback pode passar de 10 anos e o assistente avisa que não compensa.
- **Tarifa Social muda o resultado.** Como os primeiros 80 kWh são gratuitos, a economia em reais é menor. Se o uso consciente já coloca a conta dentro da faixa gratuita, o assistente não recomenda o investimento no aquecedor solar.
- **Impacto ambiental.** A matriz elétrica brasileira tem baixa emissão (0,0385 kg CO₂/kWh, MCTI 2023). Por isso, o ganho em CO₂ é pequeno. O benefício principal é financeiro e a redução de demanda no horário de pico (18h–21h).

## Limitações

Os resultados são **estimativas**, não garantia de economia. A potência do chuveiro e o tempo de banho são premissas. O aquecedor solar rende menos no inverno e em dias nublados. Bandeiras tarifárias, COSIP e reajustes futuros não foram incluídos. O payback não considera juros, inflação nem manutenção. A lista completa está em [`dados/dados_energia.md`](dados/dados_energia.md).

## Como executar

Requisito: **Python 3** instalado. Não é necessária nenhuma biblioteca externa.

```
python assistente_energia.py
```

Escolha uma opção do menu digitando o número e pressione Enter. Para sair, digite `0`.

## Estrutura do repositório

```
├── README.md                  ← este arquivo
├── assistente_energia.py      ← código do assistente (cálculos + chatbot)
├── dados/
│   └── dados_energia.md       ← dados, origem, premissas, cálculos, limitações e referências
└── testes/
    └── testes_usuarios.md     ← registro dos testes e dos ajustes realizados
```

## Referências

1. Enel Distribuição São Paulo. Fatura de energia elétrica, ref. 09/2026, classe B1 residencial (dados pessoais omitidos).
2. InfoMoney. *Aneel aprova alta média de 10,18% para tarifas dos consumidores da Enel São Paulo*. 30/06/2026. https://www.infomoney.com.br/?p=3394051
3. Revista Brasileira de Energia Solar (RBENS). Artigo sobre aquecimento solar em habitações de baixa renda (cita Eletrobras/Procel – Pesquisa de Posse e Hábitos). Dez/2011. https://rbens.emnuvens.com.br/rbens/article/download/67/67/133
4. Cronoshare. *Quanto custa instalar um aquecedor solar?* Preços 2026. https://www.cronoshare.com.br/quanto-custa/instalar-aquecedor-solar-agua-termossifao
5. O Setor Elétrico. *Geração de energia elétrica tem a menor emissão de CO2 dos últimos onze anos*. 14/02/2024. https://www.osetoreletrico.com.br/?p=159478
6. SBT News. *Tarifa social de energia entra em vigor neste sábado (5)*. 04/07/2025. https://sbtnews.sbt.com.br/noticia/brasil/tarifa-social-de-energia-entra-em-vigor-neste-sabado-5-veja-quem-tem-direito-e-o-que-muda
