"""Figure B: Place position distribution at c=[0,0] in label coordinates.

Coordinate mapping:
  cx_pos = -(place_y - ref_ry)   [label c_x direction]
  cy_pos =  (place_x - ref_rx)   [label c_y direction]
Reference (0, 0) = Motion Copy mean place position.
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
COLORS = {'Motion Copy': '#333333', 'Direct w/ image': '#e07b39',
          'Residual w/ image': '#4878cf', 'Residual w/o image': '#6acc65'}
MARKERS = {'Motion Copy': 'D', 'Direct w/ image': 'o',
           'Residual w/ image': 's', 'Residual w/o image': '^'}

# Reference from Motion Copy mean place position
mc = pd.read_csv(os.path.join(base, 'motion_copy_results_summary.csv'))
ref_rx = mc['place_x'].mean()
ref_ry = mc['place_y'].mean()

fig, ax = plt.subplots(figsize=(3.8, 3.4))

print("=== c=[0,0] Place Position Bias (label coordinates) ===")

for name, fname in DATA.items():
    df = pd.read_csv(os.path.join(base, fname))
    sub = df[(df['label_x'] == 0) & (df['label_y'] == 0)]
    cx = -(sub['place_y'].values - ref_ry)   # label c_x direction
    cy =   sub['place_x'].values - ref_rx    # label c_y direction
    ax.scatter(cx, cy, s=40, color=COLORS[name], marker=MARKERS[name],
               label=f'{name} (n={len(sub)})', zorder=3, alpha=0.85)
    mean_cx, mean_cy = cx.mean(), cy.mean()
    offset = np.sqrt(mean_cx**2 + mean_cy**2)
    print(f"{name}: n={len(sub)}  mean_cx={mean_cx:.1f}  mean_cy={mean_cy:.1f}"
          f"  offset={offset:.1f} mm  std_cx={cx.std():.2f}  std_cy={cy.std():.2f}")

# Reference at origin
ax.plot(0, 0, 'k+', markersize=14, markeredgewidth=2, zorder=5, label='Reference (0, 0)')

ax.set_xlabel(r'$\Delta c_x$ [mm]')
ax.set_ylabel(r'$\Delta c_y$ [mm]')
ax.set_title(r'Place position at $\mathbf{c}=[0,0]$')
ax.legend(loc='best', framealpha=0.85)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(base, 'fig_bias_scatter.pdf'), bbox_inches='tight')
plt.savefig(os.path.join(base, 'fig_bias_scatter.png'), bbox_inches='tight')
print("Saved fig_bias_scatter.pdf/png")
