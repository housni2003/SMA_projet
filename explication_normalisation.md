# Explication du fonctionnement de la normalisation

## 1. Pourquoi la valeur brute seule ($\text{MaxMaxIdle}$) est-elle trompeuse ?

Imaginons que l'on compare 4 agents et 64 agents sur le même terrain de 400 cases ($n = 400$) :
* Avec **4 agents**, il y a 1 agent pour **100 cases**.
* Avec **64 agents**, il y a 1 agent pour **6,25 cases**.

Il est évident qu'avec 16 fois plus d'agents, la valeur brute de l'oisiveté ($\text{MaxMaxIdle}$) sera plus petite avec 64 agents qu'avec 4 agents. 

Mais la vraie question scientifique est : **Est-ce que cette baisse est due au fait que la stratégie est efficace, ou simplement au fait qu'on a mis "plus de bras" sur le terrain ?**

C'est là qu'intervient la **normalisation**.

---

## 2. La formule de normalisation

$$\overline{\text{MaxMaxIdle}}(G) = \left( \frac{m}{n} \right) \times \text{MaxMaxIdle}(G)$$

Où :
* $m$ = Nombre d'agents patrouilleurs (ex: 4, 16, 64)
* $n$ = Nombre total de cases dans le graphe ($20 \times 20 = 400$)
* $\frac{m}{n}$ = **La densité d'agents par case** (ratio de ressources)
* $\text{MaxMaxIdle}(G)$ = L'oisiveté maximale brute mesurée (en ticks)

---

## 3. L'interprétation théorique (L'optimum idéal)

Dans un monde théorique idéal (où $m$ agents se répartissent parfaitement sur $n$ cases sans jamais se croiser ni perdre de temps) :
* Le temps qu'il faut pour visiter toutes les cases est proportionnel à $\frac{n}{m}$.
* Donc, l'oisiveté idéale théorique est :
  $$\text{Idle}_{\text{idéal}} \approx \frac{n}{m}$$

Si on calcule le ratio entre l'oisiveté brute mesurée $\text{MaxMaxIdle}(G)$ et l'oisiveté idéale $\frac{n}{m}$, on obtient :

$$\text{Facteur d'inefficacité} = \frac{\text{MaxMaxIdle}(G)}{\left(\frac{n}{m}\right)} = \left( \frac{m}{n} \right) \times \text{MaxMaxIdle}(G) = \overline{\text{MaxMaxIdle}}(G)$$

> [!NOTE]
> **Ce que mesure la valeur normalisée $\overline{\text{MaxMaxIdle}}(G)$** :
> Elle mesure le **surcoût / le facteur de dérive de l'algorithme par rapport à l'optimum théorique**. Plus cette valeur est petite, plus la stratégie utilise efficacement les agents à disposition.

---

## 4. Exemple concret à partir de nos résultats

Prenons les chiffres du tableau pour comparer ce que révèle la normalisation :

### A. Stratégie Aléatoire
* **$m = 4$** : $\text{MaxMaxIdle} = 1989 \implies \overline{\text{MaxMaxIdle}} = \frac{4}{400} \times 1989 = \mathbf{19{,}89}$
* **$m = 16$** : $\text{MaxMaxIdle} = 745 \implies \overline{\text{MaxMaxIdle}} = \frac{16}{400} \times 745 = \mathbf{29{,}80}$
* **$m = 64$** : $\text{MaxMaxIdle} = 205 \implies \overline{\text{MaxMaxIdle}} = \frac{64}{400} \times 205 = \mathbf{32{,}80}$

👉 **Constat** : Bien que la valeur brute diminue ($1989 \to 745 \to 205$), la valeur normalisée **augmente** ($19,89 \to 29,80 \to 32,80$). 
**Signification** : Ajouter des agents aléatoires est **inefficace** (rendement décroissant). Les agents supplémentaires se marchent sur les pieds et s'entassent au centre, dégradant la performance *par agent*.

---

### B. Stratégie Heuristique Locale
* **$m = 4$** : $\text{MaxMaxIdle} = 26 \implies \overline{\text{MaxMaxIdle}} = \frac{4}{400} \times 26 = \mathbf{4{,}16}$
* **$m = 16$** : $\text{MaxMaxIdle} = 97 \implies \overline{\text{MaxMaxIdle}} = \frac{16}{400} \times 97 = \mathbf{3{,}88}$
* **$m = 64$** : $\text{MaxMaxIdle} = 26 \implies \overline{\text{MaxMaxIdle}} = \frac{64}{400} \times 26 = \mathbf{4{,}16}$

👉 **Constat** : La valeur normalisée reste **quasiment constante ($\approx 4$)**.
**Signification** : L'heuristique tire un profit **parfaitement linéaire** de chaque agent supplémentaire. Multiplier le nombre d'agents par 4 permet d'augmenter la couverture d'un facteur 4 sans gaspillage de ressources.
