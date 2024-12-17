import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui
import pathlib

# Configuration de la page pour utiliser la largeur maximale
st.set_page_config(layout="wide")

# Fonction pour charger le CSS du dossier "assets"
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# Charger le CSS externe
css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

# Lire le fichier CSV en un DataFrame
df = pd.read_csv('simu_streamlit.csv', sep=';', encoding='utf-8')

# Créer les onglets
tabs = st.tabs(["Simulateur de Rémunération", "Présentation"])

# Fonction pour formater les nombres avec un espace comme séparateur de milliers
def format_number_with_space(number):
    return f"{number:,.0f}".replace(",", " ")

# Page Simulateur de Rémunération
def page_simulateur():
    st.title('Simulateur de Rémunération dans le domaine de la Paie en France')

    # Créer une colonne pour les metric_cards
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

    st.subheader("Filtres - A choisir en fonction de votre situation")

    # Créer deux colonnes pour les filtres
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        st.subheader("Filtres principaux")
        poste = st.multiselect('Poste', df['Poste'].unique(), default=[df['Poste'].unique()[0]])
        experience = st.multiselect('Expérience fonction', df['Expérience fonction'].unique(), default=df['Expérience fonction'].unique())
        structure = st.multiselect('Structure', df['Structure'].unique(), default=[df['Structure'].unique()[0]])
        region = st.multiselect('Localisation', df['Localisation'].unique(), default=df['Localisation'].unique())

        # Bouton pour afficher les filtres supplémentaires
        if st.button("Ajouter des critères supplémentaires"):
            st.session_state.show_additional_filters = True
        else:
            st.session_state.show_additional_filters = False

    with filter_col2:
        if 'show_additional_filters' in st.session_state and st.session_state.show_additional_filters:
            st.subheader("Filtres supplémentaires")
            taille_societe = st.multiselect('Taille Société', df['Taille Société'].unique(), default=df['Taille Société'].unique())
            nombre_ccn = st.multiselect('Nbre de CCN', df['Nbre de CCN'].unique(), default=df['Nbre de CCN'].unique())
            nbre_bull_prod = st.multiselect('Nbre Bulletins Produits', df['Nbre Bulletins Produits'].unique(), default=df['Nbre Bulletins Produits'].unique())
            anglais = st.multiselect('Anglais dans votre quotidien pro ?', df['Anglais dans votre quotidien pro ?'].unique(), default=df['Anglais dans votre quotidien pro ?'].unique())
            Management = st.multiselect('Management', df['Management'].unique(), default=df['Management'].unique())
            volume_supervise = st.multiselect('Volume de paies supervisées', df['Volume de paies supervisées'].unique(), default=df['Volume de paies supervisées'].unique())
            nombre_supervise = st.multiselect('Nbre de personnes supervisées', df['Nbre de personnes supervisées'].unique(), default=df['Nbre de personnes supervisées'].unique())
        else:
            taille_societe = df['Taille Société'].unique()
            nombre_ccn = df['Nbre de CCN'].unique()
            nbre_bull_prod = df['Nbre Bulletins Produits'].unique()
            anglais = df['Anglais dans votre quotidien pro ?'].unique()
            Management = df['Management'].unique()
            volume_supervise = df['Volume de paies supervisées'].unique()
            nombre_supervise = df['Nbre de personnes supervisées'].unique()

    # Filtrer le DataFrame en fonction des choix de l'utilisateur
    filtered_df = df[
        (df['Poste'].isin(poste)) &
        (df['Expérience fonction'].isin(experience)) &
        (df['Structure'].isin(structure)) &
        (df['Taille Société'].isin(taille_societe)) &
        (df['Nbre de CCN'].isin(nombre_ccn)) &
        (df['Nbre Bulletins Produits'].isin(nbre_bull_prod)) &
        (df['Anglais dans votre quotidien pro ?'].isin(anglais)) &
        (df['Localisation'].isin(region)) &
        (df['Management'].isin(Management)) &
        (df['Volume de paies supervisées'].isin(volume_supervise)) &
        (df['Nbre de personnes supervisées'].isin(nombre_supervise))
    ]

    # Calculer la rémunération moyenne, minimale, maximale et médiane
    if not filtered_df.empty:
        avg_salary = filtered_df['Rémunération brute'].mean()
        min_salary = filtered_df['Rémunération brute'].min()
        max_salary = filtered_df['Rémunération brute'].max()
        median_salary = filtered_df['Rémunération brute'].median()
        num_results = filtered_df.shape[0]

        # Afficher les résultats avec un espace comme séparateur de milliers
        with metric_col1:
            ui.metric_card(title="Nombre de réponses", content=format_number_with_space(num_results), key="card1")
        with metric_col2:
            ui.metric_card(title="Rémunération Moyenne", content=f"{format_number_with_space(avg_salary)} €", key="card2")
        with metric_col3:
            ui.metric_card(title="Rémunération Minimale", content=f"{format_number_with_space(min_salary)} €", key="card3")
        with metric_col4:
            ui.metric_card(title="Rémunération Maximale", content=f"{format_number_with_space(max_salary)} €", key="card4")
        with metric_col5:
            ui.metric_card(title="Rémunération Médiane", content=f"{format_number_with_space(median_salary)} €", key="card5")

    else:
        st.write("Aucun résultat ne correspond à votre sélection.")

# Page Présentation
def page_presentation():
    st.title('Présentation')
    st.write("J'accompagne les entreprises d’Île-de-France pour recruter les meilleurs profils PAIE & ADP, grâce à la force de mon réseau ! (au succès, sans exclusivité)")
    st.write("Sébastien Tronc")
    st.write("Voici le lien vers mon profil Linkedin ")
    ui.link_button(text="Sébastien Tronc Linkedin", url="https://www.linkedin.com/in/sebastientronc/", key="link_btn")

# Afficher le contenu des onglets
with tabs[0]:
    page_simulateur()

with tabs[1]:
    page_presentation()
