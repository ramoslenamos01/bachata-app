import streamlit as st
import random
import json
import os
import glob
import re

# ⚙️ Paramètres de l'app
MAX_MOVES = 62
MOVES_PER_PICK = 3

# 📦 Utilisateur actuel (entrée en haut de page)
st.set_page_config(page_title="Bachata Moves Picker", layout="centered")
st.markdown("## 💃 Bachata Moves Picker")

BANNED_WORDS = ["putain", "merde", "fuck", "shit", "salope", "connard", "enculé", "fdp", "ntm", "nique", "raciste","zaml"]

# Nettoyage du nom
username = st.text_input("Entre ton prénom :").strip().lower()

# Vérification du pseudo
if any(bad_word in username for bad_word in BANNED_WORDS):
    st.error("⛔ Pseudo inapproprié. Merci de rester respectueux.")
    st.stop()

# Filtrage des caractères spéciaux
if not re.match(r"^[a-zA-Z0-9_\-]{2,20}$", username):
    st.warning("⛔ Ton pseudo doit faire 2 à 20 caractères valides (lettres, chiffres, _ ou -).")
    st.stop()
# Ne rien afficher tant qu’un nom n’est pas entré
if not username:
    st.warning("➡️ Entrez votre nom ci-dessus pour commencer.")
    st.stop()

# 🔐 Fichier spécifique à l'utilisateur
SAVE_FILE = f"moves_{username.lower().strip()}.json"

# 💾 Chargement/sauvegarde des données
def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("remaining", list(range(1, MAX_MOVES + 1))), data.get("used", [])
    else:
        return list(range(1, MAX_MOVES + 1)), []

def save_data(remaining, used):
    with open(SAVE_FILE, "w") as f:
        json.dump({"remaining": remaining, "used": used}, f)

# 📥 Charger dans session_state
if "remaining" not in st.session_state or "used" not in st.session_state or st.session_state.get("user") != username:
    remaining, used = load_data()
    st.session_state.remaining = remaining
    st.session_state.used = used
    st.session_state.user = username

# 🎲 Tirage et réinitialisation
col1, col2 = st.columns(2)



with st.expander("👥 Utilisateurs enregistrés", expanded=False):
    user_files = glob.glob("moves_*.json")
    usernames = [f.replace("moves_", "").replace(".json", "") for f in user_files]

    if usernames:
        st.write(f"**{len(usernames)} utilisateur(s)** enregistré(s) :")
        st.code(", ".join(sorted(usernames)))
    else:
        st.info("Aucun utilisateur encore enregistré.")

with col1:
    if st.button("🎯 Tirer 3 moves", use_container_width=True):
        if len(st.session_state.remaining) < MOVES_PER_PICK:
            st.error("❌ Plus assez de moves restants !")
        else:
            selected = random.sample(st.session_state.remaining, MOVES_PER_PICK)
            for num in selected:
                st.session_state.remaining.remove(num)
                st.session_state.used.append(num)
            st.success(f"Moves à pratiquer : {sorted(selected)}")
            save_data(st.session_state.remaining, st.session_state.used)

with col2:
    if st.button("🔄 Réinitialiser", use_container_width=True):
        st.session_state.remaining = list(range(1, MAX_MOVES + 1))
        st.session_state.used = []
        save_data(st.session_state.remaining, st.session_state.used)
        st.info("Liste réinitialisée pour " + username)

# ✅ Moves restants
with st.expander("📋 Moves restants", expanded=True):
    st.write(f"**{len(st.session_state.remaining)} moves**")
    st.code(", ".join(str(n) for n in sorted(st.session_state.remaining)) or "Aucun")

# 🔁 Moves déjà pratiqués
with st.expander("🧠 Moves déjà pratiqués", expanded=True):
    st.write(f"**{len(st.session_state.used)} moves**")
    st.code(", ".join(str(n) for n in sorted(st.session_state.used)) or "Aucun")

st.markdown("---")

with st.expander("👮 Interface Admin"):
    admin_password = st.text_input("Mot de passe admin :", type="password")

    if admin_password == "bachata42":  # Tu peux changer ce mot de passe
        st.success("Accès admin validé ✅")

        user_files = glob.glob("moves_*.json")
        usernames = [f.replace("moves_", "").replace(".json", "") for f in user_files]

        st.write(f"Utilisateurs enregistrés : {len(usernames)}")
        selected_user = st.selectbox("Sélectionner un utilisateur à supprimer", usernames)

        if st.button("❌ Supprimer ce fichier utilisateur"):
            try:
                os.remove(f"moves_{selected_user}.json")
                st.success(f"Fichier de {selected_user} supprimé.")
            except Exception as e:
                st.error(f"Erreur lors de la suppression : {e}")
    elif admin_password != "":
        st.error("Mot de passe incorrect.")
