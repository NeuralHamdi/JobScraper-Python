import os
import time
import requests
from bs4 import BeautifulSoup


# Demander les compétences à filtrer
def demander_competences():
    print("Entrez les compétences à éviter (tapez 'exit' pour terminer) :")
    competences = []
    while True:
        competence = input("> ").strip()
        if competence.lower() == "exit":
            break
        if competence:  # Évite d'ajouter des entrées vides
            competences.append(competence)
    return competences


# Fonction qui récupère les offres d'emploi et applique le filtre
def chercher_offres(competences):
    url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation="

    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie s'il y a une erreur HTTP
    except requests.RequestException as e:
        print(f"❌ Erreur de connexion : {e}")
        return

    # Analyser le code HTML de la page
    soup = BeautifulSoup(response.text, "lxml")
    offres = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

    if not offres:
        print("⚠️ Aucune offre trouvée.")
        return

    # Créer un dossier "offres" pour enregistrer les résultats
    os.makedirs("offres", exist_ok=True)

    nb_offres_enregistrees = 0

    for i, offre in enumerate(offres, start=1):
        date = offre.find("span", class_="sim-posted").span.text.strip()

        # Vérifier si l'offre est récente
        if "few" in date.lower():
            entreprise = offre.find("h3", class_="joblist-comp-name").text.strip()
            competences_requises = offre.find("ul", class_="list-job-dtl clearfix").text.strip()
            lien = offre.h2.a["href"]

            # Vérifier si l'offre contient une compétence à éviter
            if not any(c.lower() in competences_requises.lower() for c in competences):
                fichier_nom = f"offres/offre_{i}.txt"

                with open(fichier_nom, "w", encoding="utf-8") as f:
                    f.write(f"🏢 Entreprise : {entreprise}\n")
                    f.write(f"📌 Compétences requises : {competences_requises}\n")
                    f.write(f"📅 Date de publication : {date}\n")
                    f.write(f"🔗 Plus d'infos : {lien}\n")
                    f.write("=" * 50 + "\n")

                nb_offres_enregistrees += 1

    print(f"✅ {nb_offres_enregistrees} offres enregistrées.")


# Programme principal
if __name__ == "__main__":
    competences_a_eviter = demander_competences()

    while True:
        chercher_offres(competences_a_eviter)
        print("⏳ Attente de 10 minutes avant la prochaine recherche...")
        time.sleep(600)  # 10 minutes
