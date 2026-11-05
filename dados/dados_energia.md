# Dados de Energia — Citizen Assist AI

> Contribuição da disciplina **Soluções em Energias Renováveis e Sustentáveis**

## 1. Contexto

- **Público:** famílias de baixa renda da Grande São Paulo.
- **Necessidade energética:** reduzir o gasto com a conta de luz, com foco no **chuveiro elétrico**, um dos aparelhos que mais consomem energia em uma residência.
- **Como o assistente ajuda:** o usuário informa quantas pessoas moram na casa e quanto tempo dura o banho. O Citizen Assist AI calcula o consumo e o custo do chuveiro e compara alternativas de economia, incluindo uma fonte renovável (aquecedor solar de água).

## 2. Dados utilizados

Legenda: **REAL** = dado medido ou publicado por fonte verificável | **ESTIMADO** = premissa adotada pelo grupo, com justificativa.

| Dado | Valor | Unidade | Período | Tipo | Origem |
|---|---|---|---|---|---|
| Tarifa de energia (TUSD + TE, com tributos) | 1,01883 | R$/kWh | set/2026 | REAL | Conta de luz Enel SP, classe B1 residencial [1] |
| TUSD com tributos | 0,60975 | R$/kWh | set/2026 | REAL | Conta de luz Enel SP [1] |
| TE com tributos | 0,40908 | R$/kWh | set/2026 | REAL | Conta de luz Enel SP [1] |
| Reajuste Enel SP (residencial) | 9,02 | % | a partir de 04/07/2026 | REAL | InfoMoney [2] |
| Participação do chuveiro no consumo residencial | 24 | % | média Brasil | REAL | Eletrobras/Procel, citado em RBENS [3] |
| Domicílios com chuveiro elétrico | 73,1 | % | Brasil | REAL | Eletrobras/Procel, citado em RBENS [3] |
| Duração média do banho (famílias de baixa renda) | 5,15 | min | — | REAL | Naspolini et al., citado em RBENS [3] |
| Redução média de demanda com aquecedor solar | 48,95 | % | 2004 | REAL | Estudo com famílias de baixa renda, RBENS [3] |
| Custo do aquecedor solar 150–200 L instalado | 2.300 a 4.300 | R$ | 2026 | REAL (faixa de mercado) | Cronoshare [4] |
| Fator de emissão do SIN | 0,0385 | kg CO₂/kWh | 2023 | REAL | MCTI, citado em O Setor Elétrico [5] |
| Tarifa Social: gratuidade | até 80 | kWh/mês | desde 07/2025 | REAL | SBT News [6] |
| Potência do chuveiro, modo inverno | 5.500 | W | — | ESTIMADO | Valor comum em chuveiros 220 V vendidos no Brasil |
| Potência do chuveiro, modo verão | 3.500 | W | — | ESTIMADO | Valor comum de potência reduzida em chuveiros 220 V |
| Duração do banho (cenário atual) | 8 | min | — | ESTIMADO | Acima da média do estudo [3], representando um banho sem cuidado com o tempo |
| Duração do banho (uso consciente) | 5 | min | — | ESTIMADO | Arredondado a partir da média de 5,15 min [3] |
| Fração de economia do aquecedor solar | 50 | % | média anual | ESTIMADO | Arredondado a partir da redução média de 48,95% [3] |
| Investimento no aquecedor solar (até 4 pessoas) | 3.300 | R$ | 2026 | ESTIMADO | Ponto médio da faixa R$ 2.300 – 4.300 [4] |
| Investimento no aquecedor solar 300 L (mais de 4 pessoas) | 3.800 | R$ | 2026 | ESTIMADO | Fornecimento R$ 3.000 – 3.500 + mão de obra R$ 300 – 800 [4] |

## 3. Histórico real de consumo (residência com 2 pessoas, Enel SP)

Dados retirados da conta de luz de setembro/2026. Nenhum dado pessoal (nome, endereço, CPF ou número de instalação) foi incluído.

| Mês | Consumo (kWh) | Dias |
|---|---|---|
| out/25 | 520 | 32 |
| nov/25 | 493 | 30 |
| dez/25 | 485 | 29 |
| jan/26 | 536 | 32 |
| fev/26 | 488 | 30 |
| mar/26 | 481 | 29 |
| abr/26 | 560 | 32 |
| mai/26 | 492 | 30 |
| jun/26 | 435 | 29 |
| jul/26 | 573 | 33 |
| ago/26 | 502 | 29 |
| set/26 | 609 | 32 |
| **Total 12 meses** | **6.174** | |
| **Média mensal** | **514,5** | |

## 4. Premissas dos cálculos

1. Período de referência comum: **1 mês (30 dias)** e **1 ano (12 meses)**.
2. Cada pessoa toma **1 banho por dia**.
3. Energia (kWh) = Potência (kW) × Tempo de uso (h).
4. Custo (R$) = Energia (kWh) × Tarifa (R$/kWh).
5. Adicionais de bandeira tarifária **não** foram incluídos, porque variam de mês para mês.
6. COSIP (iluminação pública) e serviços de terceiros **não** foram incluídos, porque não dependem do consumo.
7. Payback simples = Investimento ÷ Economia mensal, sem considerar juros, inflação, reajustes ou manutenção.
8. CO₂ evitado = Energia economizada (kWh) × Fator de emissão do SIN.
9. Tarifa Social: os primeiros 80 kWh do mês são gratuitos. Consideramos que o consumo acima disso é cobrado com a tarifa normal (premissa simplificada). Por isso, a economia em reais só conta a parte que sai da faixa cobrada.
10. No uso consciente, o banho é limitado a 5 minutos. Se o usuário já toma banhos mais curtos, o tempo dele é mantido.
11. Para casas com mais de 4 pessoas, considera-se um aquecedor solar maior (300 L), com custo maior.
12. Banhos acima de 15 minutos ou casas com mais de 4 pessoas recebem um aviso de que a água quente do reservatório pode acabar, reduzindo a economia real do aquecedor solar.

## 5. Limitações

- Os resultados são **estimativas** e não garantem economia. O consumo real depende do modelo do chuveiro, da tensão da rede, do clima e dos hábitos da família.
- O desempenho do aquecedor solar varia com a estação do ano, a orientação do telhado e o sombreamento. No estudo usado como base, a redução mensal variou de **29,8% a 71,3%** [3].
- O estudo de referência foi realizado em Florianópolis, com clima diferente do de São Paulo.
- Famílias com **Tarifa Social** (gratuidade até 80 kWh/mês) podem ter uma economia em reais menor do que a calculada.
- A matriz elétrica brasileira tem baixa emissão de CO₂ por kWh. Por isso, o ganho ambiental em CO₂ é pequeno. O principal benefício é financeiro e a redução de demanda no horário de pico.

## 6. Referências

1. Enel Distribuição São Paulo. Fatura de energia elétrica, referência 09/2026, classe B1 residencial (dados pessoais omitidos).
2. InfoMoney. *Aneel aprova alta média de 10,18% para tarifas dos consumidores da Enel São Paulo*. 30/06/2026. https://www.infomoney.com.br/?p=3394051
3. Revista Brasileira de Energia Solar (RBENS). Artigo sobre aquecimento solar em habitações de baixa renda. Dez/2011. https://rbens.emnuvens.com.br/rbens/article/download/67/67/133
4. Cronoshare. *Quanto custa instalar um aquecedor solar?* Preços 2026. https://www.cronoshare.com.br/quanto-custa/instalar-aquecedor-solar-agua-termossifao
5. O Setor Elétrico. *Geração de energia elétrica tem a menor emissão de CO2 dos últimos onze anos*. 14/02/2024. https://www.osetoreletrico.com.br/?p=159478
6. SBT News. *Tarifa social de energia entra em vigor neste sábado (5)*. 04/07/2025. https://sbtnews.sbt.com.br/noticia/brasil/tarifa-social-de-energia-entra-em-vigor-neste-sabado-5-veja-quem-tem-direito-e-o-que-muda
