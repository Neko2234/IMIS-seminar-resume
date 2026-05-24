"""Figure A: Label vs place displacement in label coordinates, with regression lines.

Coordinate mapping (90-deg CCW rotation from robot frame):
  disp_cx = -(place_y - ref_ry)   [c_x increases → robot Y decreases]
  disp_cy =  (place_x - ref_rx)   [c_y increases → robot X increases]
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats

mpl.rcParams.update({'font.size': 9, 'axes.titlesize': 9, 'axes.labelsize': 9,
                     'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 7.5,
                     'figure.dpi': 150})

import os; base = os.path.dirname(__file__)

DATA = {
    'Direct w/ image':     'direct_results_summary.csv',
    'Residual w/ image':   'res_results_summary.csv',
    'Residual w/o image':  'res_nonImage_results_summary.csv',
}
COLORS = {'Direct w/ image': '#e07b39', 'Residual w/ image': '#4878cf', 'Residual w/o image': '#6acc65'}
MARKERS = {'Direct w/ image': 'o', 'Residual w/ image': 's', 'Residual w/o image': '^'}

# Reference place position from motion_copy (robot coordinates)
mc = pd.read_csv(os.path.join(base, 'motion_copy_results_summary.csv'))
ref_rx = mc['place_x'].mean()
ref_ry = mc['place_y'].mean()
print(f"Reference place (robot): X={ref_rx:.2f}, Y={ref_ry:.2f}")
print("Label coords: disp_cx = -(place_y - ref_ry),  disp_cy = place_x - ref_rx\n")

print("=== Label Following Statistics (label coordinate displacements) ===")

fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
axes[0].set_title(r'(a) $c_x$ direction')
axes[1].set_title(r'(b) $c_y$ direction')

for name, fname in DATA.items():
    df = pd.read_csv(os.path.join(base, fname))
    df['disp_cx'] = -(df['place_y'] - ref_ry)
    df['disp_cy'] =   df['place_x'] - ref_rx
    c = COLORS[name]; m = MARKERS[name]

    for ax_i, (lbl_col, dsp_col) in enumerate([('label_x', 'disp_cx'), ('label_y', 'disp_cy')]):
        x, y = df[lbl_col].values, df[dsp_col].values
        mask = np.isfinite(x) & np.isfinite(y)
        x, y = x[mask], y[mask]
        rho, _ = stats.spearmanr(x, y)
        slope, intercept, r, _, _ = stats.linregress(x, y)
        r2 = r**2
        xfit = np.linspace(x.min(), x.max(), 100)
        axes[ax_i].scatter(x, y, s=6, alpha=0.4, color=c, marker=m)
        axes[ax_i].plot(xfit, slope*xfit + intercept, color=c, linewidth=1.5,
                        label=f'{name}\n$R^2$={r2:.2f}, $\\rho$={rho:.2f}')
        print(f"{name}: {lbl_col}->{dsp_col}  R2={r2:.3f}  rho={rho:.3f}  slope={slope:.3f}")

for ax, xlabel, ylabel in zip(axes,
        [r'$c_x$ [mm]', r'$c_y$ [mm]'],
        [r'$\Delta_{\rm place}\,c_x$ [mm]', r'$\Delta_{\rm place}\,c_y$ [mm]']):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='gray', linewidth=0.5, linestyle='--')
axes[0].legend(loc='upper left', framealpha=0.85, fontsize=7)

plt.tight_layout()
plt.savefig(os.path.join(base, 'fig_label_scatter.pdf'), bbox_inches='tight')
plt.savefig(os.path.join(base, 'fig_label_scatter.png'), bbox_inches='tight')
print("\nSaved fig_label_scatter.pdf/png")
