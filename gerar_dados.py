import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Configurações Iniciais
np.random.seed(42) # Para reproduzibilidade
hoje = datetime.now().date()
inicio_ano = hoje.replace(month=1, day=1) - relativedelta(months=12) # Começa 1 ano atrás
fim_projecao = hoje + timedelta(days=60) # Projeta 60 dias no futuro

# Listas de Categorias e Entidades para dar realismo
clientes = ['TechSolutions', 'Varejo Bom Preço', 'Consultório Dra. Ana', 'StartUp X', 'Padaria Central', 'Cliente Avulso']
fornecedores = ['Google Ads', 'AWS Services', 'Imobiliária Predial', 'Dell Computadores', 'Governo (Impostos)', 'Limpeza Ltda']

categorias_receita = ['Consultoria Mensal', 'Implementação de Projeto', 'Manutenção Técnica']
categorias_despesa = ['Folha de Pagamento', 'Marketing', 'Aluguel', 'Software/SaaS', 'Impostos', 'Equipamentos', 'Serviços Terceiros']

dados = []

# Função auxiliar para decidir status
def definir_status(data_transacao, tipo):
    if data_transacao > hoje:
        return 'Previsto'
    else:
        # 5% de chance de inadimplência ou atraso no passado
        return np.random.choice(['Realizado', 'Pendente'], p=[0.95, 0.05])

current_date = inicio_ano

# Loop gerando dados dia a dia até a data final de projeção
while current_date <= fim_projecao:
    
    # --- 1. GERAÇÃO DE DESPESAS FIXAS (Ocorrem em dias específicos) ---
    
    # Dia 05: Pagamento de Salários
    if current_date.day == 5:
        dados.append({
            'Data': current_date,
            'Tipo': 'Saída',
            'Categoria': 'Folha de Pagamento',
            'Descrição': 'Salários Equipe',
            'Valor': round(np.random.normal(18000, 500), 2), # Média 18k
            'Forma_Pagamento': 'Transferência',
            'Status': 'Previsto' if current_date > hoje else 'Realizado'
        })
    
    # Dia 10: Aluguel
    if current_date.day == 10:
        dados.append({
            'Data': current_date,
            'Tipo': 'Saída',
            'Categoria': 'Aluguel',
            'Descrição': 'Aluguel Escritório',
            'Valor': 3500.00,
            'Forma_Pagamento': 'Boleto',
            'Status': 'Previsto' if current_date > hoje else 'Realizado'
        })

    # Dia 20: Impostos (Simples Nacional)
    if current_date.day == 20:
        dados.append({
            'Data': current_date,
            'Tipo': 'Saída',
            'Categoria': 'Impostos',
            'Descrição': 'DAS Simples Nacional',
            'Valor': round(np.random.uniform(3000, 5000), 2),
            'Forma_Pagamento': 'Boleto',
            'Status': 'Previsto' if current_date > hoje else 'Realizado'
        })

    # --- 2. GERAÇÃO DE TRANSAÇÕES VARIÁVEIS (Aleatórias) ---
    
    # Receitas (Entradas) - Ocorrem ~15 vezes ao mês
    if np.random.random() < 0.5: # 50% de chance de ter venda no dia
        valor_venda = round(np.random.exponential(3000) + 1000, 2) # Vendas entre 1k e 10k
        cliente = np.random.choice(clientes)
        cat_rec = np.random.choice(categorias_receita)
        
        dados.append({
            'Data': current_date,
            'Tipo': 'Entrada',
            'Categoria': cat_rec,
            'Descrição': f'Serviço - {cliente}',
            'Valor': valor_venda,
            'Forma_Pagamento': np.random.choice(['Pix', 'Boleto', 'Cartão Crédito']),
            'Status': definir_status(current_date, 'Entrada')
        })

    # Despesas Variáveis (Saídas) - Marketing, Software, etc
    if np.random.random() < 0.3: # 30% de chance de despesa extra
        valor_desp = round(np.random.uniform(100, 1500), 2)
        cat_desp = np.random.choice(['Marketing', 'Software/SaaS', 'Serviços Terceiros'])
        forn = np.random.choice(fornecedores)
        
        dados.append({
            'Data': current_date,
            'Tipo': 'Saída',
            'Categoria': cat_desp,
            'Descrição': f'Pgto - {forn}',
            'Valor': valor_desp,
            'Forma_Pagamento': 'Cartão Crédito',
            'Status': definir_status(current_date, 'Saída')
        })

    current_date += timedelta(days=1)

# Criando o DataFrame
df = pd.DataFrame(dados)

# Ordenando por data
df = df.sort_values(by='Data')

# Salvando em CSV para simular a base de dados
df.to_csv('financeiro_lumos.csv', index=False)

print(f"Base de dados gerada com sucesso! {len(df)} transações criadas.")
print(df.head())