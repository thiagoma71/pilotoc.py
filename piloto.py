import os
import streamlit as st
from groq import Groq

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Assistente Groq - Streamlit",
    page_icon="✈️",
    layout="centered"
)

# Inicialização do cliente Groq
# A chave de API é buscada automaticamente nas variáveis de ambiente (ideal para o Render)
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("A chave da API da Groq (GROQ_API_KEY) não foi encontrada nas variáveis de ambiente.")
    st.stop()

client = Groq(api_key=api_key)

# Título da aplicação
st.title("🛩️ Painel de Comunicação com IA")
st.markdown("Sistema de bordo conectado à API da Groq.")

# Inicialização do histórico de mensagens no estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibição do histórico de mensagens na interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário (chat input)
if prompt := st.chat_input("Digite sua mensagem para o comandante..."):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta utilizando o modelo da Groq
    with st.chat_message("assistant"):
        try:
            # Seleção do modelo (ex: llama-3.3-70b-versatile ou outro disponível)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            
            response_content = completion.choices[0].message.content
            st.markdown(response_content)
            
            # Adiciona a resposta do assistente ao histórico
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            
        except Exception as e:
            st.error(f"Erro ao comunicar com a API da Groq: {e}")