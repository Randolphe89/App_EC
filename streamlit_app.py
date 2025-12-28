import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="App Expert-Comptable", page_icon="📊")
st.title("📊 Assistant Expert-Comptable")
st.caption("Propulsé par Gemini 1.5 Flash")

# --- RÉCUPÉRATION DE LA CLÉ API ---
# On cherche la clé dans les "Secrets" de Streamlit pour la sécurité
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Si pas de secret configuré, on affiche un champ de saisie temporaire
    api_key = st.sidebar.text_input("Clé API Google", type="password")

if not api_key:
    st.info("Veuillez ajouter votre clé API Google dans les réglages (Secrets) pour activer l'assistant.", icon="🔑")
    st.stop()

# --- CONFIGURATION DU MODÈLE ---
genai.configure(api_key=api_key)

# Réglages du modèle (température, etc.)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 4096,
}

# --- INSTRUCTIONS SYSTÈME ---
# C'est ici que vous collez vos instructions de Google AI Studio
system_instruction = """
TU ES UN EXPERT-COMPTABLE FRANÇAIS. 
TA MISSION EST D'AIDER LES UTILISATEURS SUR DES QUESTIONS DE COMPTABILITÉ, FISCALITÉ ET GESTION.
RESTE PROFESSIONNEL, PRÉCIS ET PÉDAGOGUE.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction,
)

# --- GESTION DE L'HISTORIQUE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INTERACTION UTILISATEUR ---
if prompt := st.chat_input("Posez votre question comptable ici..."):
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer et afficher la réponse de Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Envoi du message au modèle
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Sauvegarder la réponse dans l'historique
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Erreur : {e}")
