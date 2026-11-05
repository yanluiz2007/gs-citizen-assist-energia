# Registro de Testes — Citizen Assist AI (Energia)

Objetivo dos testes: verificar se as orientações do assistente são **compreensíveis** e **úteis**, e se os resultados são **coerentes** com a análise de energia.

Nenhum dado pessoal dos participantes foi registrado.

| Teste | Tipo | Quem executou |
|---|---|---|
| 1 | Teste de uso | Integrante do grupo, usando o assistente como um morador comum |
| 2 | Teste de cenário (simulado) | Grupo |
| 3 | Teste de cenário (simulado) | Grupo |

---

## Teste 1 — Família pequena com Tarifa Social

**Situação testada:** 2 pessoas, banho de 10 minutos, com Tarifa Social, conta de 50 kWh.

**O que foi observado:**

1. O usuário digitou `10 min` e o assistente recusou, pedindo só números. Um usuário comum escreveria assim.
2. O assistente estimou o chuveiro em 55 kWh, mais que o total da conta (50 kWh), e não avisou sobre a incoerência.
3. O assistente disse "R$ 56,04 na conta", mas com a Tarifa Social o consumo até 80 kWh é gratuito. A frase confundia.

**Ajustes realizados:**

1. A leitura de números passou a aceitar texto junto (`10 min`, `12 minutos`).
2. Foi incluído um aviso quando a estimativa do chuveiro passa do total da conta.
3. Com Tarifa Social, o assistente passou a mostrar apenas o valor efetivamente pago pela parte do chuveiro.

---

## Teste 2 — Família grande com banho longo

**Situação testada:** 5 pessoas, banho de 25 minutos, sem Tarifa Social.

**Resultado obtido:** chuveiro com 343,8 kWh/mês (R$ 350,22). Uso consciente economizaria R$ 305,65/mês. O aquecedor solar se pagaria em 1,6 ano.

**O que foi observado:**

1. O payback de 1,6 ano para o aquecedor solar era otimista demais. Um reservatório de 200 L atende cerca de 4 pessoas com banho normal. Com 5 pessoas e banhos longos, a água quente acaba e o chuveiro elétrico volta a ligar.
2. A recomendação de passar de 25 para 5 minutos de uma vez não era realista.
3. O assistente não mostrava que 25 minutos está muito acima da média.

**Ajustes realizados:**

1. Para mais de 4 pessoas, o cálculo passou a usar um aquecedor de 300 L (R$ 3.800), e o payback foi para 1,8 ano. Também foi incluído um aviso de que a economia real pode ser menor com muitos banhos ou banhos longos.
2. O assistente passou a mostrar **quanto cada minuto a menos economiza** (neste caso, R$ 14,01/mês) e a recomendar uma redução gradual.
3. Para banhos acima de 15 minutos, o assistente compara o tempo informado com a média de 5,15 minutos do estudo de referência.

---

## Teste 3 — Família com Tarifa Social e consumo acima de 80 kWh

**Situação testada:** 3 pessoas, banho de `12 minutos` (escrito por extenso), com Tarifa Social, conta de 120 kWh.

**Resultado obtido:** chuveiro com 99 kWh/mês. As duas alternativas mostraram a **mesma economia, R$ 40,75/mês**, e o aquecedor solar aparecia com payback de 6,7 anos.

**O que foi observado:**

1. O usuário não entende por que alternativas com economias diferentes em kWh (72,8 e 49,5) dão o mesmo valor em reais. Isso acontece porque, com a Tarifa Social, só os 40 kWh acima de 80 são cobrados.
2. Se o uso consciente já leva a conta para dentro da faixa gratuita, o aquecedor solar não traz economia extra. Mesmo assim, o assistente mostrava um payback, o que podia induzir a um investimento desnecessário.

**Ajustes realizados:**

1. O assistente passou a explicar que só a parte acima de 80 kWh é cobrada e que a economia em reais é limitada a esse valor.
2. Quando o uso consciente já zera a parte cobrada, o assistente informa que o aquecedor solar não traria economia extra em reais e deixa de sugerir o investimento.

---

## Resumo dos ajustes

| # | Problema encontrado | Ajuste | Teste |
|---|---|---|---|
| 1 | Entrada "10 min" recusada | Aceitar número junto com texto | 1 |
| 2 | Chuveiro maior que a conta inteira | Aviso de incoerência | 1 |
| 3 | Valor da conta errado com Tarifa Social | Mostrar só o valor pago | 1 |
| 4 | Aquecedor solar subdimensionado para 5 pessoas | Aquecedor de 300 L + aviso | 2 |
| 5 | Meta de banho irreal | Economia por minuto + redução gradual | 2 |
| 6 | Banho longo sem referência | Comparação com a média do estudo | 2 |
| 7 | Mesma economia em R$ sem explicação | Explicação da faixa cobrada | 3 |
| 8 | Payback sugerido sem economia extra | Não recomendar o investimento nesse caso | 3 |
