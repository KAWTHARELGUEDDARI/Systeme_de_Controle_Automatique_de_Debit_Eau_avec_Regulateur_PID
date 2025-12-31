# Schéma Bloc PID

##  Description du Système

Ce diagramme représente un *système de contrôle en boucle fermée* pour la régulation automatique de l'humidité du sol à l'aide d'un *régulateur PID (Proportionnel-Intégral-Dérivé)* implémenté sur Arduino.

---

##  Composants du Schéma

### *1. Consigne d'entrée - R(s)*
- *Signal* : Consigne d'humidité (Setpoint)
- *Valeur* : 30-80% (réglable par potentiomètre)
- *Représentation* : Ligne humidité (potentiomètre)
- *Fonction* : Valeur cible que le système doit atteindre

### *2. Comparateur (Cercle ⊕)*
- *Opération* : E(s) = R(s) - B(s)
- *Fonction* : Calcule l'erreur entre la consigne et la mesure
- *Sortie* : Signal d'erreur E(s)
- *Symbole* : 
  - + : Entrée de référence (setpoint)
  - - : Retour de mesure (feedback)

### *3. Contrôleur PID Arduino (Rouge)*
- *Paramètres* : Kp=3, Ki=0.5, Kd=1
- *Entrée* : Erreur E(s)
- *Sortie* : Commande U(s)
- *Équation* : 
  
  U(s) = Kp·E(s) + Ki·∫E(s)dt + Kd·dE(s)/dt
  
- *Rôle* : Calcule la commande optimale pour corriger l'erreur

### *4. Plant P(s) - Système Physique (Violet)*
- *Composants* : Sol + Pompe + Tuyau
- *Entrée* : Commande U(s) du PID
- *Sortie* : Humidité réelle Y(s)
- *Fonction* : Représente la dynamique du système d'arrosage
- *Comportement* : 
  - Pompe ON → Humidité augmente
  - Évaporation → Humidité diminue

### *5. Capteur d'Humidité H(s) (Orange)*
- *Type* : Capteur capacitif
- *Entrée* : Humidité réelle Y(s) du sol
- *Sortie* : Signal électrique B(s) vers Arduino
- *Conversion* : 0-100% → 0-1023 (valeur analogique A0)
- *Fonction* : Mesure l'état actuel du système

### *6. Sortie - Humidité du Sol (Vert)*
- *Variable* : Y(s)
- *Plage* : 0-100%
- *État désiré* : Y(s) = R(s)
- *Affichage* : LCD et Arduino A0 (0-1023)

---

##  Principe de Fonctionnement

### *Boucle de Régulation :*


1. CONSIGNE (R) → Utilisateur règle le setpoint (ex: 60%)
                  ↓
2. COMPARATEUR  → Calcule E(s) = R(s) - B(s)
                  Exemple : 60% - 45% = +15% (erreur)
                  ↓
3. PID          → Calcule la commande U(s)
                  P = 3×15 = 45
                  I = accumulation
                  D = variation
                  U(s) = 45 + I + D
                  ↓
4. SYSTÈME      → Pompe s'active si U(s) > 0
                  Humidité monte progressivement
                  ↓
5. CAPTEUR      → Mesure nouvelle humidité Y(s) = 50%
                  Convertit en signal B(s)
                  ↓
6. RETOUR       → B(s) retourne au comparateur
                  Nouvelle erreur : 60% - 50% = +10%
                  ↓
   BOUCLE SE RÉPÈTE jusqu'à Y(s) ≈ R(s)


---

## Signaux du Système

| Signal | Nom | Description | Unité | Exemple |
|--------|-----|-------------|-------|---------|
| *R(s)* | Référence | Consigne d'humidité (Setpoint) | % | 60% |
| *E(s)* | Erreur | Écart entre consigne et mesure | % | +15% |
| *U(s)* | Commande | Sortie du PID vers système | - | +45.3 |
| *Y(s)* | Sortie | Humidité réelle du sol | % | 45% |
| *B(s)* | Retour | Mesure du capteur | % | 45% |
| *C(s)* | Contrôleur | Fonction de transfert PID | - | PID |

---

##  Équations du Système

### *1. Erreur :*

E(s) = R(s) - B(s)

- Si E(s) > 0 → Sol trop sec → Arroser
- Si E(s) < 0 → Sol trop humide → Arrêter

### *2. Commande PID :*

U(s) = C(s) × E(s)

Où C(s) = Kp + Ki/s + Kd·s


*Forme temporelle :*

u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt


### *3. Système Physique :*

Y(s) = P(s) × U(s)

- P(s) = Fonction de transfert du système (sol + pompe)

### *4. Capteur :*

B(s) = H(s) × Y(s)

- Dans notre cas : H(s) = 1 (capteur parfait, pas de dynamique)

### *5. Boucle Fermée Complète :*

Y(s)/R(s) = [C(s)·P(s)] / [1 + C(s)·P(s)·H(s)]


---

## 🔧 Paramètres de Réglage

### *Gains du PID :*
| Paramètre | Valeur | Rôle | Impact si augmenté |
|-----------|--------|------|-------------------|
| *Kp* | 3.0 | Réactivité | Réponse plus rapide, risque d'oscillations |
| *Ki* | 0.5 | Précision | Élimine erreur résiduelle, risque dépassement |
| *Kd* | 1.0 | Stabilité | Réduit oscillations, sensible au bruit |

### *Autres Paramètres :*
- *Période d'échantillonnage* : 0.3 secondes (300 ms)
- *Hystérésis* : ±3% autour du setpoint
- *Anti-windup* : Intégrale limitée à ±100

---

## Analyse du Système

### *Type de Système :*
- *Ordre* : 1er ordre (approximation)
- *Stabilité* : Stable avec les paramètres choisis
- *Précision* : ±2% en régime permanent

### *Performances Typiques :*
- *Temps de réponse (95%)* : 3-5 minutes
- *Dépassement* : < 5%
- *Erreur statique* : 0% (grâce au terme I)
- *Oscillations* : Minimales (grâce au terme D)

### *Avantages de la Boucle Fermée :*
 *Auto-correction* : S'adapte aux perturbations (pluie, évaporation)
 *Précision* : Atteint exactement la consigne
 *Robustesse* : Fonctionne malgré variations du sol
 *Stabilité* : Pas d'oscillations grâce au PID