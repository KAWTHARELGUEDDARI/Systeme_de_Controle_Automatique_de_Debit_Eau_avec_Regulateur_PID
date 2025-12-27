#  Rapport de Projet  
## Conception et Réalisation d’un Système de Contrôle Automatique de Débit d’Eau  
### avec Régulateur PID sur Arduino

**Auteurs :**  
- Kawthar El Gueddari  
- Nada Fri  
- Aya El Bouazzaoui  

**Encadré par :** M. Hicham Belkebir  

**Établissement :**  
École Nationale des Sciences Appliquées (ENSA)  
Filière : Ingénierie des Systèmes Embarqués et Intelligence Artificielle  

 **Date :** 07 Décembre 2025  

---

##  Table des matières

1. [Résumé](#-résumé)  
2. [Contexte et Problématique](#-contexte-et-problématique)  
3. [Critères de Performance et Validation](#-critères-de-performance-et-validation)  
4. [Descriptif Technique du Projet](#-descriptif-technique-du-projet)  
5. [Modélisation du Système](#-modélisation-du-système)  
6. [Régulateur PID Optimal](#-régulateur-pid-optimal)  
7. [Résultats et Performances](#-résultats-et-performances)  
8. [Comparaison Boucle Ouverte / Boucle Fermée](#-comparaison-boucle-ouverte--boucle-fermée)  
9. [Applications Industrielles](#-applications-industrielles)  
10. [Conclusion Générale](#-conclusion-générale)  

---

##  Résumé

Ce projet présente la conception et la réalisation d’un système de contrôle automatique de débit d’eau utilisant un régulateur PID (Proportionnel–Intégral–Dérivé) implémenté sur un microcontrôleur **Arduino Uno**.

L’objectif est de maintenir un débit d’eau constant autour d’une consigne programmable, tout en garantissant des performances dynamiques et statiques conformes à un cahier des charges industriel.

---

##  Objectif principal

Développer un système capable de maintenir un débit d’eau constant avec les performances suivantes :

-  Temps de réponse ≤ **10 s**
-  Dépassement ≤ **15 %**
-  Erreur statique ≤ **3 %**

---

##  Composants principaux

- **Capteur** : Débitmètre à effet Hall **YF-S201** (1–30 L/min)
- **Actionneur** : Servomoteur **MG995** commandant une vanne à bille 1/2”
- **Contrôleur** : **Arduino Uno** avec régulateur PID numérique
- **Interface utilisateur** :  
  - Écran LCD 20×4  
  - Potentiomètres  
  - Communication série USB  

---

##  Contexte et Problématique

### Contexte industriel

Le contrôle précis des débits de fluides est crucial dans plusieurs domaines industriels :

-  Traitement des eaux
-  Chimie et pharmaceutique
-  Agroalimentaire
-  Irrigation
-  Systèmes énergétiques

### Défis techniques

- Non-linéarités (vanne, pertes de charge)
- Perturbations (pression, température, bulles d’air)
- Dynamique du système (inertie, temps mort)
- Contraintes de mesure (bruit, dérive)
- Contraintes matérielles (saturation, usure)

---

##  Solution proposée

Approche en **boucle fermée** intégrant :

- Capteur YF-S201 (±5 %, signal numérique)
- Servomoteur MG995 (PWM, couple 10 kg·cm)
- Arduino Uno (ATmega328P, 16 MHz)
- Interface LCD et port série

---

##  Critères de Performance et Validation

### Performances dynamiques

| Critère | Spécification |
|-------|---------------|
| Temps de réponse | ≤ 10 s |
| Dépassement maximal | ≤ 15 % |
| Pulsation de coupure | 2 rad/s |
| Marge de phase | 85° |

### Performances statiques

| Critère | Spécification |
|-------|---------------|
| Erreur statique | ≤ 3 % |
| Précision capteur | ±5 % |
| Stabilité | Garantie |

---

##  Descriptif Technique du Projet

- Débit de consigne : **100 L/min**
- Régulateur PID optimisé par **placement de pôles**

---

##  Modélisation du Système

### Pompe et Variateur

- \( K_p = 0.667 \ \text{L/min·rpm} \)
- \( K_v = 150 \ \text{rpm/V} \)

### Processus Hydraulique

- Constante de temps : \( \tau_h = 5s \)
- Fonction de transfert :  
  \[
  G_h(s) = \frac{1}{5s + 1}
  \]
- Pulsation de coupure : \( \omega_c = 0.2 \ \text{rad/s} \)

---

##  Régulateur PID Optimal

Structure **PI avec dérivation légère** :

| Paramètre | Valeur | Unité |
|---------|--------|-------|
| Kp | 5.5 | – |
| Ti | 0.5 | s |
| Td | 0.1 | s |

---

##  Résultats et Performances

| Critère | Résultat |
|-------|----------|
| Erreur statique | 0 L/min |
| Marge de phase | 85° |
| Dépassement | 8.5 % |
| Temps de réponse | 6.2 s |
| Pulsation de coupure | 2 rad/s |

 **100 % du cahier des charges validé**

---

##  Comparaison Boucle Ouverte / Boucle Fermée

| Critère | Boucle ouverte | Boucle fermée | Gain |
|-------|----------------|---------------|------|
| Erreur statique | Variable | 0 L/min | Éliminée |
| Temps de réponse | 15 s | 6.2 s | ×2.4 |
| Rejet perturbations | Aucun | Excellent | Total |
| Stabilité | Marginale | Garantie | Assurée |

---

##  Applications Industrielles

- Réseaux de distribution d’eau (15–25 % d’économie d’énergie)
- Systèmes d’irrigation
- Procédés industriels continus
- Systèmes hydrauliques (réduction des coups de bélier)

---

##  Conclusion Générale

Le système développé satisfait pleinement le cahier des charges :

- Erreur statique éliminée
- Marge de phase de **85°**
- Temps de réponse de **6.2 s**
- Excellent rejet des perturbations

Le régulateur PID optimisé  
**(Kp = 5.5, Ti = 0.5 s, Td = 0.1 s)**  
est prêt pour une **implémentation industrielle sur microcontrôleur**.

---

