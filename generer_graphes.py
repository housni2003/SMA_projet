import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration du style graphique
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Chargement des données
df = pd.read_csv('experiment_table', skiprows=6)
norm_col = '((count patrouilleurs / count patches) * max-max-idle)'
raw_col = 'max-max-idle'

m_vals = [1, 2, 4, 8, 16, 32, 64]

colors = {
    'aleatoire': '#e74c3c',     # Rouge
    'heuristique': '#27ae60',   # Vert
    'cognitif': '#2980b9'      # Bleu
}

labels = {
    'aleatoire': 'Réactif Aléatoire',
    'heuristique': 'Réactif Heuristique locale',
    'cognitif': 'Cognitif (Gain - Coût)'
}

markers = {
    'aleatoire': 'o',
    'heuristique': 's',
    'cognitif': '^'
}

# ==============================================================================
# 1. GRAPHIQUE OFFICIEL : Efficacité normalisée \hat{MaxMaxIdle}(G)
# ==============================================================================
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

for strat in ['heuristique', 'cognitif', 'aleatoire']:
    sub = df[df['strategie'] == strat].groupby('nb_patrouilleurs')[norm_col].agg(['mean', 'std']).loc[m_vals]
    ax.plot(sub.index, sub['mean'], marker=markers[strat], color=colors[strat], 
            label=f"{labels[strat]} (moyenne)", linewidth=2.4, markersize=8)
    ax.fill_between(sub.index, sub['mean'] - sub['std'], sub['mean'] + sub['std'], 
                    color=colors[strat], alpha=0.18, label=f"± 1 écart-type ({strat})")

ax.set_xscale('log', base=2)
ax.set_xticks(m_vals)
ax.set_xticklabels([str(m) for m in m_vals], fontsize=11)
ax.set_xlabel('Nombre de patrouilleurs $m$', fontsize=13, fontweight='bold', labelpad=10)
ax.set_ylabel(r'$\widehat{\mathrm{MaxMaxIdle}}(G) = \frac{m}{n} \times \mathrm{MaxMaxIdle}(G)$', fontsize=13, fontweight='bold', labelpad=10)
ax.set_title(r'Exercice 5 (Q1) : Évolution du critère normalisé $\widehat{\mathrm{MaxMaxIdle}}(G)$' + '\n' + r'en fonction du nombre de patrouilleurs ($n=400$ tuiles, 3000 pas, 30 runs)', fontsize=13, fontweight='bold', pad=14)
ax.grid(True, which="both", ls="--", color='#dddddd', alpha=0.8)

# Annotations clés
ax.annotate('Heuristique : passage à l\'échelle optimal\n(score quasi-constant $\\approx 3.5 - 4.4$)', 
            xy=(16, 3.496), xytext=(8, 12),
            arrowprops=dict(facecolor='#27ae60', shrink=0.08, width=1.5, headwidth=7),
            fontsize=10, fontweight='bold', color='#1e8449',
            bbox=dict(boxstyle="round,pad=0.3", fc="#eafaf1", ec="#27ae60", lw=1))

ax.annotate('Cognitif : effondrement à grande échelle\n(effet de troupeau sans coordination)', 
            xy=(64, 32.77), xytext=(16, 25),
            arrowprops=dict(facecolor='#2980b9', shrink=0.08, width=1.5, headwidth=7),
            fontsize=10, fontweight='bold', color='#1b4f72',
            bbox=dict(boxstyle="round,pad=0.3", fc="#ebf5fb", ec="#2980b9", lw=1))

# Légende épurée
handles, leg_labels = ax.get_legend_handles_labels()
# On ne garde que les 3 moyennes pour la clarté
ax.legend(handles[0:6:2], [leg_labels[0], leg_labels[2], leg_labels[4]], 
          frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cccccc', fontsize=11, loc='upper left')

plt.tight_layout()
plt.savefig('graphe_maxmaxidle_normalise.png')
plt.close()

# ==============================================================================
# 2. GRAPHIQUE BRUT : MaxMaxIdle(G) en ticks
# ==============================================================================
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

for strat in ['heuristique', 'cognitif', 'aleatoire']:
    sub = df[df['strategie'] == strat].groupby('nb_patrouilleurs')[raw_col].agg(['mean', 'std']).loc[m_vals]
    ax.plot(sub.index, sub['mean'], marker=markers[strat], color=colors[strat], 
            label=labels[strat], linewidth=2.4, markersize=8)
    ax.fill_between(sub.index, np.maximum(0, sub['mean'] - sub['std']), sub['mean'] + sub['std'], 
                    color=colors[strat], alpha=0.18)

ax.set_xscale('log', base=2)
ax.set_xticks(m_vals)
ax.set_xticklabels([str(m) for m in m_vals], fontsize=11)
ax.set_xlabel('Nombre de patrouilleurs $m$', fontsize=13, fontweight='bold', labelpad=10)
ax.set_ylabel(r'$\mathrm{MaxMaxIdle}(G)$ brut (ticks)', fontsize=13, fontweight='bold', labelpad=10)
ax.set_title(r'Pire cas d\'oisiveté absolue $\mathrm{MaxMaxIdle}(G)$ en fonction de $m$' + '\n' + r'($n=400$ tuiles, 3000 pas, 30 runs)', fontsize=13, fontweight='bold', pad=14)
ax.grid(True, which="both", ls="--", color='#dddddd', alpha=0.8)
ax.legend(frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cccccc', fontsize=11, loc='upper right')

plt.tight_layout()
plt.savefig('graphe_maxmaxidle_brut.png')
plt.close()

# ==============================================================================
# 3. GRAPHIQUE COMPARATIF DOUBLE (Panel A: Brut, Panel B: Normalisé)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

# Panel 1 : Brut
for strat in ['heuristique', 'cognitif', 'aleatoire']:
    sub = df[df['strategie'] == strat].groupby('nb_patrouilleurs')[raw_col].agg(['mean', 'std']).loc[m_vals]
    ax1.plot(sub.index, sub['mean'], marker=markers[strat], color=colors[strat], 
             label=labels[strat], linewidth=2.2, markersize=7)
    ax1.fill_between(sub.index, np.maximum(0, sub['mean'] - sub['std']), sub['mean'] + sub['std'], 
                     color=colors[strat], alpha=0.15)

ax1.set_xscale('log', base=2)
ax1.set_xticks(m_vals)
ax1.set_xticklabels([str(m) for m in m_vals], fontsize=10)
ax1.set_xlabel('Nombre de patrouilleurs $m$', fontsize=12, fontweight='bold')
ax1.set_ylabel(r'$\mathrm{MaxMaxIdle}(G)$ brut (ticks)', fontsize=12, fontweight='bold')
ax1.set_title('(A) Oisiveté maximale absolue brute', fontsize=13, fontweight='bold')
ax1.grid(True, ls="--", alpha=0.7)
ax1.legend(frameon=True, facecolor='white', fontsize=10, loc='upper right')

# Panel 2 : Normalisé
for strat in ['heuristique', 'cognitif', 'aleatoire']:
    sub = df[df['strategie'] == strat].groupby('nb_patrouilleurs')[norm_col].agg(['mean', 'std']).loc[m_vals]
    ax2.plot(sub.index, sub['mean'], marker=markers[strat], color=colors[strat], 
             label=labels[strat], linewidth=2.2, markersize=7)
    ax2.fill_between(sub.index, sub['mean'] - sub['std'], sub['mean'] + sub['std'], 
                     color=colors[strat], alpha=0.15)

ax2.set_xscale('log', base=2)
ax2.set_xticks(m_vals)
ax2.set_xticklabels([str(m) for m in m_vals], fontsize=10)
ax2.set_xlabel('Nombre de patrouilleurs $m$', fontsize=12, fontweight='bold')
ax2.set_ylabel(r'$\widehat{\mathrm{MaxMaxIdle}}(G) = \frac{m}{n} \times \mathrm{MaxMaxIdle}(G)$', fontsize=12, fontweight='bold')
ax2.set_title('(B) Facteur de dérive normalisé (Efficacité)', fontsize=13, fontweight='bold')
ax2.grid(True, ls="--", alpha=0.7)
ax2.legend(frameon=True, facecolor='white', fontsize=10, loc='upper left')

plt.suptitle('Synthèse comparative : Comportements de patrouille multi-agents sous NetLogo', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('graphe_comparatif_global.png', bbox_inches='tight')
plt.close()

print('Tous les graphiques ont été générés avec succès.')
