import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from modules import (
    apply_custom_css, 
    load_excel_data, 
    calculate_metrics, 
    render_performance_chart, 
    render_risk_charts, 
    render_allocation_chart, 
    render_heatmap,
    render_dividend_analysis,
    render_market_intelligence  # Novo módulo de notícias
)

st.set_page_config(page_title="Quantum Asset Terminal v3.1", layout="wide", page_icon="💎")
apply_custom_css()

sel, cot, ret = load_excel_data()

if ret is not None:
    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135706.png" width="70" style="margin-bottom: -15px;">
                <h2 style="text-align: center; color: #00d1b2; font-family: 'Plus Jakarta Sans', sans-serif;">QUANTUM</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption("Terminal de Inteligência Quantitativa")
        st.divider()

        cap_inicial = st.number_input("Capital Inicial (R$)", value=1000, step=1000)
        rf_annual = st.number_input("Taxa Risk-Free (% a.a.)", value=10.5, step=0.5) / 100
        
        st.subheader("🛠️ Forja de Portfólio")
        tickers = [c for c in cot.columns if c not in ['Data', 'BRAX11']]
        ativos_user = st.multiselect("Selecione seus Ativos:", tickers, default=tickers[:5])
        
        if st.button("⚖️ Distribuir Pesos por Igual"):
            if ativos_user:
                peso_eq = round(100.0 / len(ativos_user), 2)
                for a in ativos_user:
                    st.session_state[f"input_{a}"] = peso_eq
                st.rerun()

        pesos = {}
        for a in ativos_user:
            if f"input_{a}" not in st.session_state:
                st.session_state[f"input_{a}"] = 0.0
            pesos[a] = st.number_input(f"{a} (%)", 0.0, 100.0, key=f"input_{a}")
        
        st.divider()
        start_date = st.date_input("Início", ret['Data'].min())
        end_date = st.date_input("Fim", ret['Data'].max())

    mask = (ret['Data'].dt.date >= start_date) & (ret['Data'].dt.date <= end_date)
    df_f = ret.loc[mask].copy()
    total_w = sum(pesos.values())
    
    if len(ativos_user) > 0 and abs(total_w - 100) < 0.1:
        res = calculate_metrics(df_f, pesos, (1 + rf_annual)**(1/252) - 1)
        
        st.title("🏦 Quantum Intelligence Terminal")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Patrimônio Final", f"R$ {cap_inicial * res['acum_port'].iloc[-1]:,.2f}", f"{(res['acum_port'].iloc[-1]-1):.2%}")
        c2.metric("Sharpe Ratio", f"{res['sharpe']:.2f}")
        c3.metric("Fator Beta", f"{res['beta']:.2f}")
        c4.metric("VaR Diário (95%)", f"{res['var_95']:.2%}")

        st.divider()
        
        t1, t2, t3, t4, t5, t6 = st.tabs([
            "📊 Performance", "🛡️ Risco Profundo", "🧩 Alocação", 
            "📝 Relatório", "💰 Dividendos", "🌐 Intelligence"
        ])
        
        with t1:
            render_performance_chart(res['df_calc'], cap_inicial, res['acum_port'], res['acum_idx'])
            render_heatmap(res['df_calc'].copy())
        with t2:
            render_risk_charts(res['df_calc'], res['acum_port'])
        with t3:
            render_allocation_chart(pesos)
        with t4:
            st.header("📝 Executive Intelligence Report")
            perfil = "Agressivo" if res['beta'] > 1.15 else "Defensivo" if res['beta'] < 0.85 else "Moderado"
            st.markdown(f"""
            ### Diagnóstico Estratégico
            - **Perfil:** Esta carteira foi forjada com um viés **{perfil}**.
            - **Eficiência:** O Sharpe de **{res['sharpe']:.2f}** indica a qualidade do retorno.
            - **Alpha Anualizado:** Suas decisões geraram **{res['alpha']:.2%}** de Alpha.
            - **Resiliência:** O Max Drawdown histórico foi de **{res['max_dd']:.2%}**.
            """)
        with t5:
            render_dividend_analysis(ativos_user)
        with t6:
            render_market_intelligence(ativos_user)
            
    else:
        st.warning(f"Soma dos pesos: **{total_w:.2f}%**. Ajuste para 100% para liberar o terminal.")
else:
    st.error("Planilha 'cotacoes_ibrx11.xlsx' não encontrada.")