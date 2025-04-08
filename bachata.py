import streamlit as st
import random
import json
import re
import requests
import base64

# ⚙️ Paramètres
MAX_MOVES = 62
MOVES_PER_PICK = 3

st.set_page_config(page_title="Bachata Moves Picker", layout="centered")
st.markdown("## 💃 Bachata Moves Picker")

BANNED_WORDS = ["putain", "merde", "fuck", "shit", "salope", "connard", "enculé", "fdp", "ntm", "nique", "raciste", "zaml"]

username = st.text_input("Entre ton prénom :").strip().lower()

if any(bad_word in username for bad_word in BANNED_WORDS):
    st.error("⛔ Pseudo inapproprié. Merci de rester respectueux.")
    st.stop()

if not re.match(r"^[a-zA-Z0-9_-]{2,20}$", username):
    st.warning("⛔ Ton pseudo doit faire 2 à 20 caractères valides (lettres, chiffres, _ ou -).")
    st.stop()

if not username:
    st.warning("➡️ Entrez votre nom ci-dessus pour commencer.")
    st.stop()

# GitHub setup
TOKEN = st.secrets["github"]["token"]
REPO = st.secrets["github"]["repo"]
BRANCH = st.secrets["github"]["branch"]
FILEPATH = f"data/moves_{username}.json"

headers = {'Authorization': f'token {TOKEN}'}

# Functions for GitHub
def load_github_file():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILEPATH}?ref={BRANCH}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        data = json.loads(base64.b64decode(content["content"]).decode())
        return data, content["sha"]
    else:
        return {"remaining": list(range(1, MAX_MOVES + 1)), "used": [], "custom": []}, None


def save_github_file(data, sha=None):
    url = f"https://api.github.com/repos/{REPO}/contents/{FILEPATH}"
    encoded_data = base64.b64encode(json.dumps(data).encode()).decode()

    commit_message = f"Update moves for {username}"

    payload = {
        "message": commit_message,
        "content": encoded_data,
        "branch": BRANCH
    }

    if sha:
        payload["sha"] = sha

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        new_sha = response.json()['content']['sha']
        return True, new_sha
    else:
        with st.expander("🛠️ Détails"):
            st.write("Statut :", response.status_code)
            st.write("Réponse :", response.json())
        return False, None


# Load from GitHub
if "remaining" not in st.session_state or st.session_state.get("user") != username:
    data, sha = load_github_file()
    st.session_state.remaining = data["remaining"]
    st.session_state.used = data["used"]
    st.session_state.custom = data.get("custom", [])
    st.session_state.sha = sha
    st.session_state.user = username

col1, col2 = st.columns(2)

with col1:
    if st.button("🎯 Tirer 3 moves", use_container_width=True):
        if len(st.session_state.remaining) < MOVES_PER_PICK:
            st.error("❌ Plus assez de moves restants !")
        else:
            selected = random.sample(st.session_state.remaining, MOVES_PER_PICK)
            for num in selected:
                st.session_state.remaining.remove(num)
                st.session_state.used.append(num)
            success, new_sha = save_github_file({"remaining": st.session_state.remaining, "used": st.session_state.used, "custom": st.session_state.custom}, st.session_state.sha)
            if success:
                st.session_state.sha = new_sha
                st.success(f"Moves à pratiquer : {sorted(selected)}")
            else:
                st.error("Erreur lors de la sauvegarde sur GitHub.")

with col2:
    if st.button("🔄 Réinitialiser", use_container_width=True):
        st.session_state.remaining = list(range(1, MAX_MOVES + 1))
        st.session_state.used = []
        st.session_state.custom = []
        success, new_sha = save_github_file({"remaining": st.session_state.remaining, "used": [], "custom": []}, st.session_state.sha)
        if success:
            st.session_state.sha = new_sha
            st.info("Liste réinitialisée pour " + username)
        else:
            st.error("Erreur lors de la réinitialisation sur GitHub.")

# Gestion manuelle
st.markdown("---")
st.markdown("### 🛠️ Gestion manuelle")
num_to_add = st.text_input("Ajouter un numéro ou une vidéo (Instagram)")
if st.button("➕ Ajouter"):
    if num_to_add.isdigit():
        num = int(num_to_add)
        if num not in st.session_state.remaining:
            st.session_state.remaining.append(num)
            st.success(f"Numéro {num} ajouté aux moves restants.")
        else:
            st.warning(f"Le numéro {num} existe déjà.")
    else:
        if num_to_add not in st.session_state.custom:
            st.session_state.custom.append(num_to_add)
            st.success("Lien Instagram ajouté aux moves personnalisés.")
        else:
            st.warning("Lien déjà ajouté.")
    success, new_sha = save_github_file({"remaining": st.session_state.remaining, "used": st.session_state.used, "custom": st.session_state.custom}, st.session_state.sha)
    if success:
        st.session_state.sha = new_sha

num_to_remove = st.text_input("Supprimer un numéro")
if st.button("➖ Supprimer"):
    if num_to_remove.isdigit() and int(num_to_remove) in st.session_state.remaining:
        st.session_state.remaining.remove(int(num_to_remove))
        st.success(f"Numéro {num_to_remove} supprimé.")
        success, new_sha = save_github_file({"remaining": st.session_state.remaining, "used": st.session_state.used, "custom": st.session_state.custom}, st.session_state.sha)
        if success:
            st.session_state.sha = new_sha
    else:
        st.error("Numéro non trouvé dans la liste principale.")