import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse

def render_market_intelligence(tickers):
    st.subheader("📰 Market Intelligence Feed")
    st.caption("Notícias globais via Google News (Real-time)")
    
    if not tickers:
        st.info("Selecione ativos na barra lateral para ver as notícias.")
        return

    for t in tickers:
        with st.expander(f"Notícias de {t}", expanded=True):
            # Criamos uma query de busca específica para o ticker no Google News
            query = urllib.parse.quote(f"{t} stock B3")
            url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-pt"
            
            try:
                feed = feedparser.parse(url)
                
                if feed.entries:
                    for item in feed.entries[:3]: # Top 3 notícias
                        col_icon, col_txt = st.columns([1, 10])
                        with col_icon:
                            st.write("🔹")
                        with col_txt:
                            # Título e Link
                            title = item.title
                            link = item.link
                            
                            # Formatação da data
                            published = item.get('published', 'Data indisponível')
                            # Google News usa um formato de data amigável, vamos apenas limpar o excesso
                            date_clean = published.split(' +')[0] if ' +' in published else published
                            
                            st.markdown(f"**[{title}]({link})**")
                            st.caption(f"Fonte: Google News | {date_clean}")
                else:
                    st.write(f"Nenhuma notícia recente encontrada para {t}.")
            
            except Exception as e:
                st.write(f"Erro ao carregar notícias para {t}: {e}")