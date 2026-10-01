# Préparation à l'Oral — Projet SMA : Patrouille Multi-Agents

* **Binôme :** RAKOTOARISOA Housni & Cédric
* **Matière :** Systèmes Multi-Agents (SMA) — 5A FISE/FISA
* **Enseignant :** Maxime MORGE
* **Fichiers sources du projet :** 
  * Modèle NetLogo : `TT.nlogox`
  * Rapport d'expérimentation : `compte_rendu.md`
  * Script d'analyse graphique : `generer_graphes.py`
  * Données brutes BehaviorSpace : `experiment_table`

---

## 1. Le Pitch Oral en 1 minute (Introduction)

> *"L'objectif de notre projet est d'étudier le **problème de la patrouille multi-agents** sur une grille 2D fermée de 400 cases ($20 \times 20$) non torique. Le but est de minimiser l'**oisiveté** des tuiles, c'est-à-dire le temps pendant lequel une case reste sans visite.*  
> 
> *Nous avons implémenté et comparé trois stratégies :*
> 1. ***Réactif Aléatoire*** *(marche brownienne discrète)*,
> 2. ***Réactif Heuristique locale*** *(gradient d'oisiveté à 1 pas)*,
> 3. ***Cognitif*** *(planification globale basée sur une fonction d'utilité $Gain - Coût$).*  
> 
> *Le résultat central du projet illustre un principe fondamental des systèmes multi-agents :*  
> * *Pour **1 agent unique**, l'approche **cognitive** est la meilleure car elle évite d'errer sans but.*  
> * *Mais dès qu'on **augmente le nombre d'agents ($m \ge 8, 16, 64$)**, le comportement cognitif s'effondre à cause d'un **effet de troupeau (*herding effect*)** dû à l'absence de coordination sociale.*  
> * *À l'inverse, l'**heuristique locale** surclasse tout le monde à grande échelle grâce à un phénomène d'**auto-organisation par stigmergie répulsive**, sans aucun échange de messages."*

---

## 2. Environnement et Formules Théoriques

### A. L'Environnement
* **Taille :** Grille de $20 \times 20$ tuiles $\implies n = 400$ tuiles.
* **Topologie :** **Non torique** (les bords et coins ne rebouclent pas).
* **Voisinage :** 4-voisinage (`neighbors4`) — déplacements orthogonaux (Nord, Sud, Est, Ouest).

### B. Les Métriques d'Oisiveté (*Idleness*)
* **$Idle_t(i)$ :** Temps écoulé (en ticks) depuis la dernière visite d'un agent sur la tuile $i$. À $t=0$, $Idle_0(i) = 0$. À chaque pas, toutes les tuiles s'incrémentent de $+1$. Lorsqu'un patrouilleur marche dessus, son oisiveté retombe immédiatement à $0$.
* **$MaxIdle_t(G) = \max_{i \in V} Idle_t(i)$ :** Oisiveté de la case la plus délaissée à l'instant précis $t$.
* **$MaxMaxIdle(G) = \max_{t \le t_f} MaxIdle_t(G)$ :** Le pire temps d'attente absolu enregistré sur toute la simulation ($3\,000$ ticks).

### C. La Normalisation : Pourquoi et Comment ?

$$\widehat{\text{MaxMaxIdle}}(G) = \left(\frac{m}{n}\right) \times \text{MaxMaxIdle}(G)$$

* **Pourquoi la valeur brute est trompeuse :**  
  Avec 64 agents, il y a 1 agent pour 6,25 cases, contre 1 agent pour 100 cases à 4 agents. La valeur brute chute forcément, simplement parce qu'on a mis "plus de bras".
* **L'explication mathématique :**  
  Dans un système parfait théorique sans collision ni recouvrement, chaque case recevrait une visite tous les $\frac{n}{m}$ ticks.  
  Le critère normalisé calcule le ratio entre la réalité observée et l'idéal théorique :
  $$\text{Facteur d'inefficacité} = \frac{\text{MaxMaxIdle}(G)}{\left(\frac{n}{m}\right)} = \left(\frac{m}{n}\right) \times \text{MaxMaxIdle}(G)$$
* **Interprétation :**  
  * Si la courbe normalisée est **plate** : l'ajout d'agents apporte un gain d'efficacité parfaitement proportionnel (scalabilité idéale).
  * Si la courbe normalisée **monte** : les agents se gênent et font du travail redondant.

---

## 3. Données Expérimentales (30 runs BehaviorSpace)

Tableau des résultats moyens ($\pm$ écart-type) calculés sur 30 exécutions par configuration pour $t_f = 3\,000$ ticks :

| Stratégie       | Nb agents ($m$) | Ratio $m/n$ | $MaxMaxIdle$ brut (ticks) | $\widehat{MaxMaxIdle}$ normalisé | Diagnostic                      |
| :-------------- | :-------------: | :---------: | :-----------------------: | :------------------------------: | :------------------------------ |
| **Aléatoire**   |        1        |   0,0025    |  $3\,000{,}0 \pm 0{,}0$   |     **$7{,}50 \pm 0{,}00$**      | Échec complet d'exploration     |
| **Heuristique** |        1        |   0,0025    | $1\,232{,}5 \pm 137{,}0$  |     **$3{,}08 \pm 0{,}34$**      | Acceptable                      |
| **Cognitif**    |        1        |   0,0025    | **$519{,}6 \pm 15{,}1$**  |     **$1{,}30 \pm 0{,}04$**      | **Meilleur résultat à 1 agent** |
| **Aléatoire**   |        2        |   0,0050    |  $2\,972{,}1 \pm 84{,}4$  |     **$14{,}86 \pm 0{,}42$**     | Dérive rapide                   |
| **Heuristique** |        2        |   0,0050    |   $671{,}2 \pm 85{,}9$    |     **$3{,}36 \pm 0{,}43$**      | Stable                          |
| **Cognitif**    |        2        |   0,0050    | **$475{,}3 \pm 47{,}6$**  |     **$2{,}38 \pm 0{,}24$**      | Bon                             |
| **Aléatoire**   |        4        |   0,0100    | $2\,230{,}8 \pm 400{,}1$  |     **$22{,}31 \pm 4{,}00$**     | Inefficace                      |
| **Heuristique** |        4        |   0,0100    | **$340{,}0 \pm 31{,}3$**  |     **$3{,}40 \pm 0{,}31$**      | Stable                          |
| **Cognitif**    |        4        |   0,0100    |   $375{,}0 \pm 40{,}8$    |     **$3{,}75 \pm 0{,}41$**      | Début de dépassement            |
| **Aléatoire**   |        8        |   0,0200    | $1\,443{,}2 \pm 314{,}0$  |     **$28{,}86 \pm 6{,}28$**     | Mauvais                         |
| **Heuristique** |        8        |   0,0200    | **$174{,}8 \pm 16{,}1$**  |     **$3{,}50 \pm 0{,}32$**      | Stable                          |
| **Cognitif**    |        8        |   0,0200    |   $303{,}7 \pm 27{,}6$    |     **$6{,}07 \pm 0{,}55$**      | Dégradation nette               |
| **Aléatoire**   |       16        |   0,0400    |   $779{,}4 \pm 145{,}4$   |     **$31{,}18 \pm 5{,}82$**     | Fort gaspillage                 |
| **Heuristique** |       16        |   0,0400    |  **$87{,}4 \pm 6{,}1$**   |     **$3{,}50 \pm 0{,}24$**      | Quasi parfait                   |
| **Cognitif**    |       16        |   0,0400    |   $252{,}8 \pm 28{,}2$    |     **$10{,}11 \pm 1{,}13$**     | Chute des performances          |
| **Aléatoire**   |       32        |   0,0800    |   $458{,}7 \pm 83{,}2$    |     **$36{,}70 \pm 6{,}65$**     | Rendement décroissant           |
| **Heuristique** |       32        |   0,0800    |  **$46{,}1 \pm 5{,}2$**   |     **$3{,}69 \pm 0{,}42$**      | Linéarité confirmée             |
| **Cognitif**    |       32        |   0,0800    |   $224{,}0 \pm 22{,}6$    |     **$17{,}92 \pm 1{,}81$**     | Effet troupeau sévère           |
| **Aléatoire**   |       64        |   0,1600    |   $235{,}5 \pm 52{,}3$    |     **$37{,}67 \pm 8{,}37$**     | Très mauvais rendement          |
| **Heuristique** |       64        |   0,1600    |  **$27{,}4 \pm 2{,}8$**   |     **$4{,}38 \pm 0{,}44$**      | **Champion absolu à 64 agents** |
| **Cognitif**    |       64        |   0,1600    |   $204{,}8 \pm 18{,}1$    |     **$32{,}77 \pm 2{,}89$**     | Naufrage collectif              |

---

## 4. Analyse des Stratégies et Extraits de Code NetLogo

### 1. Comportement Réactif Aléatoire

```netlogo
to comportement-reactif-aleatoire
  let voisins neighbors4
  if any? voisins [
    let cible one-of voisins
    face cible
    move-to cible
    reinitialiser-oisivete-courante
  ]
end
```

* **Principe :** Déplacement arbitraire uniforme vers un voisin orthogonal.
* **Problème du piégeage topologique :**  
  Sur une grille non torique, les coins ont 2 voisins, les bords 3 voisins et les cases intérieures 4 voisins. Une chaîne de Markov montre que les probabilités stationnaires favorisent massivement le centre. L'agent aléatoire y reste piégé, et les coins restent oubliés pendant des centaines voire milliers de pas ($MaxMaxIdle = 3000$ à $m=1$).

---

### 2. Comportement Réactif Heuristique Locale (Le Champion)

```netlogo
to comportement-reactif-heuristique
  let voisins neighbors4
  if any? voisins [
    ; Choix du voisin avec l'oisiveté maximale
    let cible max-one-of voisins [ oisivete ]
    face cible
    move-to cible
    reinitialiser-oisivete-courante
  ]
end
```

* **Principe :** Décision purement locale à 1 pas d'anticipation ($\mathcal{O}(1)$).
* **Mécanisme clé : Stigmergie Répulsive Décentralisée :**  
  * Aucun message explicite n'est envoyé entre patrouilleurs.
  * Lorsqu'un agent visite une tuile, il remet son oisiveté à 0 : il crée une **zone froide**.
  * Un agent voisin inspectant ses tuiles adjacentes est naturellement attiré par les **zones chaudes** (forte oisiveté) et repoussé loin des zones froides.
  * **Auto-organisation spatiale :** Les agents se repoussent mutuellement et couvrent toute la grille sans redondance. La métrique normalisée reste remarquable de stabilité autour de $\approx 3{,}5 - 4{,}4$.

---

### 3. Comportement Cognitif ($Gain - Coût$)

```netlogo
to comportement-cognitif
  ; 1. Sélection de la tuile maximisant l'utilité U = gain - coût
  let cible max-one-of patches [ gain - cout ]
  
  ; 2. Calcul du pas optimal vers la cible
  let prochain-pas bfs-to cible
  
  ; 3. Déplacement
  if prochain-pas != nobody [
    face prochain-pas
    move-to prochain-pas
  ]
  
  ; 4. Réinitialisation de la tuile atteinte
  reinitialiser-oisivete-courante
end

to calculer-utilite [ agent-cible ]
  ask patches [
    set gain oisivete
    set cout distance agent-cible
  ]
end

to-report bfs-to [ destination ]
  if patch-here = destination [
    report destination
  ]
  ; Sélectionne le voisin orthogonal qui minimise la distance à la cible
  report min-one-of neighbors4 [ distance destination ]
end
```

* **Principe :** Perception globale. L'agent évalue les 400 cases selon $U(v) = oisivete(v) - distance(agent, v)$, sélectionne la meilleure tuile et s'y dirige.
* **Mécanisme clé : L'Effet de Troupeau (*Herding Effect*) :**  
  * À $m=1$, c'est la meilleure stratégie ($519{,}6$ ticks) car l'agent ne tourne pas en rond.
  * Dès que $m$ augmente, tous les agents ont la même fonction d'utilité et la même vue du monde. **Ils choisissent tous la même case la plus en retard en même temps**.
  * Ils se déplacent en essaim compact. Le premier agent réinitialise l'oisiveté de la cible, et les 63 autres agents ont gaspillé leurs actions. C'est l'illustration type du dilemme : **l'optimum individuel sans coordination sociale aboutit à un échec collectif**.

---

### 4. La Boucle Principale `go` et l'Ordonnancement

```netlogo
to go
  ; 1. Condition d'arrêt
  if ticks >= max_tick [
    stop
  ]
  
  ; 2. Incrémentation de l'oisiveté de toutes les tuiles
  ask patches [
    set oisivete oisivete + 1
    set plabel oisivete
  ]
  
  ; 3. Exécution du comportement
  ifelse strategie = "cognitif" [
    foreach (sort patrouilleurs) [
      patrouilleurCourant ->
      reinitialiser-utilite
      calculer-utilite patrouilleurCourant
      ask patrouilleurCourant [ comportement-cognitif ]
    ]
  ] [
    ask patrouilleurs [ comportement-reactif ]
  ]
  
  ; 4. Mise à jour de MaxMaxIdle
  let max-idle-courant max [oisivete] of patches
  if max-idle-courant > max-max-idle [
    set max-max-idle max-idle-courant
  ]
  
  tick
end
```

---

## 5. Tableau Synthétique Comparatif

| Propriété                         |             Réactif Aléatoire             |           Heuristique Locale           |        Cognitif (Gain - Coût)        |
| :-------------------------------- | :---------------------------------------: | :------------------------------------: | :----------------------------------: |
| **Complexité par agent**          |             $\mathcal{O}(1)$              |            $\mathcal{O}(1)$            |   $\mathcal{O}(n)$ ($400$ tuiles)    |
| **Volume de messages**            |                    Nul                    |            Nul (Stigmergie)            |                 Nul                  |
| **Performance à $m=1$**           |             $3\,000$ (Échec)              |          $1\,232{,}5$ (Moyen)          |      **$519{,}6$ (Excellent)**       |
| **Performance à $m=64$**          |           $235{,}5$ (Médiocre)            |      **$27{,}4$ (Exceptionnel)**       |         $204{,}8$ (Médiocre)         |
| **Scalabilité ($\widehat{MMI}$)** | Dégradation continue ($7{,}5 \to 37{,}7$) | **Optimale ($\approx 3{,}5 - 4{,}4$)** |    Explosion ($1{,}3 \to 32{,}8$)    |
| **Comportement émergent**         |            Errance / Piégeage             |     **Dispersion auto-organisée**      | **Attroupement néfaste (*Herding*)** |

---

## 6. Les 6 Questions Pièges de l'Oral & Réponses Prêtes

### Q1 : *"Pourquoi avoir normalisé par $\frac{m}{n} \times MaxMaxIdle$ et pas juste divisé par $m$ ?"*
> **Réponse :**  
> *"La fréquence théorique idéale de visite dépend à la fois du nombre de patrouilleurs $m$ et du nombre total de cases $n$. Dans un monde théorique sans chevauchement, chaque case est visitée tous les $\frac{n}{m}$ ticks. Diviser l'oisiveté brute mesurée par cet idéal revient mathématiquement à la multiplier par $\frac{m}{n}$ :  
> $\frac{MaxMaxIdle}{\frac{n}{m}} = \frac{m}{n} \times MaxMaxIdle$.  
> C'est une métrique sans dimension qui mesure directement le facteur d'inefficacité par rapport à l'optimum théorique absolu."*

---

### Q2 : *"Pourquoi votre agent cognitif est-il moins bon que l'heuristique à 64 agents ?"*
> **Réponse :**  
> *"À cause de l'**effet de troupeau (*herding effect*)**. Nos agents cognitifs sont purement égocentrés : ils possèdent la même fonction d'utilité et la même perception globale de l'environnement sans communiquer entre eux. Ils ciblent donc tous la même case au même instant et se déplacent en groupe compact, ce qui détruit le parallélisme et la couverture de la patrouille."*

---

### Q3 : *"Comment pourriez-vous corriger ce problème pour l'agent cognitif ?"*
> **Réponse :**  
> *"En introduisant des mécanismes de **coordination multi-agents** :*  
> 1. *Un système de **réservation d'intention** : un agent réserve sa tuile cible, ce qui annule ou réduit fortement son utilité pour les autres patrouilleurs.*  
> 2. *Un **partitionnement spatial** (ex: diagramme de Voronoï ou partitionnement de graphe) : chaque agent gère sa zone cognitivement.*  
> 3. *Une modification de la fonction d'utilité pénalisant une cible si un autre patrouilleur est déjà plus proche d'elle."*

---

### Q4 : *"Est-ce que votre `bfs-to` est un vrai BFS ?"*
> **Réponse :**  
> *"Sur notre grille sans obstacles statiques, `bfs-to` sélectionne le voisin orthogonal minimisant la distance euclidienne à la cible (`min-one-of neighbors4 [distance destination]`). Sur un plan vierge de murs, cela donne exactement la trajectoire du plus court chemin (distance de Manhattan). S'il y avait eu des obstacles statiques ou un labyrinthe, il aurait fallu implémenter une vraie file FIFO d'exploration de graphe."*

---

### Q5 : *"Pourquoi l'heuristique locale fonctionne-t-elle si bien sans communication ?"*
> **Réponse :**  
> *"Parce qu'elle exploite la **stigmergie répulsive**. L'environnement fait office de mémoire partagée. Lorsqu'un agent visite une case, il met son oisiveté à 0 et crée une zone 'froide'. Les patrouilleurs voisins sélectionnent la tuile ayant l'oisiveté maximale et sont donc naturellement repoussés vers les zones 'chaudes' (non visitées). Ce gradient répulsif passif assure une auto-organisation optimale de la flotte sans aucun coût de calcul ni de communication."*

---

### Q6 : *"Comment avez-vous obtenu vos courbes et vos données ?"*
> **Réponse :**  
> *"Nous avons utilisé **BehaviorSpace** sous NetLogo pour lancer une campagne expérimentale systématique. Pour garantir une haute significativité statistique, nous avons réalisé **30 répétitions indépendantes** de 3 000 ticks pour chaque configuration (7 valeurs de $m \in \{1, 2, 4, 8, 16, 32, 64\}$ et 3 stratégies), soit un total de **630 simulations**. Nous avons ensuite traité le fichier d'export avec un script Python (`generer_graphes.py` utilisant Pandas, Matplotlib et Seaborn) pour calculer les moyennes, les écarts-types et tracer les courbes finales."*
