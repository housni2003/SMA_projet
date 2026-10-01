# Explication de la Monotonie de la Courbe Normalisée

Fichier sans aucun code LaTeX, écrit en texte simple pour être lisible dans n'importe quel éditeur.

---

## 1. La Question Posée

> "Est-ce que la courbe normalisée est monotone ?"  
> "Pourquoi normaliser par (m / n) * MaxMaxIdle et pas juste diviser par m ?"

Voici l'explication complète, étape par étape.

---

## 2. Si on avait fait l'erreur de "diviser par m" : (MaxMaxIdle / m)

Si on divisait simplement par m, la courbe serait obligatoirement et strictement monotone décroissante (elle plongerait vers 0) :

* MaxMaxIdle (valeur brute) diminue quand on ajoute des agents.
* m (le nombre d'agents) augmente.
* Donc (MaxMaxIdle / m) est la division d'une valeur qui baisse par une valeur qui monte : elle s'écrase vers 0 à toute vitesse (en 1 / m^2).

Le piège :  
Cette courbe donnerait la fausse illusion que l'algorithme devient fantastique à 64 agents, alors qu'on a simplement divisé par 64 un chiffre qui était déjà petit.

---

## 3. Avec la vraie formule : MaxMaxIdle_normalisé = (m / n) * MaxMaxIdle

Ici, on multiplie une variable qui monte par une variable qui descend :

Formule :
MaxMaxIdle_normalisé = (1 / n) * [ m (qui monte) * MaxMaxIdle (qui descend) ]

Où :
* m = nombre de patrouilleurs (croissant : 1, 2, 4, 8, 16, 32, 64)
* MaxMaxIdle = pire oisiveté brute mesurée (décroissante)
* n = nombre total de tuiles (fixe à 400)

Mathématiquement, le produit d'une valeur qui monte et d'une valeur qui descend n'a AUCUNE OBLIGATION d'être monotone.  
La pente de la courbe dépend du rapport de force entre l'ajout d'agents et le gain de temps :

### Cas 1 : Si MaxMaxIdle baisse PLUS VITE que (1 / m)
* La courbe normalisée DESCEND.
* Signification : Les agents créent une synergie si forte que le gain dépasse la simple addition de moyens.

### Cas 2 : Si MaxMaxIdle baisse EXACTEMENT au même rythme que (1 / m)
* La courbe normalisée est HORIZONTALE (plate / constante).
* Signification : Le passage à l'échelle est parfait. Doubler le nombre d'agents divise exactement le temps d'attente par 2.

### Cas 3 : Si MaxMaxIdle baisse MOINS VITE que (1 / m)
* La courbe normalisée MONTE.
* Signification : Il y a du gaspillage. Les agents supplémentaires se marchent sur les pieds (effet de troupeau ou embouteillage).

---

## 4. Ce que l'on observe concrètement dans nos résultats

Dans nos expériences, nous observons précisément les deux comportements :

### A. Pour l'Heuristique Locale : courbe quasi-plate avec de légères variations (NON MONOTONE)
* Sur un run individuel (Exercice 3 du compte-rendu) :
  * Pour 4 agents   : valeur normalisée = 4.16
  * Pour 16 agents  : valeur normalisée = 3.88   <-- La courbe DESCEND !
  * Pour 64 agents  : valeur normalisée = 4.16   <-- La courbe REMONTE !
  
  Ici, la courbe est clairement NON MONOTONE.  
  Ces petites oscillations sont dues aux conditions de départ (à 16 agents, certains peuvent temporairement suivre la même trace avant de se disperser).

* Sur la moyenne des 30 runs BehaviorSpace :
  * m = 1  : 3.08
  * m = 2  : 3.36
  * m = 4  : 3.40
  * m = 8  : 3.50
  * m = 16 : 3.50
  * m = 32 : 3.69
  * m = 64 : 4.38
  
  La courbe forme un plateau remarquable entre 3.08 et 4.38. Le score reste quasi-constant, preuve d'une scalabilité presque parfaite.

### B. Pour l'Aléatoire et le Cognitif : courbes MONOTONES CROISSANTES
* Dès qu'on ajoute des agents, ils s'entassent (au centre pour l'aléatoire, sur la même cible pour le cognitif).
* MaxMaxIdle ne diminue presque pas, alors que m est multiplié par 2 à chaque étape.
* Par conséquent, le produit m * MaxMaxIdle explose vers le haut :
  * Cognitif : passe de 1.30 (à 1 agent) à 32.77 (à 64 agents).
  * Aléatoire : passe de 7.50 (à 1 agent) à 37.67 (à 64 agents).

---

## 5. La Réponse Prête pour l'Oral

Si le professeur demande :
"Pourquoi la courbe normalisée n'est-elle pas forcément monotone ?"

Votre réponse :
"Multiplier par (m / n) met en compétition deux forces inverses : la hausse du nombre d'agents m et la baisse du temps d'attente MaxMaxIdle.  
La courbe n'a donc aucune contrainte mathématique de monotonie.  
Elle monte quand les agents se gênent comme dans le cognitif (effet de troupeau).  
Elle reste quasi-plate avec de petites fluctuations locales quand le collectif s'auto-organise parfaitement, comme nous l'observons sur l'heuristique locale qui oscille autour de 3.5 à 4.4."
