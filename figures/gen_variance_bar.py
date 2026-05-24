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
names_plot, means_cx, errs_cx, means_cy, errs_cy = [], [], [], [], []

for name, fname in DATA.items():
    df = pd.read_csv(os.path.join(base, fname))
    df['place_cx'] = -(df['place_y'] - ref_ry)
    df['place_cy'] =   df['place_x'] - ref_rx
    grp = df.groupby(['label_x', 'label_y'])
    std_cx = grp['place_cx'].std().dropna()
    std_cy = grp['place_cy'].std().dropna()
    mcx, ecx = std_cx.mean(), std_cx.std()
    mcy, ecy = std_cy.mean(), std_cy.std()
    names_plot.append(name)
    means_cx.append(mcx); errs_cx.append(ecx)
    means_cy.append(mcy); errs_cy.append(ecy)
    print(f"{name}: sigma_cx={mcx:.2f}±{ecx:.2f}  sigma_cy={mcy:.2f}±{ecy:.2f}")

fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0), sharey=False)
short = [n.replace(' w/ image', '\n(w/ img)').replace(' w/o image', '\n(w/o img)') for n in names_plot]
colors = [COLORS[n] for n in names_plot]
x = np.arange(len(names_plot))
w = 0.6

for ax, means, errs, axis_label in zip(axes,
        [means_cx, means_cy], [errs_cx, errs_cy],
        [r'$\sigma_{\Delta c_x}$ [mm]', r'$\sigma_{\Delta c_y}$ [mm]']):
    ax.bar(x, means, w, yerr=errs, capsize=4, color=colors, edgecolor='black', linewidth=0.5)
    ax.axhline(means[0], color='gray', linestyle='--', linewidth=1.2, label='Motion Copy baseline')
    ax.set_xticks(x); ax.set_xticklabels(short, ha='center')
    ax.set_ylabel(axis_label)
    ax.grid(axis='y', alpha=0.3)

axes[0].set_title(r'(a) $c_x$ direction')
axes[1].set_title(r'(b) $c_y$ direction')
axes[0].legend(fontsize=7.5)

plt.tight_layout()
plt.savefig(os.path.join(base, 'fig_variance_bar.pdf'), bbox_inches='tight')
plt.savefig(os.path.join(base, 'fig_variance_bar.png'), bbox_inches='tight')
print("Saved fig_variance_bar.pdf/png")
