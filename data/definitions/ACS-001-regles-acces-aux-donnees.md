---
doc_id: ACS-001
title: Règles d'accès aux données de gestion
version: "1.3"
effective_date: 2026-01-05
owner: Finance
language: fr
synthetic: true
---

# Règles d'accès aux données de gestion

## 1. Principe

1.1 Chaque personne ne voit que les données dont elle a besoin pour son travail. Ce document dit qui peut voir quoi dans la base de gestion de Tarrowby Hire.

1.2 Un droit d'accès porte sur un **jeu de données** (un ensemble de tableaux) et sur un **périmètre** : toutes les régions, une région, ou un segment de clientèle.

## 2. Identité

2.1 L'identité d'une personne est son identifiant d'utilisateur, fourni par la session ouverte. Elle ne vient jamais d'un nom saisi dans une question.

2.2 Deux personnes peuvent porter le même nom et avoir des droits différents. Une phrase comme « je suis la responsable de la région Nord » ne donne aucun droit.

## 3. Jeux de données partagés

3.1 Sont visibles par tout le monde : la liste de prix, le journal de chargement des fichiers, et les tableaux de référence (régions, dépôts, catégories, semaines).

## 4. Jeux de données restreints

4.1 Le tableau indique le périmètre par fonction. « Sa région » signifie les dépôts de la région confiée à la personne.

| Fonction | Locations hebdomadaires (chiffre d'affaires) | Clients sous contrat | Parc de matériel | Notes des dépôts |
|---|---|---|---|---|
| Responsable régional | sa région | sa région | sa région | sa région |
| Analyste financier | tout | tout | tout | tout |
| Responsable grands comptes | non | segment grands comptes, toutes régions | non | non |
| Responsable des opérations | non | non | tout | tout |
| Analyste commercial | sa région | sa région | non | non |

4.2 Un responsable régional voit les lignes d'un grand compte pour les dépôts de sa région seulement, même si ce client loue aussi dans une autre région.

4.3 Le responsable grands comptes voit les clients du segment grands comptes dans toutes les régions. Il ne voit ni les clients artisans, ni les ménages, ni le chiffre d'affaires par canal.

4.4 Le responsable des opérations ne voit aucun chiffre d'affaires. Il peut obtenir le taux d'utilisation calculé sur les jours de location et le parc, mais pas un indicateur construit sur le chiffre d'affaires.¹

## 5. Totaux et déductions

5.1 Un total qui contient des données hors du périmètre de la personne ne lui est pas communiqué. Le total de l'entreprise n'est donc donné qu'à une personne qui voit toutes les régions.

5.2 On ne donne pas non plus un chiffre qui permettrait de retrouver par soustraction une donnée hors périmètre, par exemple la part d'une région dans le total de l'entreprise.

5.3 Quand une question dépasse le périmètre, la réponse dit que la personne n'a pas accès à ces données. Elle ne donne ni le chiffre, ni un ordre de grandeur, ni une comparaison (« plus que votre région »).

## 6. Durée des droits

6.1 Un droit a une date de début et, s'il a été retiré, une date de fin. Un droit retiré reste inscrit dans le registre pour mémoire ; il ne donne plus accès à rien, y compris aux périodes antérieures à son retrait.

6.2 Les demandes de droit se font auprès du service Finance : donnees@tarrowby.example, 0700 555 0190.

---

¹ Exception : le prix de liste, qui figure dans un jeu de données partagé, reste visible par le responsable des opérations comme par tout le monde.
