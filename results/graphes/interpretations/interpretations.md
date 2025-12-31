

Cas 1: Kp faible

Kp = 1.0, Ki = 0.5, Kd = 1.0

**Analyse de la réponse temporelle**

La montée de l’humidité est progressive et relativement lente. Le système met environ 8,4 secondes pour atteindre 95 % de la consigne. La réponse reste toujours en dessous du point de consigne, ce qui montre une correction modérée.

**Dépassement et stabilité**

Aucun dépassement significatif n’est observé (dépassement négatif ≈ -2,9 %). Les oscillations autour de la valeur finale sont faibles, ce qui indique un comportement stable mais peu réactif.

**Sortie du PID**

La sortie PID présente une amplitude modérée, traduisant une commande douce de la pompe. Le contrôleur réagit faiblement aux erreurs, ce qui limite les risques d’instabilité mais ralentit la correction.

**Conclusion**

Un Kp faible rend le système stable mais peu réactif. Ce réglage est sûr mais non optimal lorsque l’on souhaite une réponse rapide.

-----------------------------------------------

Cas 2 — Kp optimal

Kp = 3.0, Ki = 0.5, Kd = 1.0

**Analyse de la réponse temporelle**

L’humidité atteint rapidement la consigne avec un temps de réponse similaire, mais la montée est plus dynamique. Le système se rapproche efficacement du point de consigne sans retard notable.

**Dépassement et stabilité**

Le dépassement reste très faible et contrôlé. Les oscillations sont limitées et régulières, ce qui montre un bon compromis entre rapidité et stabilité.

**Sortie du PID**

La sortie PID est plus énergique au démarrage, puis se stabilise. Cela montre que le contrôleur corrige efficacement l’erreur initiale avant de maintenir le régime permanent.

**Conclusion**

Ce réglage représente un bon compromis entre rapidité, stabilité et précision. Il correspond à une configuration proche de l’optimum pour ce système.

-----------------------------------------------

Cas 3 — Ki élevé

Kp = 3.0, Ki = 2.0, Kd = 1.0

**Analyse de la réponse temporelle**

La montée vers la consigne est rapide, mais le système montre une tendance à maintenir une action de correction importante même lorsque l’erreur est faible.

**Dépassement et stabilité**

Bien que le dépassement reste limité, les oscillations persistent légèrement autour de la consigne. Cela est dû à l’accumulation de l’erreur intégrale.

**Sortie du PID**

La sortie PID est nettement plus élevée en régime permanent. Le terme intégral dominant provoque une correction excessive, augmentant le risque de windup.

**Conclusion**

Un Ki trop élevé améliore la correction de l’erreur statique mais dégrade la stabilité. Il peut entraîner des oscillations et une sollicitation excessive de l’actionneur.

-----------------------------------------------

**Conclusion générale**

Chaque paramètre PID joue un rôle spécifique :

* Kp agit sur la rapidité de réaction
* Ki élimine l’erreur statique mais peut provoquer des oscillations
* Kd améliore la stabilité et l’amortissement

Le réglage Kp = 3.0, Ki = 0.5, Kd = 1.0 offre le meilleur compromis global pour ce système d’arrosage automatique.
