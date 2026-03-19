import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Quantum Asset Terminal v3.0", layout="wide", page_icon="💎")

# --- DESIGN SYSTEM (CSS PREMIUM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #05070a; color: #e1e1e1; }
    .main { background: #05070a; }
    
    /* CORREÇÃO PARA O ZOOM 100% / LARGURA EXCESSIVA */
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
        margin: auto;
    }

    /* Metric Cards Glassmorphism */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar Modernization */
    [data-testid="stSidebar"] { background-color: #0a0c10; border-right: 1px solid rgba(0, 209, 178, 0.2); }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #00d1b2 0%, #0097a7 100%);
        color: white; font-weight: 800; height: 50px; border: none;
        letter-spacing: 1px; transition: 0.4s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px rgba(0, 209, 178, 0.5); }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: transparent; border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05); color: #888; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { 
        background: rgba(0, 209, 178, 0.1) !important; 
        border: 1px solid #00d1b2 !important; color: #00d1b2 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE CÁLCULO ---
@st.cache_data
def load_data():
    file_path = 'cotacoes_ibrx11.xlsx'
    try:
        sel = pd.read_excel(file_path, sheet_name='Selecao_Carteira')
        cot = pd.read_excel(file_path, sheet_name='Cotacoes')
        ret = pd.read_excel(file_path, sheet_name='Retorno')
        cot['Data'], ret['Data'] = pd.to_datetime(cot['Data']), pd.to_datetime(ret['Data'])
        return sel, cot, ret
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None, None

def generate_monthly_heatmap(df_ret):
    df_ret['Year'] = df_ret['Data'].dt.year
    df_ret['Month'] = df_ret['Data'].dt.month
    monthly = df_ret.groupby(['Year', 'Month'])['Portfolio'].apply(lambda x: (1 + x).prod() - 1).unstack()
    monthly.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    return monthly

# --- EXECUÇÃO ---
sel, cot, ret = load_data()

if ret is not None:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=70)
        st.title("Quantum v3.0")
        cap_inicial = st.number_input("Capital Inicial (R$)", value=1000, step=1000)

        rf_annual = st.number_input(
            "Taxa Livre de Risco (% a.a.)",
            min_value=0.0,
            max_value=50.0,
            value=10.0,
            step=0.5
        ) / 100
        
        st.divider()
        st.subheader("🛠️ Seletor de Ativos")
        tickers_disp = [c for c in cot.columns if c not in ['Data', 'BRAX11']]
        ativos_user = st.multiselect("Escolha seus Ativos:", tickers_disp, default=tickers_disp[:6])
        
        pesos_user = {}
        if ativos_user:
            if st.button("⚖️ Peso Igualitário"):
                for a in ativos_user:
                    st.session_state[f"w_{a}"] = round(100/len(ativos_user), 2)
            
            for a in ativos_user:
                pesos_user[a] = st.number_input(f"{a} (%)", 0.0, 100.0, key=f"w_{a}")
            
            total_w = sum(pesos_user.values())
            if total_w != 100:
                st.warning(f"Soma: {total_w:.1f}%")

        st.divider()
        start_date = st.date_input("Início", ret['Data'].min())
        end_date = st.date_input("Fim", ret['Data'].max())

    # --- PROCESSAMENTO QUANT ---
    mask = (ret['Data'].dt.date >= start_date) & (ret['Data'].dt.date <= end_date)
    df_f = ret.loc[mask].copy()

    rf_daily = (1 + rf_annual)**(1/252) - 1

    w_series = pd.Series(pesos_user) / 100
    df_f['Portfolio'] = df_f[ativos_user].mul(w_series).sum(axis=1)

    df_calc = df_f.dropna(subset=['Portfolio', 'BRAX11'])

    if len(df_calc) > 5:
        acum_port = (1 + df_calc['Portfolio']).cumprod()
        acum_idx = (1 + df_calc['BRAX11']).cumprod()
        
        vol_anual = df_calc['Portfolio'].std() * np.sqrt(252)

        # 🔥 Ajuste Sharpe (com risk-free)
        sharpe = ((df_calc['Portfolio'] - rf_daily).mean() * 252) / vol_anual if vol_anual > 0 else 0
        
        cov_p_idx = df_calc['Portfolio'].cov(df_calc['BRAX11'])
        var_idx = df_calc['BRAX11'].var()
        beta = cov_p_idx / var_idx if var_idx != 0 else 0
        
        # 🔥 Ajuste Alpha (CAPM com risk-free)
        alpha = (((df_calc['Portfolio'] - rf_daily).mean()) - beta * ((df_calc['BRAX11'] - rf_daily).mean())) * 252

        max_dd = (acum_port / acum_port.cummax() - 1).min()
        var_95 = np.percentile(df_calc['Portfolio'], 5)
        
        # --- UI PRINCIPAL ---
        st.title("🏦 Quantum Intelligence Terminal")
        st.markdown(f"Análise Estratégica: **{len(ativos_user)} Ativos** | Período: **{start_date} a {end_date}**")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Retorno Final", f"R$ {cap_inicial * acum_port.iloc[-1]:,.2f}", f"{(acum_port.iloc[-1]-1):.2%}")
        c2.metric("Eficiência (Sharpe)", f"{sharpe:.2f}")
        c3.metric("Beta do Portfólio", f"{beta:.2f}", help="Indica a sensibilidade ao mercado")
        c4.metric("Valor em Risco (VaR)", f"{var_95:.2%}", help="Perda máxima provável em 1 dia")

        st.divider()

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance & Heatmap", "🛡️ Risco Profundo", "🧩 Alocação Ativa", "📄 Relatório Executivo"])

        with tab1:
            st.subheader("Evolução do Capital")
            fig_evol = go.Figure()
            fig_evol.add_trace(go.Scatter(x=df_calc['Data'], y=acum_port*cap_inicial, name="Sua Carteira", line=dict(color='#00d1b2', width=4)))
            fig_evol.add_trace(go.Scatter(x=df_calc['Data'], y=acum_idx*cap_inicial, name="Índice BRAX11", line=dict(color='white', dash='dot'), opacity=0.4))
            fig_evol.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=20,b=0))
            st.plotly_chart(fig_evol, use_container_width=True)
            
            st.subheader("Calendário de Retornos Mensais (%)")
            heatmap_data = generate_monthly_heatmap(df_calc.copy())
            st.dataframe(heatmap_data.style.background_gradient(cmap='RdYlGn', axis=None).format("{:.2%}"), use_container_width=True)

        with tab2:
            col_dd, col_vol = st.columns(2)
            with col_dd:
                st.subheader("Drawdown Histórico")
                drawdown = (acum_port / acum_port.cummax() - 1)
                fig_dd = px.area(x=df_calc['Data'], y=drawdown, color_discrete_sequence=['#ff4b4b'])
                fig_dd.update_layout(template="plotly_dark", yaxis_tickformat='.1%')
                st.plotly_chart(fig_dd, use_container_width=True)
            with col_vol:
                st.subheader("Volatilidade Móvel (21 dias)")
                rolling_vol = df_calc['Portfolio'].rolling(21).std() * np.sqrt(252)
                fig_vol = px.line(x=df_calc['Data'], y=rolling_vol, color_discrete_sequence=['#ffeb3b'])
                fig_vol.update_layout(template="plotly_dark", yaxis_tickformat='.1%')
                st.plotly_chart(fig_vol, use_container_width=True)

        with tab3:
            col_pie, col_beta = st.columns(2)
            with col_pie:
                st.subheader("Composição do Portfólio")
                fig_p = px.pie(values=list(pesos_user.values()), names=list(pesos_user.keys()), hole=0.6, color_discrete_sequence=px.colors.qualitative.Prism)
                fig_p.update_layout(template="plotly_dark")
                st.plotly_chart(fig_p, use_container_width=True)
            with col_beta:
                st.subheader("Regressão: Carteira vs Mercado")
                fig_reg = px.scatter(df_calc, x="BRAX11", y="Portfolio", trendline="ols", trendline_color_override="#00d1b2")
                fig_reg.update_layout(template="plotly_dark")
                st.plotly_chart(fig_reg, use_container_width=True)

        with tab4:
            st.header("📝 Executive Intelligence Report")
            perfil = "Agressivo (High Beta)" if beta > 1.15 else "Defensivo (Low Beta)" if beta < 0.85 else "Neutro"
            alerta = "⚠️ Risco de Concentração" if any(p > 40 for p in pesos_user.values()) else "✅ Bem Diversificada"
            st.markdown(f"""
            ### Análise de Gestão de Ativos
            - **Resumo do Perfil:** Sua carteira possui um perfil **{perfil}**. O Beta de **{beta:.2f}** indica que {'você amplifica' if beta > 1 else 'você amortece'} os movimentos do mercado.
            - **Qualidade do Retorno:** O Alpha anualizado de **{alpha:.2%}** mostra que suas escolhas {'geraram valor real' if alpha > 0 else 'ficaram abaixo do esperado'} frente ao risco tomado.
            - **Eficiência Operacional:** Com um Sharpe de **{sharpe:.2f}**, para cada unidade de risco, você está obtendo um prêmio satisfatório.
            - **Suporte de Queda:** O Max Drawdown de **{max_dd:.2%}.** **Status da Carteira:** {alerta}
            """)
    else:
        st.warning("⚠️ Selecione um período maior ou ajuste os filtros para ver as estatísticas.")
else:
    st.error("Planilha 'cotacoes_ibrx11.xlsx' não encontrada.")