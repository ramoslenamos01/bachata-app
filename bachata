import streamlit as st
import random
import json
import os

SAVE_FILE = "moves.json"
MAX_MOVES = 62
MOVES_PER_PICK = 3

# Charger les données si elles existent
def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("remaining", list(range(1, MAX_MOVES + 1))), data.get("used", [])
    else:
        return list(range(1, MAX_MOVES + 1)), []

# Sauvegarder les données
def save_data(remaining, used):
    with open(SAVE_FILE, "w") as f:
        json.dump({"remaining": remaining, "used": used}, f)

# Initialisation
if "remaining" not in st.session_state or "used" not in st.session_state:
    remaining, used = load_data()
    st.session_state.remaining = remaining
    st.session_state.used = used

# 💃 Interface
st.set_page_config(page_title="Bachata Moves 🎶", layout="centered")
st.markdown("<h1 style='text-align: center;'>💃 Bachata Moves Picker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Tire 3 moves aléatoires parmi 62</p>", unsafe_allow_html=True)

# Tirage
if st.button("🎲 Choisir 3 moves", use_container_width=True):
    if len(st.session_state.remaining) < MOVES_PER_PICK:
        st.error("Plus assez de moves restants !")
    else:
        selected = random.sample(st.session_state.remaining, MOVES_PER_PICK)
        for num in selected:
            st.session_state.remaining.remove(num)
            st.session_state.used.append(num)
        st.success(f"Moves à pratiquer : {sorted(selected)}")
        save_data(st.session_state.remaining, st.session_state.used)

# Moves restants
st.markdown("### ✅ Moves restants")
st.write(f"{len(st.session_state.remaining)} moves")
st.code(", ".join(str(n) for n in sorted(st.session_state.remaining)))

# Moves déjà tirés
st.markdown("### 🔁 Moves déjà pratiqués")
st.write(f"{len(st.session_state.used)} moves")
st.code(", ".join(str(n) for n in sorted(st.session_state.used)))

# Reset
if st.button("🔄 Réinitialiser la liste", use_container_width=True):
    st.session_state.remaining = list(range(1, MAX_MOVES + 1))
    st.session_state.used = []
    save_data(st.session_state.remaining, st.session_state.used)
    st.info("Liste réinitialisée avec succès !")
