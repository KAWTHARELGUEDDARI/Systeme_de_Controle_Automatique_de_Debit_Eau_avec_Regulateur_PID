# Système PID de Contrôle d'Humidité du Sol

** Établissement** : ENSAF
** Année académique** : 2025-2026
** Professeur** : HICHAM BELEKBIR 
** Groupe** : GRP7 (Nada Fri , EL GUEDDARI Kawthar , Aya El Bouazzaoui  )

## Table des matières

- [Introduction](#-introduction)
- [Objectifs du projet](#-objectifs-du-projet)
- [Architecture matérielle](#-architecture-matérielle)
- [Le contrôleur PID](#-le-contrôleur-pid)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Résultats et analyses](#-résultats-et-analyses)
- [Vidéo de démonstration](#-vidéo-de-démonstration)
- [Membres de l'équipe](#-membres-de-léquipe)
- [Documentation complète](#-documentation-complète)

---

##  Introduction

Ce projet implémente un **système automatique de contrôle d'humidité du sol** utilisant un régulateur **PID (Proportionnel-Intégral-Dérivé)**. L'objectif principal est de maintenir l'humidité du sol à une valeur de consigne réglable, en activant une pompe d'arrosage de manière intelligente et optimisée.

### Pourquoi un PID ?

Contrairement à un simple système ON/OFF qui créerait des oscillations importantes, le PID permet une **régulation douce et précise**, en anticipant les variations et en corrigeant les erreurs accumulées dans le temps.

---

## Objectifs du projet

-  Maintenir l'humidité du sol à une consigne réglable (30% - 80%)
-  Implémenter un contrôleur PID pour une régulation optimale
-  Afficher en temps réel les paramètres sur écran LCD
-  Analyser les performances avec différents paramètres Kp, Ki, Kd
-  Optimiser les paramètres PID pour une réponse rapide et stable

---

## Architecture matérielle

### Composants utilisés

| Composant                     | Fonction                         | Connexion                |
|------------------------------|-----------------------------------|--------------------------|
| Arduino UNO                  | Microcontrôleur principal         | —                        |
| Capteur d'humidité capacitif | Mesure l'humidité du sol          | Pin A0                   |
| Potentiomètre                | Réglage de la consigne            | Pin A1                   |
| Écran LCD 16x2               | Affichage des données             | Pins 12, 11, 5, 4, 3, 2  |
| Module relais                | Commande de la pompe              | Pin 7                    |
| Pompe d'arrosage             | Arrosage automatique              | Via relais               |


### Schéma de connexion

```
Arduino UNO
├── A0 ← Capteur d'humidité
├── A1 ← Potentiomètre (consigne)
├── D7 → Module relais → Pompe
└── D12, D11, D5, D4, D3, D2 → LCD 16x2
```

##  Le contrôleur PID

### Principe fondamental

Le régulateur PID calcule une commande basée sur **trois termes distincts** :

**Sortie PID = Kp × Erreur + Ki × Intégrale + Kd × Dérivée**

### Les trois termes expliqués

#### 1️ **Terme Proportionnel (P)** - *La réaction immédiate*
- **Kp = 3.0** dans notre implémentation
- Réagit directement à l'écart entre consigne et mesure
- Plus l'écart est grand, plus la correction est forte
- **Exemple** : Si consigne = 60% et mesure = 40%, contribution P = 3.0 × 20 = 60

#### 2️ **Terme Intégral (I)** - *L'élimination de l'erreur résiduelle*
- **Ki = 0.5** dans notre implémentation
- Accumule les erreurs passées au fil du temps
- Force le système à corriger complètement l'erreur
- **Anti-windup** : Limitation entre -100 et +100 pour éviter l'emballement

#### 3️ **Terme Dérivé (D)** - *L'anticipation et la stabilité*
- **Kd = 1.0** dans notre implémentation
- Calcule la vitesse de changement de l'erreur
- Freine le système pour éviter les dépassements
- Agit comme un "amortisseur" contre les oscillations

### Logique de commande

La pompe s'active si :
-  Sortie PID > 0 **ET**
-  Humidité < Consigne - 3%

Cette **hystérésis de 3%** évite les commutations trop fréquentes du relais.

---

##  Installation

### 1. Prérequis

**Arduino :**
- Arduino IDE 1.8.x ou supérieur
- Bibliothèque `LiquidCrystal` (incluse par défaut)

**Python :**
```bash
pip install numpy matplotlib scipy
```

### 2. Installation du code Arduino

1. Ouvrir `code/arduino/control_pid_humidite.ino` dans l'Arduino IDE
2. Sélectionner la carte : **Tools → Board → Arduino UNO**
3. Sélectionner le port série approprié
4. Téléverser le code (Ctrl+U)

---

## Utilisation

### Code Arduino

Une fois téléversé, le système :
1. Affiche "Système PID - Démarrage..." pendant 2 secondes
2. Lit en continu l'humidité du capteur
3. Lit la consigne du potentiomètre
4. Calcule la sortie PID
5. Active/désactive la pompe selon la logique
6. Affiche sur LCD :
   - **Ligne 1** : `H:XX.X% SP:XX%` (Humidité et Setpoint)
   - **Ligne 2** : `PID:XX.X ON/OFF` (Sortie PID et état pompe)

### Code Python - Analyse et optimisation

```bash
cd code/python
python analyse_pid.py
```

**Menu interactif :**
```
[1] Optimiser automatiquement (trouver Kp, Ki, Kd optimaux)
[2] Tester configuration actuelle (3.0, 0.5, 1.0)
[3] Tester configuration personnalisée
[4] Comparer plusieurs configurations
[5] Quitter
```

**Fonctionnalités :**
- Simulation du système avec différents paramètres PID
- Optimisation automatique des paramètres (algorithme L-BFGS-B)
- Génération de graphes d'analyse
- Calcul des métriques de performance :
  - Temps de réponse (95% de la consigne)
  - Dépassement maximum (overshoot)
  - Erreur quadratique moyenne
  - Oscillations (variance)

---

## Résultats et analyses

### Performances du système

Avec les paramètres **Kp = 3.0, Ki = 0.5, Kd = 1.0** :

| Métrique                      | Valeur        |
|-------------------------------|---------------|
| Temps de réponse              | 3–5 minutes   |
| Dépassement                   | < 5 %         |
| Précision en régime stable    | ± 2 %         |
| Temps de stabilisation        | < 10 minutes  |


### Graphes d'analyse

Les graphes d'analyse détaillés des paramètres Kp, Ki, Kd se trouvent dans le dossier [`results/graphes/`](results/graphes/) :

- **Influence du terme Proportionnel (Kp)**
- **Influence du terme Intégral (Ki)**
- **Influence du terme Dérivé (Kd)**
- **Comparaison des configurations**

> **Note :** Les interprétations détaillées de ces graphes sont disponibles dans [`results/interpretations/`](results/interpretations/)

### Graphe PID complet

Le graphe montrant la réponse complète du système PID est disponible dans [`results/graphe-pid/`](results/graphe-pid/)

---

## Vidéo de démonstration

Une vidéo explicative complète du projet est disponible ici :

> **Lien vers la vidéo** : [`media/README.md`](media/) 

---

## Membres de l'équipe

Ce projet a été réalisé par une équipe de 3 étudiants :

| Membre                     |
|----------------------------|
| Nada Fri                   |
| EL GUEDDARI Kawthar        |
| Aya El Bouazzaoui          |


## Licence

Ce projet est développé dans un cadre académique.

---

## Analyse et résultats
1. **Graphes d'analyse Kp/Ki/Kd** →  dans `results/graphes/`
2. **Interprétations** → dans `results/interpretations/`
3. **Graphe PID** →  dans `results/graphe-pid/`
4. **Vidéo** → dans `media/` 

---


