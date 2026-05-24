"""Figure A: Label vs place displacement (from reference) scatter with regression lines."""
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

# Reference place position from motion_copy
mc = pd.read_csv(os.path.join(base, 'motion_copy_results_summary.csv'))
ref_x = mc['place_x'].mean()
ref_y = mc['place_y'].mean()
print(f"Reference place position: ({ref_x:.2f}, {ref_y:.2f})")

print("\n=== Label Following Statistics (place deviation from reference) ===")
print("Checking all 4 correlations: label_x→disp_x, label_x→disp_y, label_y→disp_x, label_y→disp_y\n")

# Determine best axis mapping from res model (ground truth for strong correlation)
res_df = pd.read_csv(os.path.join(base, 'res_results_summary.csv'))
res_df['disp_x'] = res_df['place_x'] - ref_x
res_df['disp_y'] = res_df['place_y'] - ref_y
_, _, r_xx, _, _ = stats.linregress(res_df['label_x'], res_df['disp_x'])
_, _, r_xy, _, _ = stats.linregress(res_df['label_x'], res_df['disp_y'])
_, _, r_yx, _, _ = stats.linregress(res_df['label_y'], res_df['disp_x'])
_, _, r_yy, _, _ = stats.linregress(res_df['label_y'], res_df['disp_y'])
print(f"Res: r(label_x,disp_x)={r_xx:.3f}  r(label_x,disp_y)={r_xy:.3f}")
print(f"Res: r(label_y,disp_x)={r_yx:.3f}  r(label_y,disp_y)={r_yy:.3f}")

# Choose mapping based on absolute correlation
if abs(r_xx) >= abs(r_xy):
    map_a = ('label_x', 'disp_x', '$c_x$ [mm]', '$\\Delta x_{\\rm place}$ [mm]')
    map_b = ('label_y', 'disp_y', '$c_y$ [mm]', '$\\Delta y_{\\rm place}$ [mm]')
else:
    map_a = ('label_x', 'disp_y', '$c_x$ [mm]', '$\\Delta y_{\\rm place}$ [mm]')
    map_b = ('label_y', 'disp_x', '$c_y$ [mm]', '$\\Delta x_{\\rm place}$ [mm]')
print(f"\nAxis mapping: label_x -> {map_a[1]}, label_y -> {map_b[1]}\n")

fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
axes[0].set_title(f'(a) $c_x$ direction')
axes[1].set_title(f'(b) $c_y$ direction')

for name, fname in DATA.items():
    df = pd.read_csv(os.path.join(base, fname))
    df['disp_x'] = df['place_x'] - ref_x
    df['disp_y'] = df['place_y'] - ref_y
    c = COLORS[name]; m = MARKERS[name]

    for ax_i, (lbl, dlt, xlabel, ylabel) in enumerate([map_a, map_b]):
        x, y = df[lbl].values, df[dlt].values
        mask = np.isfinite(x) & np.isfinite(y)
        x, y = x[mask], y[mask]
        rho, _ = stats.spearmanr(x, y)
        slope, intercept, r, _, _ = stats.linregress(x, y)
        r2 = r**2
        xfit = np.linspace(x.min(), x.max(), 100)
        axes[ax_i].scatter(x, y, s=6, alpha=0.4, color=c, marker=m)
        axes[ax_i].plot(xfit, slope*xfit + intercept, color=c, linewidth=1.5,
                        label=f'{name}\n$R^2$={r2:.2f}, $\\rho$={rho:.2f}')
        print(f"{name}: {lbl}->{dlt}  R2={r2:.3f}  rho={rho:.3f}  slope={slope:.3f}")

for ax, (lbl, dlt, xlabel, ylabel) in zip(axes, [map_a, map_b]):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='gray', linewidth=0.5, linestyle='--')
axes[0].legend(loc='upper left', framealpha=0.85, fontsize=7)

plt.tight_layout()
plt.savefig(os.path.join(base, 'fig_label_scatter.pdf'), bbox_inches='tight')
plt.savefig(os.path.join(base, 'fig_label_scatter.png'), bbox_inches='tight')
print("\nSaved fig_label_scatter.pdf/png")
