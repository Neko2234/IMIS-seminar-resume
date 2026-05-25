"""Figure C: Within-label variance bar chart in label coordinates.

Uses absolute place position converted to label frame:
  place_cx = -(place_y - ref_ry)   [label c_x direction]
  place_cy =  (place_x - ref_rx)   [label c_y direction]
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 9, 'axes.labelsize': 9,
                     'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8})

import os; base = os.path.dirname(__file__)

DATA = {
    'Motion Copy':         'motion_copy_results_summary.csv',
    'Direct w/ image':     'direct_results_summary.csv',
    'Residual w/ image':   'res_results_summary.csv',
    'Residual w/o image':  'res_nonImage_results_summary.csv',
}
COLORS = {'Motion Copy': '#888888', 'Direct w/ image': '#e07b39',
          'Residual w/ image': '#4878cf', 'Residual w/o image': '#6acc65'}

# Reference from Motion Copy
mc = pd.read_csv(os.path.join(base, 'motion_copy_results_summary.csv'))
ref_rx = mc['place_x'].mean()
ref_ry = mc['place_y'].mean()

print("=== Within-label Standard Deviation (label coordinates) ===")
names_plot, means_cx, means_cy = [], [], []

for name, fname in DATA.items():
    df = pd.read_csv(os.path.join(base, fname))
    df['place_cx'] = -(df['place_y'] - ref_ry)
    df['place_cy'] =   df['place_x'] - ref_rx
    grp = df.groupby(['label_x', 'label_y'])
    std_cx = grp['place_cx'].std().dropna()
    std_cy = grp['place_cy'].std().dropna()
    names_plot.append(name)
    means_cx.append(std_cx.mean())
    means_cy.append(std_cy.mean())
    print(f"{name}: sigma_cx={std_cx.mean():.2f}  sigma_cy={std_cy.mean():.2f}")

short = [n.replace(' w/ image', '\n(w/ img)').replace(' w/o image', '\n(w/o img)') for n in names_plot]
colors = [COLORS[n] for n in names_plot]
x = np.arange(len(names_plot))
w = 0.6

PANELS = [
    (means_cx, r'$\sigma_{\Delta c_x}$ [mm]', 'fig_variance_bar_cx'),
    (means_cy, r'$\sigma_{\Delta c_y}$ [mm]', 'fig_variance_bar_cy'),
]

y_top = max(m for means, *_ in PANELS for m in means if np.isfinite(m))
margin = y_top * 0.08
y_shared = (0, y_top + margin)
print(f"Shared y-axis range: {y_shared[0]:.1f} to {y_shared[1]:.1f}\n")

for means, axis_label, outname in PANELS:
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    ax.bar(x, means, w, color=colors, edgecolor='black', linewidth=0.5)
    ax.set_xticks(x); ax.set_xticklabels(short, ha='center')
    ax.set_ylabel(axis_label)
    ax.set_ylim(y_shared)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(base, outname + '.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(base, outname + '.png'), bbox_inches='tight')
    plt.close()
    print(f"Saved {outname}.pdf/png")
