import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Lumos Financeiro", layout="wide")

# 2. Função de Carga de Dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("financeiro_lumos.csv")
    df['Data'] = pd.to_datetime(df['Data'])
    df['Mes_Ano'] = df['Data'].dt.to_period('M').astype(str)
    return df

df = carregar_dados()
hoje = datetime.now()

# 3. Sidebar com Botão de Tema e Filtros
with st.sidebar:
    st.header("🎨 Personalização")
    tema = st.toggle("Modo Escuro", value=False) # Botão de alternar tema
    
    st.header("📅 Filtros")
    meses = sorted(df['Mes_Ano'].unique())
    mes_selecionado = st.multiselect("Selecione os Meses:", meses, default=meses)
    
    st.header("💰 Simulador What-If")
    investimento = st.number_input("Valor do Investimento (R$):", min_value=0.0, step=1000.0)
    data_invest = st.date_input("Data do Investimento:", hoje)

# Definindo cores com base no tema selecionado
if tema:
    bg_color = "#0E1117"
    txt_color = "white"
    chart_template = "plotly_dark"
else:
    bg_color = "white"
    txt_color = "#262730"
    chart_template = "plotly_white"

# Aplicando Filtro
df_filtrado = df[df['Mes_Ano'].isin(mes_selecionado)]

# 4. Título e KPIs
st.title("📊 Dashboard de Saúde Financeira - Lumos Serviços")

entradas_real = df_filtrado[(df_filtrado['Tipo'] == 'Entrada') & (df_filtrado['Status'] == 'Realizado')]['Valor'].sum()
saidas_real = df_filtrado[(df_filtrado['Tipo'] == 'Saída') & (df_filtrado['Status'] == 'Realizado')]['Valor'].sum()
saldo_atual = entradas_real - saidas_real

col1, col2, col3, col4 = st.columns(4)
col1.metric("Saldo em Caixa", f"R$ {saldo_atual:,.2f}")
col2.metric("A Receber", f"R$ {df_filtrado[(df_filtrado['Tipo'] == 'Entrada') & (df_filtrado['Status'] != 'Realizado')]['Valor'].sum():,.2f}")
col3.metric("A Pagar", f"R$ -{df_filtrado[(df_filtrado['Tipo'] == 'Saída') & (df_filtrado['Status'] != 'Realizado')]['Valor'].sum():,.2f}")

# Cálculo de Burn Rate e Runway
media_gastos = df_filtrado[df_filtrado['Tipo'] == 'Saída']['Valor'].sum() / len(mes_selecionado) if mes_selecionado else 1
runway = saldo_atual / media_gastos if media_gastos > 0 else 0
col4.metric("Runway (Meses)", f"{runway:.1f}", help="Quantos meses o caixa atual suporta sem novas vendas")

st.markdown("---")

# 5. Gráficos Principais
col_esq, col_dir = st.columns(2)

with col_esq:
    df_mensal = df_filtrado.groupby(['Mes_Ano', 'Tipo'])['Valor'].sum().reset_index()
    fig_bar = px.bar(df_mensal, x='Mes_Ano', y='Valor', color='Tipo', barmode='group',
                     title="Fluxo Mensal", color_discrete_map={'Entrada': '#2ECC71', 'Saída': '#E74C3C'},
                     template=chart_template)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_dir:
    df_sorted = df_filtrado.sort_values('Data').copy()
    df_sorted['Valor_Sinal'] = df_sorted.apply(lambda x: x['Valor'] if x['Tipo'] == 'Entrada' else -x['Valor'], axis=1)
    df_sorted['Saldo_Acumulado'] = df_sorted['Valor_Sinal'].cumsum()
    
    # Simulação
    data_invest_dt = pd.to_datetime(data_invest)
    df_sorted['Saldo_Simulado'] = df_sorted.apply(
        lambda x: x['Saldo_Acumulado'] - investimento if x['Data'] >= data_invest_dt else x['Saldo_Acumulado'], axis=1
    )
    
    fig_line = px.line(df_sorted, x='Data', y=['Saldo_Acumulado', 'Saldo_Simulado'],
                       title="Projeção de Caixa", template=chart_template,
                       color_discrete_map={'Saldo_Acumulado': '#2980B9', 'Saldo_Simulado': '#E67E22'})
    st.plotly_chart(fig_line, use_container_width=True)

# 6. Camada de Profundidade (Rosca e Tabela)
st.markdown("---")
c1, c2 = st.columns([1, 2])

with c1:
    st.subheader("Composição de Custos")
    df_rosca = df_filtrado[df_filtrado['Tipo'] == 'Saída'].groupby('Categoria')['Valor'].sum().reset_index()
    fig_pie = px.pie(df_rosca, values='Valor', names='Categoria', hole=.5, template=chart_template)
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("⚠️ Entradas Pendentes / Inadimplência")
    df_pendente = df_filtrado[(df_filtrado['Tipo'] == 'Entrada') & (df_filtrado['Status'] == 'Pendente')].copy()
    if not df_pendente.empty:
        st.dataframe(df_pendente[['Data', 'Descrição', 'Valor', 'Forma_Pagamento']].style.format({'Valor': 'R$ {:,.2f}'}), 
                     use_container_width=True, hide_index=True)
    else:
        st.success("Nenhuma pendência encontrada!")