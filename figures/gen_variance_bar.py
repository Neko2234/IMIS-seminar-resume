"""Figure C: Within-label variance bar chart."""
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

print("=== Within-label Standard Deviation ===")
names_plot, means_x, errs_x, means_y, errs_y = [], [], [], [], []

for name, fname in DATA.items():
    df = pd.read_csv(os.path.join(base, fname))
    grp = df.groupby(['label_x', 'label_y'])
    std_x = grp['delta_x'].std().dropna()
    std_y = grp['delta_y'].std().dropna()
    mx, ex = std_x.mean(), std_x.std()
    my, ey = std_y.mean(), std_y.std()
    names_plot.append(name)
    means_x.append(mx); errs_x.append(ex)
    means_y.append(my); errs_y.append(ey)
    print(f"{name}: sigma_x_mean={mx:.2f}±{ex:.2f}  sigma_y_mean={my:.2f}±{ey:.2f}")

fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0), sharey=False)
short = [n.replace(' w/ image', '\n(w/ img)').replace(' w/o image', '\n(w/o img)') for n in names_plot]
colors = [COLORS[n] for n in names_plot]
x = np.arange(len(names_plot))
w = 0.6

for ax, means, errs, axis_label in zip(axes,
        [means_x, means_y], [errs_x, errs_y], ['$\\sigma_{\\Delta x}$ [mm]', '$\\sigma_{\\Delta y}$ [mm]']):
    bars = ax.bar(x, means, w, yerr=errs, capsize=4, color=colors, edgecolor='black', linewidth=0.5)
    mc_val = means[0]
    ax.axhline(mc_val, color='gray', linestyle='--', linewidth=1.2, label='Motion Copy baseline')
    ax.set_xticks(x); ax.set_xticklabels(short, ha='center')
    ax.set_ylabel(axis_label)
    ax.grid(axis='y', alpha=0.3)

axes[0].set_title('(a) $X$ direction')
axes[1].set_title('(b) $Y$ direction')
axes[0].legend(fontsize=7.5)

plt.tight_layout()
plt.savefig(os.path.join(base, 'fig_variance_bar.pdf'), bbox_inches='tight')
plt.savefig(os.path.join(base, 'fig_variance_bar.png'), bbox_inches='tight')
print("Saved fig_variance_bar.pdf/png")
