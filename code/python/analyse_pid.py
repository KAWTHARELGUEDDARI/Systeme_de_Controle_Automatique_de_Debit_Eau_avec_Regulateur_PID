import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ========== SIMULATION DU SYSTÈME ==========
class SystemeArrosage:
    def __init__(self):
        self.humidite = 20.0  # État initial (sol sec)
        self.debit_pompe = 5.0  # %/seconde quand pompe ON
        self.evaporation = 0.5  # %/seconde (perte naturelle)
        
    def step(self, pompe_on, dt=0.3):
        """Simule une étape du système"""
        if pompe_on:
            self.humidite += self.debit_pompe * dt
        self.humidite -= self.evaporation * dt
        self.humidite = np.clip(self.humidite, 0, 100)
        return self.humidite

# ========== CONTRÔLEUR PID ==========
class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integrale = 0
        self.erreur_precedente = 0
        
    def compute(self, setpoint, mesure, dt):
        erreur = setpoint - mesure
        
        # Terme P
        P = self.Kp * erreur
        
        # Terme I avec anti-windup
        self.integrale += erreur * dt
        self.integrale = np.clip(self.integrale, -100, 100)
        I = self.Ki * self.integrale
        
        # Terme D
        derivee = (erreur - self.erreur_precedente) / dt
        D = self.Kd * derivee
        
        self.erreur_precedente = erreur
        
        sortie = P + I + D
        return sortie, P, I, D

# ========== FONCTION DE SIMULATION ==========
def simuler_pid(Kp, Ki, Kd, setpoint=60, duree=60, dt=0.3, afficher=False):
    """Simule le système avec des paramètres PID donnés"""
    
    systeme = SystemeArrosage()
    pid = PID(Kp, Ki, Kd)
    
    temps = np.arange(0, duree, dt)
    humidite_log = []
    sortie_pid_log = []
    
    for t in temps:
        # Mesure actuelle
        humidite = systeme.humidite
        humidite_log.append(humidite)
        
        # Calcul PID
        sortie_pid, P, I, D = pid.compute(setpoint, humidite, dt)
        sortie_pid_log.append(sortie_pid)
        
        # Décision pompe (avec hystérésis)
        pompe_on = (sortie_pid > 0) and (humidite < setpoint - 3)
        
        # Mise à jour système
        systeme.step(pompe_on, dt)
    
    # ========== CALCUL DES MÉTRIQUES ==========
    humidite_log = np.array(humidite_log)
    
    # 1. Temps pour atteindre 95% de la consigne
    seuil = setpoint * 0.95
    idx_atteint = np.where(humidite_log >= seuil)[0]
    temps_reponse = temps[idx_atteint[0]] if len(idx_atteint) > 0 else duree
    
    # 2. Dépassement maximum
    depassement = np.max(humidite_log - setpoint)
    depassement_pourcent = (depassement / setpoint) * 100
    
    # 3. Erreur quadratique moyenne (après stabilisation)
    idx_stable = int(len(temps) * 0.7)  # Derniers 30%
    erreur_stable = np.mean((humidite_log[idx_stable:] - setpoint) ** 2)
    
    # 4. Oscillations (variance après stabilisation)
    variance = np.var(humidite_log[idx_stable:])
    
    # Score global (à minimiser)
    score = (temps_reponse * 0.3 +          # Pénalité temps de réponse
             abs(depassement_pourcent) * 2 + # Pénalité dépassement
             erreur_stable * 10 +             # Pénalité erreur
             variance * 5)                    # Pénalité oscillations
    
    if afficher:
        print(f"\n{'='*50}")
        print(f"RÉSULTATS POUR Kp={Kp:.2f}, Ki={Ki:.2f}, Kd={Kd:.2f}")
        print(f"{'='*50}")
        print(f"Temps de réponse (95%) : {temps_reponse:.1f} secondes")
        print(f"Dépassement maximum    : {depassement_pourcent:.1f}%")
        print(f"Erreur stable (MSE)    : {erreur_stable:.2f}")
        print(f"Variance (oscillations): {variance:.2f}")
        print(f"SCORE GLOBAL           : {score:.2f}")
        
        # Graphique
        plt.figure(figsize=(12, 6))
        
        plt.subplot(2, 1, 1)
        plt.plot(temps, humidite_log, 'b-', linewidth=2, label='Humidité')
        plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
        plt.axhline(y=setpoint*0.95, color='g', linestyle=':', alpha=0.5)
        plt.fill_between(temps, setpoint-3, setpoint+3, alpha=0.2, color='green')
        plt.ylabel('Humidité (%)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.title(f'Réponse du système - Kp={Kp:.2f}, Ki={Ki:.2f}, Kd={Kd:.2f}', 
                  fontsize=14, fontweight='bold')
        
        plt.subplot(2, 1, 2)
        plt.plot(temps, sortie_pid_log, 'g-', linewidth=2, label='Sortie PID')
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.xlabel('Temps (s)', fontsize=12)
        plt.ylabel('Sortie PID', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    return score

# ========== OPTIMISATION AUTOMATIQUE ==========
def optimiser_pid():
    """Trouve les meilleures valeurs de Kp, Ki, Kd"""
    
    print("\n" + "="*60)
    print("  OPTIMISATION AUTOMATIQUE DES PARAMÈTRES PID")
    print("="*60)
    
    # Fonction objectif à minimiser
    def objectif(params):
        Kp, Ki, Kd = params
        return simuler_pid(Kp, Ki, Kd, afficher=False)
    
    # Valeurs initiales
    x0 = [2.0, 0.3, 0.5]
    
    # Contraintes (valeurs positives)
    bounds = [(0.1, 10), (0.01, 2), (0.01, 5)]
    
    print("\nRecherche en cours...")
    print("(Cela peut prendre 30-60 secondes)\n")
    
    # Optimisation
    result = minimize(objectif, x0, method='L-BFGS-B', bounds=bounds)
    
    Kp_opt, Ki_opt, Kd_opt = result.x
    
    print("\n" + "="*60)
    print("  VALEURS OPTIMALES TROUVÉES")
    print("="*60)
    print(f"\n  Kp = {Kp_opt:.2f}")
    print(f"  Ki = {Ki_opt:.2f}")
    print(f"  Kd = {Kd_opt:.2f}\n")
    print("="*60)
    
    return Kp_opt, Ki_opt, Kd_opt

# ========== COMPARAISON DE PLUSIEURS CONFIGURATIONS ==========
def comparer_configurations():
    """Compare différentes configurations PID"""
    
    configs = [
        (1.0, 0.5, 1.0, "Kp trop faible"),
        (5.0, 0.5, 1.0, "Kp trop élevé"),
        (3.0, 2.0, 1.0, "Ki trop élevé"),
        (3.0, 0.1, 1.0, "Ki trop faible"),
        (3.0, 0.5, 0.1, "Kd trop faible"),
        (3.0, 0.5, 5.0, "Kd trop élevé"),
        (3.0, 0.5, 1.0, "Configuration actuelle"),
    ]
    
    print("\n" + "="*70)
    print("  COMPARAISON DES CONFIGURATIONS")
    print("="*70)
    print(f"{'Kp':>6} {'Ki':>6} {'Kd':>6} {'Score':>8} {'Description':<25}")
    print("-"*70)
    
    scores = []
    for Kp, Ki, Kd, desc in configs:
        score = simuler_pid(Kp, Ki, Kd, afficher=False)
        scores.append(score)
        print(f"{Kp:>6.1f} {Ki:>6.1f} {Kd:>6.1f} {score:>8.1f} {desc:<25}")
    
    meilleur_idx = np.argmin(scores)
    print("="*70)
    print(f"MEILLEURE CONFIGURATION : {configs[meilleur_idx][3]}")
    print(f"Kp={configs[meilleur_idx][0]:.1f}, Ki={configs[meilleur_idx][1]:.1f}, Kd={configs[meilleur_idx][2]:.1f}")
    print("="*70)

# ========== MENU PRINCIPAL ==========
def main():
    print("\n" + "="*60)
    print("  SIMULATEUR ET OPTIMISEUR PID")
    print("  Système d'arrosage automatique")
    print("="*60)
    
    while True:
        print("\n  MENU :")
        print("  [1] Optimiser automatiquement (trouver Kp, Ki, Kd optimaux)")
        print("  [2] Tester configuration actuelle (3.0, 0.5, 1.0)")
        print("  [3] Tester configuration personnalisée")
        print("  [4] Comparer plusieurs configurations")
        print("  [5] Quitter")
        
        choix = input("\n  Votre choix : ")
        
        if choix == "1":
            Kp_opt, Ki_opt, Kd_opt = optimiser_pid()
            input("\nAppuyez sur Entrée pour voir la simulation...")
            simuler_pid(Kp_opt, Ki_opt, Kd_opt, afficher=True)
            
        elif choix == "2":
            simuler_pid(3.0, 0.5, 1.0, afficher=True)
            
        elif choix == "3":
            try:
                Kp = float(input("  Kp : "))
                Ki = float(input("  Ki : "))
                Kd = float(input("  Kd : "))
                simuler_pid(Kp, Ki, Kd, afficher=True)
            except ValueError:
                print("  Erreur : valeurs invalides")
                
        elif choix == "4":
            comparer_configurations()
            
        elif choix == "5":
            print("\n  Au revoir !\n")
            break
        else:
            print("  Choix invalide")

if __name__ == "__main__":
    main()
