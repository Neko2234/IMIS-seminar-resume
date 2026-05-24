"""Figure D: Pick position deviation heatmap + OOD analysis."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 9, 'axes.labelsize': 9,
                     'xtick.labelsize': 8, 'ytick.labelsize': 8})

import os; base = os.path.dirname(__file__)

MODELS = {
    'Direct w/ image':     'direct_results_summary.csv',
    'Residual w/ image':   'res_results_summary.csv',
    'Residual w/o image':  'res_nonImage_results_summary.csv',
}
TRAIN_LABELS = {(0,0),(5,0),(-5,0),(0,5),(0,-5),(5,5),(5,-5),(-5,5),(-5,-5)}

mc_df = pd.read_csv(os.path.join(base, 'motion_copy_results_summary.csv'))
ref_pick_x = mc_df['pick_x'].mean()
ref_pick_y = mc_df['pick_y'].mean()
print(f"Reference pick position (Motion Copy): ({ref_pick_x:.2f}, {ref_pick_y:.2f})")

# All label values used
lx_vals = sorted([-7,-5,-3,0,3,5,7])
ly_vals = sorted([-7,-5,-3,0,3,5,7])

print("\n=== Pick Position Deviation Analysis ===")
fig, axes = plt.subplots(1, 3, figsize=(7.5, 2.8))

for ax, (name, fname) in zip(axes, MODELS.items()):
    df = pd.read_csv(os.path.join(base, fname))

    # Count trials per label (to detect exclusions)
    trial_counts = df.groupby(['label_x', 'label_y']).size()

    # Per-label mean pick deviation
    grp = df.groupby(['label_x', 'label_y'])
    mean_pick = grp[['pick_x', 'pick_y']].mean()

    grid = np.full((len(ly_vals), len(lx_vals)), np.nan)
    for i, ly in enumerate(ly_vals):
        for j, lx in enumerate(lx_vals):
            try:
                px = mean_pick.loc[(lx, ly), 'pick_x']
                py = mean_pick.loc[(lx, ly), 'pick_y']
                grid[i, j] = np.sqrt((px - ref_pick_x)**2 + (py - ref_pick_y)**2)
            except KeyError:
                pass  # label not tested -> stays NaN

    # Identify excluded labels (tested labels that had <5 trials due to failures)
    excluded = [(lx, ly) for (lx, ly), cnt in trial_counts.items() if cnt < 5]
    in_dist = [(lx, ly) for (lx, ly) in trial_counts.index if (lx, ly) in TRAIN_LABELS]

    cmap = plt.cm.YlOrRd.copy(); cmap.set_bad('#cccccc')
    im = ax.imshow(grid, origin='lower', cmap=cmap, aspect='auto',
                   extent=[-7.5, 7.5, -7.5, 7.5], vmin=0, vmax=40)

    # Mark excluded labels with X
    for (lx, ly) in excluded:
        ax.plot(lx, ly, 'kx', markersize=8, markeredgewidth=1.5)

    ax.set_xticks(lx_vals); ax.set_yticks(ly_vals)
    ax.set_xlabel('$c_x$ [mm]'); ax.set_ylabel('$c_y$ [mm]') if ax == axes[0] else None
    ax.set_title(name, fontsize=8.5)
    plt.colorbar(im, ax=ax, label='deviation [mm]' if ax == axes[2] else '')

    # Print stats
    excluded_lbl_str = ', '.join([f'({lx},{ly})' for lx, ly in excluded])
    print(f"\n{name}:")
    print(f"  Excluded labels (pick failures): {excluded_lbl_str if excluded else 'none'}")
    # In-dist successful labels
    valid = df.copy()
    in_dist_dev = []
    for (lx, ly) in in_dist:
        sub = df[(df['label_x']==lx) & (df['label_y']==ly)]
        if len(sub) > 0:
            d = np.sqrt((sub['pick_x'] - ref_pick_x)**2 + (sub['pick_y'] - ref_pick_y)**2)
            in_dist_dev.append(d.mean())
    ood_dev = []
    for i, ly in enumerate(ly_vals):
        for j, lx in enumerate(lx_vals):
            if not np.isnan(grid[i,j]) and (lx, ly) not in TRAIN_LABELS:
                ood_dev.append(grid[i,j])
    print(f"  In-dist pick deviation: mean={np.mean(in_dist_dev):.1f} mm")
    print(f"  OOD pick deviation:     mean={np.mean(ood_dev):.1f} mm" if ood_dev else "  No OOD data")
    # Within-label std for pick position
    within_std = []
    for (lx, ly), sub in df.groupby(['label_x', 'label_y']):
        if len(sub) >= 3:
            s = np.sqrt(sub['pick_x'].std()**2 + sub['pick_y'].std()**2)
            within_std.append(s)
    print(f"  Within-label pick std (mean): {np.mean(within_std):.2f} mm")

plt.tight_layout()
plt.savefig(os.path.join(base, 'fig_pick_pos.pdf'), bbox_inches='tight')
plt.savefig(os.path.join(base, 'fig_pick_pos.png'), bbox_inches='tight')
print("\nSaved fig_pick_pos.pdf/png")
