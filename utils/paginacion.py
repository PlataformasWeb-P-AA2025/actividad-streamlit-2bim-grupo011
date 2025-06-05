import streamlit as st
import math

def paginar(nombre_estado, total_items, label):
    st.sidebar.subheader(f"Paginación: {label}")
    por_pagina = st.sidebar.number_input(
        f"{label} por página",
        min_value=1,
        max_value=50,
        value=5,
        key=f"pp_{nombre_estado}"
    )
    total_paginas = max(1, math.ceil(total_items / por_pagina))

    if nombre_estado not in st.session_state:
        st.session_state[nombre_estado] = 1

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅ Anterior", key=f"prev_{nombre_estado}", disabled=st.session_state[nombre_estado] == 1):
            st.session_state[nombre_estado] -= 1
    with col3:
        if st.button("Siguiente ➡", key=f"next_{nombre_estado}", disabled=st.session_state[nombre_estado] == total_paginas):
            st.session_state[nombre_estado] += 1

    st.markdown(f"**Página {st.session_state[nombre_estado]} de {total_paginas}**")
    offset = (st.session_state[nombre_estado] - 1) * por_pagina
    return offset, por_pagina
