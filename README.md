# Quantum Invest

Aplicação interativa desenvolvida em **Streamlit** para análise quantitativa de portfólios de ações brasileiras, com foco na avaliação integrada de retorno, risco e exposição ao mercado.

O projeto implementa uma estrutura de análise baseada em séries temporais de retornos, permitindo a construção de carteiras customizadas e sua comparação direta com um benchmark de mercado (**BRAX11**). A aplicação combina modelagem financeira — incluindo métricas como Sharpe Ratio, Beta, Alpha, Max Drawdown e Value at Risk (VaR) — com visualizações interativas que facilitam a interpretação dos resultados.

Diferente de análises estáticas, o sistema permite ao usuário alterar dinamicamente a composição da carteira, os pesos dos ativos e o horizonte temporal, atualizando em tempo real todas as métricas e gráficos. Isso possibilita explorar, de forma prática, como decisões de alocação impactam o perfil risco-retorno do portfólio.

A aplicação também incorpora ferramentas de diagnóstico, como análise de volatilidade, regressão em relação ao mercado e decomposição de desempenho, oferecendo uma visão estruturada sobre a consistência e robustez da estratégia adotada.

Em síntese, o projeto busca transformar uma análise quantitativa de portfólio em um ambiente interativo, onde é possível investigar, validar e compreender o comportamento de carteiras sob diferentes configurações e cenários.

---

## Visão Geral

A aplicação permite:

* Construção de portfólios com pesos customizados
* Comparação direta com benchmark de mercado (**BRAX11**)
* Análise de performance acumulada
* Avaliação de risco com métricas clássicas e avançadas
* Visualização interativa de resultados
* Geração de relatórios interpretativos

---

## Arquitetura do Projeto

```bash
quantum-invest/
├── app.py                    # Aplicação principal (Streamlit)
├── cotacoes_ibrx11.xlsx      # Base de dados
├── requirements.txt          # Dependências
└── README.md                 # Documentação
```

### Pipeline de Execução

1. Carregamento dos dados (`pandas.read_excel`)
2. Seleção de ativos pelo usuário
3. Definição de pesos
4. Cálculo de retornos da carteira
5. Comparação com benchmark (BRAX11)
6. Cálculo de métricas de risco e retorno
7. Renderização via Streamlit + Plotly

---

## Modelagem Financeira

### 1. Retorno da Carteira

[
R_{p,t} = \sum_{i=1}^{N} w_i \cdot R_{i,t}
]

Onde:

* ( w_i ): peso do ativo ( i )
* ( R_{i,t} ): retorno do ativo ( i ) no tempo ( t )

---

### 2. Retorno Acumulado

[
R_{acumulado} = \prod_{t=1}^{T} (1 + R_{p,t}) - 1
]

---

### 3. Volatilidade

[
\sigma_p = \sqrt{Var(R_p)}
]

---

### 4. Sharpe Ratio

[
Sharpe = \frac{E[R_p - R_f]}{\sigma_p}
]

(assumindo ( R_f \approx 0 ) no contexto atual)

---

### 5. Beta (CAPM)

Estimado via regressão linear:

[
R_p = \alpha + \beta R_m + \epsilon
]

Onde:

* ( R_m ): retorno do benchmark (BRAX11)
* ( \beta ): sensibilidade ao mercado

---

### 6. Alpha

[
\alpha = R_p - \beta R_m
]

---

### 7. Max Drawdown

[
MDD = \max \left( \frac{Peak - Trough}{Peak} \right)
]

---

### 8. Value at Risk (VaR)

Estimado empiricamente a partir da distribuição dos retornos:

[
VaR_{\alpha} = \text{quantil inferior} (R_p)
]

---

## Funcionalidades

### 🔹 Construção de Carteira

* Seleção dinâmica de ativos
* Ajuste manual de pesos
* Opção de pesos iguais

### Análise de Performance

* Retorno acumulado
* Comparação com benchmark
* Evolução temporal

### Análise de Risco

* Volatilidade
* Sharpe Ratio
* Beta e Alpha
* Max Drawdown
* VaR

### Visualizações

* Curva de performance
* Heatmap de retornos mensais
* Volatilidade móvel
* Regressão carteira vs mercado
* Composição da carteira

### Relatório Executivo

* Interpretação automatizada
* Perfil de risco
* Diagnóstico da carteira

---

## Base de Dados

Arquivo:

```bash
cotacoes_ibrx11.xlsx
```

### Estrutura esperada:

#### `Selecao_Carteira`

* Lista de ativos disponíveis

#### `Cotacoes`

* Séries de preços históricos

#### `Retorno`

* Retornos calculados dos ativos

---

## Como Utilizar

1. Defina o capital inicial
2. Selecione os ativos da carteira
3. Ajuste os pesos
4. Escolha o período de análise
5. Explore as abas:

* Performance & Heatmap
* Risco Profundo
* Alocação Ativa
* Relatório Executivo

---

## Premissas e Limitações

* Não considera custos de transação
* Não considera impostos
* Assume rebalanceamento implícito contínuo
* Dependência da qualidade dos dados da planilha

---

## Possíveis Extensões

* Otimização de portfólio (Markowitz)
* Backtesting com rebalanceamento periódico
* Stress testing e cenários macroeconômicos

---

## Licença

Projeto de caráter acadêmico e experimental.
