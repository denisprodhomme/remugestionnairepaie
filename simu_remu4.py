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

# Initialiser l'état de l'application
if 'show_additional_filters' not in st.session_state:
    st.session_state.show_additional_filters = False

# Liste des critères principaux dans l'ordre souhaité
principal_filters = [
    ('Poste', 'Poste'),
    ('Expérience fonction', 'Expérience fonction'),
    ('Structure', 'Structure'),
    ('Localisation', 'Localisation')
]

# Liste des critères supplémentaires dans l'ordre souhaité
additional_filters = [
    ('Taille Société', 'Taille Société'),
    ('Nbre de CCN', 'Nbre de CCN'),
    ('Nbre Bulletins Produits', 'Nbre Bulletins Produits'),
    ('Anglais dans votre quotidien pro ?', 'Anglais dans votre quotidien pro ?'),
    ('Management', 'Management'),
    ('Volume de paies supervisées', 'Volume de paies supervisées'),
    ('Nbre de personnes supervisées', 'Nbre de personnes supervisées')
]

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
        filter_selections = {}
        for label, column in principal_filters:
            filter_selections[column] = st.multiselect(label, df[column].unique(), default=df[column].unique())

        # Bouton pour afficher les filtres supplémentaires
        if st.button("Ajouter des critères supplémentaires"):
            st.session_state.show_additional_filters = True

    with filter_col2:
        if st.session_state.show_additional_filters:
            st.subheader("Filtres supplémentaires")
            for label, column in additional_filters:
                filter_selections[column] = st.multiselect(label, df[column].unique(), default=df[column].unique())
        else:
            for label, column in additional_filters:
                filter_selections[column] = df[column].unique()

    # Filtrer le DataFrame en fonction des choix de l'utilisateur
    filtered_df = df[
        (df['Poste'].isin(filter_selections['Poste'])) &
        (df['Expérience fonction'].isin(filter_selections['Expérience fonction'])) &
        (df['Structure'].isin(filter_selections['Structure'])) &
        (df['Taille Société'].isin(filter_selections['Taille Société'])) &
        (df['Nbre de CCN'].isin(filter_selections['Nbre de CCN'])) &
        (df['Nbre Bulletins Produits'].isin(filter_selections['Nbre Bulletins Produits'])) &
        (df['Anglais dans votre quotidien pro ?'].isin(filter_selections['Anglais dans votre quotidien pro ?'])) &
        (df['Localisation'].isin(filter_selections['Localisation'])) &
        (df['Management'].isin(filter_selections['Management'])) &
        (df['Volume de paies supervisées'].isin(filter_selections['Volume de paies supervisées'])) &
        (df['Nbre de personnes supervisées'].isin(filter_selections['Nbre de personnes supervisées']))
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
