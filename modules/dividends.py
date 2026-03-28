import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

def get_dividend_data(tickers):
    div_data = []
    for t in tickers:
        # No Brasil, o yfinance precisa do ".SA"
        ticker_sa = f"{t}.SA" if not t.endswith(".SA") else t
        try:
            asset = yf.Ticker(ticker_sa)
            # Pegando o histórico de dividendos
            history = asset.dividends
            if not history.empty:
                # Soma dos dividendos nos últimos 12 meses
                last_12m = history.last('365D').sum()
                # Preço atual para o cálculo do Yield
                price = asset.history(period="1d")['Close'].iloc[-1]
                yield_perc = (last_12m / price) if price > 0 else 0
                
                div_data.append({
                    "Ativo": t,
                    "Dividendos (12m)": round(last_12m, 2),
                    "Preço Atual": round(price, 2),
                    "DY (%)": round(yield_perc * 100, 2)
                })
        except:
            continue
    return pd.DataFrame(div_data)

def render_dividend_analysis(tickers):
    st.subheader("💰 Análise de Proventos (Yield)")
    
    with st.spinner("Buscando dados no Yahoo Finance..."):
        df_div = get_dividend_data(tickers)
    
    if not df_div.empty:
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.dataframe(df_div.set_index("Ativo"), use_container_width=True)
            
        with c2:
            fig = px.bar(df_div, x="Ativo", y="DY (%)", 
                         title="Dividend Yield Comparativo",
                         color="DY (%)", 
                         color_continuous_scale='GnBu')
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Não foram encontrados dados de dividendos para os ativos selecionados.")