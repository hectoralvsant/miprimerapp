import random
import re
import streamlit as st
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="Ecuaciones de 1er Grado", page_icon="🧮", layout="centered")

# --- Helpers ---
def nueva_ecuacion():
    # Garantiza solución entera escogiendo x primero
    x = random.randint(-20, 20)
    a_choices = [i for i in range(-9, 10) if i != 0]  # evita a=0
    a = random.choice(a_choices)
    b = random.randint(-30, 30)
    c = a * x + b
    st.session_state.eq = {"a": a, "b": b, "c": c, "x": x}
    st.session_state.feedback = ""
    st.session_state.correcta = None

def nueva_ecuacion():
    x = random.randint(-20, 20)
    a_choices = [i for i in range(-9, 10) if i != 0]
    a = random.choice(a_choices)
    b = random.randint(-30, 30)
    c = a * x + b
    st.session_state.eq = {"a": a, "b": b, "c": c, "x": x}
    st.session_state.feedback = ""
    st.session_state.correcta = None

def pretty_latex(a, b, c):
    # Construye un string LaTeX ordenado como ax + b = c (manejando signos)
    if a == 1:
        ax = "x"
    elif a == -1:
        ax = "-x"
    else:
        ax = f"{a}x"
    if b == 0:
        left = ax
    elif b > 0:
        left = f"{ax} + {abs(b)}"
    else:
        left = f"{ax} - {abs(b)}"
    return rf"{left} = {c}"

def es_entero(s: str) -> bool:
    return re.fullmatch(r"-?\d+", s.strip()) is not None

# --- Estado inicial ---
if "eq" not in st.session_state:
    nueva_ecuacion()

st.title("🧮 Resolución de ecuaciones de primer grado")
st.write("Adivina el valor de **x** que satisface la ecuación. Tu respuesta debe ser un **entero**.")

# --- Mostrar ecuación actual ---
a = st.session_state.eq["a"]
b = st.session_state.eq["b"]
c = st.session_state.eq["c"]
x_sol = st.session_state.eq["x"]

st.latex(pretty_latex(a, b, c))

col1, col2 = st.columns([2, 1])

with col1:
    answer = st.text_input("Tu respuesta (entero)", key="answer", placeholder="Ej. -3, 0, 42")

with col2:
    st.write("")  # separador
    verificar = st.button("Verificar ✅")
    nueva = st.button("Nueva ecuación 🔄")

if nueva:
    nueva_ecuacion()
    st.experimental_rerun()

if verificar:
    if not es_entero(answer or ""):
        st.error("Por favor, ingresa un **número entero** (sin decimales).")
    else:
        valor = int(answer.strip())
        if valor == x_sol:
            st.success("¡Correcto! 🎯")
            rain(emoji="🎉", font_size=40, falling_speed=5, animation_length="3")
            st.session_state.correcta = True
        else:
            st.warning("No es correcto. Inténtalo de nuevo.")
            st.session_state.correcta = False

with st.expander("Mostrar solución"):
    st.markdown(f"La solución es **x = {x_sol}**.")
    st.markdown(
        rf"""Despeje:
1. {pretty_latex(a, b, c)}
2. {rf"{a}x = {c - b}"}
3. {rf"x = \dfrac{{{c - b}}}{{{a}}} = {x_sol}"}"""
    )

st.caption("Hecho con ❤️ en Streamlit.")
