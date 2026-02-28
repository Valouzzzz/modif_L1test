import fitz  # Bibliothèque PyMuPDF
import re
import os

def extraire_description_pdf(chemin_pdf, nom_fonction):
    """Cherche le nom de la fonction dans le PDF et renvoie les 25 mots suivants."""
    try:
        doc = fitz.open(chemin_pdf)
        texte_complet = ""
        for page in doc:
            texte_complet += page.get_text("text")
        
        # Nettoyage simple du texte (enlève les retours à la ligne inutiles)
        texte_complet = " ".join(texte_complet.split())
        
        # Recherche du nom de la fonction suivi du texte
        # On cherche le nom de la fonction et on capture ce qui suit
        pattern = rf"{nom_fonction}\s+(.*?)(?=\s\w+\s\(|$)"
        match = re.search(pattern, texte_complet, re.IGNORECASE)
        
        if match:
            description = match.group(1).strip()
            mots = description.split()
            return " ".join(mots[:25]) # On garde les 25 premiers mots
        
        return "Description non trouvée dans le PDF."
    except Exception as e:
        return f"Erreur lors de la lecture du PDF : {e}"

def mettre_a_jour_fichier(chemin_python, chemin_pdf):
    """Parcourt le fichier .py et remplace les balises de docstring."""
    if not os.path.exists(chemin_python):
        print(f"Erreur : Le fichier {chemin_python} n'existe pas.")
        return

    with open(chemin_python, 'r', encoding='utf-8') as f:
        lignes = f.readlines()

    nouveau_contenu = []
    derniere_fonction = None

    for ligne in lignes:
        # Détecter le nom de la fonction : def nom_fonction(...)
        match_func = re.match(r"def\s+(\w+)\s*\(", ligne.strip())
        if match_func:
            derniere_fonction = match_func.group(1)
        
        # Détecter la ligne à remplacer
        cible = '""" à_remplacer_par_ce_que_fait_la_fonction'
        if cible in ligne and derniere_fonction:
            print(f"Mise à jour de la fonction : {derniere_fonction}")
            description = extraire_description_pdf(chemin_pdf, derniere_fonction)
            
            # On reconstruit la ligne avec la description trouvée
            ligne = ligne.replace(cible, f'""" {description}')
        
        nouveau_contenu.append(ligne)

    # Sauvegarde du fichier modifié
    with open(chemin_python, 'w', encoding='utf-8') as f:
        f.writelines(nouveau_contenu)
    print("Mise à jour terminée !")