import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def render_performance_chart(df_calc, cap_inicial, acum_port, acum_idx):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_calc['Data'], y=acum_port*cap_inicial, name="Sua Carteira", line=dict(color='#00d1b2', width=4)))
    fig.add_trace(go.Scatter(x=df_calc['Data'], y=acum_idx*cap_inicial, name="Índice BRAX11", line=dict(color='white', dash='dot'), opacity=0.4))
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=20,b=0), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

def render_risk_charts(df_calc, acum_port):
    col_dd, col_vol = st.columns(2)
    with col_dd:
        drawdown = (acum_port / acum_port.cummax() - 1)
        fig_dd = px.area(x=df_calc['Data'], y=drawdown, title="Drawdown Histórico", color_discrete_sequence=['#ff4b4b'])
        fig_dd.update_layout(template="plotly_dark", yaxis_tickformat='.1%')
        st.plotly_chart(fig_dd, use_container_width=True)
    with col_vol:
        rolling_vol = df_calc['Portfolio'].rolling(21).std() * (252**0.5)
        fig_vol = px.line(x=df_calc['Data'], y=rolling_vol, title="Volatilidade Móvel (21d)", color_discrete_sequence=['#ffeb3b'])
        fig_vol.update_layout(template="plotly_dark", yaxis_tickformat='.1%')
        st.plotly_chart(fig_vol, use_container_width=True)

def render_allocation_chart(pesos):
    fig = px.pie(values=list(pesos.values()), names=list(pesos.keys()), 
                 hole=0.6, color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(template="plotly_dark", title="Divisão do Capital")
    st.plotly_chart(fig, use_container_width=True)

def render_heatmap(df_ret):
    df_ret['Year'] = df_ret['Data'].dt.year
    df_ret['Month'] = df_ret['Data'].dt.month
    monthly = df_ret.groupby(['Year', 'Month'])['Portfolio'].apply(lambda x: (1 + x).prod() - 1).unstack()
    monthly.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    st.subheader("Calendário de Retornos (%)")
    st.dataframe(monthly.style.background_gradient(cmap='RdYlGn', axis=None).format("{:.2%}"), use_container_width=True)