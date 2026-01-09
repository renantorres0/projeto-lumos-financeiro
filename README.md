# 📊 Monitor de Fluxo de Caixa Inteligente - Lumos Serviços

Este projeto consiste em um Dashboard de Saúde Financeira desenvolvido para pequenas empresas (PME), utilizando **Python** e **Streamlit**. O objetivo é transformar transações brutas em inteligência de negócio, permitindo ao empresário prever buracos no caixa e simular investimentos.

## 🚀 Funcionalidades Principais

- **Visão Executiva (KPIs):** Saldo em caixa, contas a receber e a pagar em tempo real.
- **Análise de Sobrevivência:** Cálculo automático de *Burn Rate* (gasto mensal) e *Runway* (meses de fôlego financeiro).
- **Simulação What-If:** Módulo interativo para prever o impacto de novos investimentos no saldo futuro.
- **Monitor de Inadimplência:** Identificação visual de pagamentos pendentes e atrasados.
- **Personalização de Interface:** Alternância entre Modo Claro e Escuro para melhor legibilidade.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pandas:** Manipulação e tratamento de dados financeiros.
* **Streamlit:** Framework para criação da interface web interativa.
* **Plotly:** Gráficos dinâmicos e interativos.
* **Venv:** Gerenciamento de ambiente virtual.

## 📈 Como rodar o projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/renantorres0/projeto-lumos-financeiro.git](https://github.com/renantorres0/projeto-lumos-financeiro.git)
    ```
2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o dashboard:**
    ```bash
    streamlit run app.py
    ```

---
*Desenvolvido como parte do meu Portfólio de Data Analytics.*