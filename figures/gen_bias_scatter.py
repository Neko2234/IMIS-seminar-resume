"""Figure B: Place position distribution at c=[0,0]."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

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

fig, ax = plt.subplots(figsize=(3.8, 3.4))

print("=== c=[0,0] Place Position Bias ===")
ref_x, ref_y = None, None

for name, fname in DATA.items():
    df = pd.read_csv(os.path.join(base, fname))
    sub = df[(df['label_x'] == 0) & (df['label_y'] == 0)]
    px, py = sub['place_x'].values, sub['place_y'].values
    ax.scatter(px, py, s=40, color=COLORS[name], marker=MARKERS[name],
               label=f'{name} (n={len(sub)})', zorder=3, alpha=0.85)
    mean_x, mean_y = px.mean(), py.mean()
    std_xy = np.sqrt(((px - mean_x)**2 + (py - mean_y)**2).mean())
    print(f"{name}: n={len(sub)}  mean=({mean_x:.1f}, {mean_y:.1f})  bias_XY={std_xy:.1f} mm"
          f"  std_x={px.std():.2f}  std_y={py.std():.2f}")
    if name == 'Motion Copy':
        ref_x, ref_y = mean_x, mean_y

if ref_x is not None:
    ax.plot(ref_x, ref_y, 'k+', markersize=14, markeredgewidth=2,
            zorder=5, label=f'Reference ({ref_x:.0f}, {ref_y:.0f})')

ax.set_xlabel('place$_x$ [mm]')
ax.set_ylabel('place$_y$ [mm]')
ax.set_title('Place position at $\\mathbf{c}=[0,0]$')
ax.legend(loc='best', framealpha=0.85)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(base, 'fig_bias_scatter.pdf'), bbox_inches='tight')
plt.savefig(os.path.join(base, 'fig_bias_scatter.png'), bbox_inches='tight')
print("Saved fig_bias_scatter.pdf/png")
