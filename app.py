import streamlit as st
from scipy.optimize import linprog
import numpy as np

def main():
    st.set_page_config(page_title="Optimisation des Sièges", layout="centered")
    
    st.markdown(
        """
        <style>
            body {
                background-color: #f4f4f4;
            }
            .stApp {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                max-width: 800px;
                margin: auto;
            }
            .title {
                color: #2E86C1;
                text-align: center;
                font-size: 28px;
                font-weight: bold;
            }
            .stButton>button {
                background-color: #2E86C1 !important;
                color: white !important;
                border-radius: 5px;
                padding: 10px;
            }
            .stButton>button:hover {
                background-color: #1B4F72 !important;
            }
            .stTextInput>div>div>input {
                border-radius: 5px;
                border: 1px solid #2E86C1;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("<div class='title'>Optimisation du remplissage des sièges ✈️</div>", unsafe_allow_html=True)
    
    # Saisie des classes tarifaires
    st.subheader("Définition des classes tarifaires")
    tarif_classes = {}
    num_classes = st.number_input("Nombre de classes tarifaires", min_value=1, value=3, step=1)

    for i in range(num_classes):
        col1, col2 = st.columns(2)
        with col1:
            classe = st.text_input(f"Nom de la classe {i+1}", f"Classe {i+1}")
        with col2:
            tarif = st.number_input(f"Tarif de {classe}", min_value=0.0, value=100.0, step=10.0)
        tarif_classes[classe] = tarif

    # Conversion des tarifs en liste de coefficients
    c = list(tarif_classes.values())

    # Saisie des contraintes
    st.subheader("Définition des contraintes")
    num_contraintes = st.number_input("Nombre de contraintes", min_value=1, value=3, step=1)

    A, b = [], []
    
    for j in range(num_contraintes):
        st.write(f"**Contrainte {j+1}**")
        coefficients = []
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            coeff_str = st.text_input(f"Coefficients des classes tarifaires (séparés par des virgules) pour la contrainte {j+1}", 
                                      ",".join(["1"] * num_classes))
            coefficients = list(map(float, coeff_str.split(',')))

        with col2:
            operateur = st.selectbox(f"Opérateur de la contrainte {j+1}", ["≤", "≥"], key=f"op_{j}")
        
        with col3:
            valeur = st.number_input(f"Valeur de la contrainte {j+1}", min_value=0.0, value=1000.0, step=10.0, key=f"b_{j}")

        if operateur == "≥":
            coefficients = [-x for x in coefficients]
            valeur = -valeur

        A.append(coefficients)
        b.append(valeur)

    # Bouton de résolution
    if st.button("Résoudre"):
        try:
            res = linprog(c=-1 * np.array(c), A_ub=A, b_ub=b, method='highs')
            
            if res.success:
                st.success("Optimisation réussie ! ✅")
                st.write("**Solution optimale :**", np.round(res.x, 2))
                st.write("**Valeur optimale :**", round(-res.fun, 2))
            else:
                st.error("Optimisation échouée : " + res.message)
        except Exception as e:
            st.error(f"Erreur de traitement des entrées : {e}")

if __name__ == "__main__":
    main()
