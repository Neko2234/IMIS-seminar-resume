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

PANELS = [
    ('label_x', 'disp_cx', r'$c_x$ [cm]', r'$\Delta_{\rm place}\,c_x$ [mm]',
     'fig_label_scatter_cx'),
    ('label_y', 'disp_cy', r'$c_y$ [cm]', r'$\Delta_{\rm place}\,c_y$ [mm]',
     'fig_label_scatter_cy'),
]

# Pre-compute displacements for all models
model_data = {}
for name, fname in DATA.items():
    df = pd.read_csv(os.path.join(base, fname))
    df['disp_cx'] = -(df['place_y'] - ref_ry)
    df['disp_cy'] =   df['place_x'] - ref_rx
    model_data[name] = df

# Compute shared y-axis range across both panels
all_y = []
for lbl_col, dsp_col, *_ in PANELS:
    for name in DATA:
        y = model_data[name][dsp_col].dropna().values
        all_y.extend(y)
pad = 5
y_shared = (min(all_y) - pad, max(all_y) + pad)
print(f"Shared y-axis range: {y_shared[0]:.1f} to {y_shared[1]:.1f}\n")

for lbl_col, dsp_col, xlabel, ylabel, outname in PANELS:
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    for name in DATA:
        df = model_data[name]
        c = COLORS[name]; m = MARKERS[name]
        x, y = df[lbl_col].values, df[dsp_col].values
        mask = np.isfinite(x) & np.isfinite(y)
        x, y = x[mask], y[mask]
        rho, _ = stats.spearmanr(x, y)
        slope, intercept, r, _, _ = stats.linregress(x, y)
        r2 = r**2
        xfit = np.linspace(x.min(), x.max(), 100)
        ax.scatter(x, y, s=6, alpha=0.4, color=c, marker=m)
        ax.plot(xfit, slope*xfit + intercept, color=c, linewidth=1.5, label=name)
        print(f"{name}: {lbl_col}->{dsp_col}  R2={r2:.3f}  rho={rho:.3f}  slope={slope:.3f}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(y_shared)
    ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='gray', linewidth=0.5, linestyle='--')
    ax.legend(loc='upper left', framealpha=0.85, fontsize=7)
    plt.tight_layout()
    plt.savefig(os.path.join(base, outname + '.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(base, outname + '.png'), bbox_inches='tight')
    plt.close()
    print(f"Saved {outname}.pdf/png")
print()
