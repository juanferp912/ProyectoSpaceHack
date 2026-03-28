"""
SpaceHack 2026 — External Data Visualizations
===============================================
Reads external_insights/ CSVs and generates 7 professional charts
saved to external_results/ at 300 DPI.

Charts:
  ext_01_corridor_green_stage.png    — G2Z maturity ladder: 3 corridors on 5-stage axis
  ext_02_co2_savings_waterfall.png   — CO2 remaining after each fuel scenario per corridor
  ext_03_thetis_fleet_breakdown.png  — THETIS-MRV EU fleet CO2 by vessel type (531 Mt)
  ext_04_cii_compliance_heatmap.png  — CII compliance grade heatmap (vessel type x corridor)
  ext_05_voyage_emissions_bubble.png — Bubble: annual voyages x distance x CO2 per corridor
  ext_06_fuel_deployment_gantt.png   — Fuel readiness Gantt: TRL + commercial timeline
  ext_07_imo_vs_corridor_gap.png     — 2030 IMO target gap per corridor (bar + threshold line)
"""

import sys
import io
import warnings
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

# ── paths ────────────────────────────────────────────────────────────────────
workspace       = Path(__file__).parent.parent
insights_dir    = workspace / "external_insights"
results_dir     = workspace / "external_results"
results_dir.mkdir(exist_ok=True)

# ── style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family':    'DejaVu Sans',
    'font.size':      10,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi':     100,
    'savefig.dpi':    300,
})

# Corridor colour palette
C1 = '#E63946'   # Route 1 Shanghai-LA    red
C2 = '#457B9D'   # Route 2 Rotterdam-SGP  blue
C3 = '#2A9D8F'   # Route 3 Australia-EA   teal
NEUTRAL = '#A8DADC'
DARK    = '#1D3557'

CORR_COLORS = [C1, C2, C3]
CORR_SHORT  = ['Shanghai→LA', 'Rotterdam→SGP', 'Australia→EA']

SOURCE_NOTE = 'Sources: OECD.csv, THETIS-MRV 2023 (EMSA), Getting to Zero Coalition 2025, IMO MEPC 2023'

def _save(fig, name):
    p = results_dir / name
    fig.savefig(p, bbox_inches='tight')
    plt.close(fig)
    print(f"  [OK] {name}")

def _source(ax, note=SOURCE_NOTE):
    ax.annotate(note, xy=(0, -0.12), xycoords='axes fraction',
                fontsize=7, color='grey', ha='left')


# ============================================================================
# ext_01 — G2Z MATURITY LADDER
# ============================================================================
def chart_01_maturity():
    maturity = pd.read_csv(insights_dir / "04_corridor_green_maturity.csv")
    g2z      = pd.read_csv(Path(workspace) / "data" / "external" / "green_corridor_status.csv")

    stages = ['Announced', 'Feasibility', 'Adv. Feasibility', 'Early Realization', 'Realization']
    stage_x = {s: i for i, s in enumerate(stages)}
    status_map = {
        'Feasibility':         'Feasibility',
        'Advanced Feasibility':'Adv. Feasibility',
        'Early Realization':   'Early Realization',
        'Realization':         'Realization',
        'Announced':           'Announced',
    }

    fig, ax = plt.subplots(figsize=(11, 5))

    # Stage background bands
    for i, stage in enumerate(stages):
        color = '#f0f8f0' if i % 2 == 0 else '#e8f4f8'
        ax.axvspan(i - 0.5, i + 0.5, color=color, alpha=0.5, zorder=0)
        ax.text(i, 4.15, stage, ha='center', va='bottom', fontsize=9,
                color='#444', fontweight='bold')

    routes = [
        ('Route 1 (Shanghai -> LA)',       C1, 'Early Realization', 2800, True),
        ('Route 2 (Rotterdam -> Singapore)', C2, 'Advanced Feasibility', 3400, False),
        ('Route 3 (Australia -> East Asia)', C3, 'Feasibility',         5600, False),
    ]

    y_positions = [2.0, 1.0, 0.0]
    labels = ['Route 1\nShanghai->LA', 'Route 2\nRotterdam->SGP', 'Route 3\nAustralia->EA']

    for (route, color, status, voyages, phase1), y, lbl in zip(routes, y_positions, labels):
        sx = stage_x.get(status_map.get(status, 'Announced'), 0)

        # Progress trail
        ax.plot([-0.5, sx], [y, y], color=color, lw=6, alpha=0.25, solid_capstyle='round')
        ax.plot([-0.5, sx], [y, y], color=color, lw=2, alpha=0.8, solid_capstyle='round')

        # Milestone dots on completed stages
        for xi in range(sx + 1):
            filled = xi <= sx
            ax.plot(xi, y, 'o', ms=18, color=color if filled else 'white',
                    mec=color, mew=2, zorder=5)
            if xi <= sx:
                ax.text(xi, y, stages[xi][0], ha='center', va='center',
                        fontsize=7, color='white', fontweight='bold', zorder=6)

        # Current stage label
        ax.text(sx + 0.05, y + 0.22, status, fontsize=8, color=color,
                fontweight='bold', va='bottom')

        # Route label on left
        ax.text(-0.7, y, lbl, ha='right', va='center', fontsize=9,
                color=color, fontweight='bold')

        # Phase 1 badge
        if phase1:
            ax.annotate('Phase 1\nComplete', xy=(sx, y), xytext=(sx + 0.6, y + 0.5),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                        fontsize=7.5, color=color, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', fc='#f0fff0', ec=color, lw=1))

    # Global context callout
    ax.text(4.5, 3.7,
            '84 active green corridors\nglobally (2025)\n6 at Realization stage',
            ha='right', va='top', fontsize=8, color='#1D3557',
            bbox=dict(boxstyle='round,pad=0.5', fc='#dff2ff', ec='#457B9D', lw=1))

    ax.set_xlim(-1.2, 4.9)
    ax.set_ylim(-0.6, 4.5)
    ax.axis('off')
    ax.set_title('Green Shipping Corridor Maturity — Getting to Zero Coalition 2025',
                 pad=14, loc='left')
    _source(ax, 'Source: Getting to Zero Coalition Annual Progress Report 2025')
    _save(fig, 'ext_01_corridor_green_stage.png')


# ============================================================================
# ext_02 — CO2 SAVINGS WATERFALL (stacked bar diverging)
# ============================================================================
def chart_02_waterfall():
    df = pd.read_csv(insights_dir / "02_co2_savings_by_scenario.csv")

    scenarios_order = [
        'HFO Baseline', 'LNG', 'Wind-Assist', 'LNG + Wind-Assist',
        'Green Methanol', 'Green Ammonia', 'Green Hydrogen'
    ]
    colors_scen = {
        'HFO Baseline':      '#E63946',
        'LNG':               '#F4A261',
        'Wind-Assist':       '#E9C46A',
        'LNG + Wind-Assist': '#E76F51',
        'Green Methanol':    '#52B788',
        'Green Ammonia':     '#2D6A4F',
        'Green Hydrogen':    '#1B4332',
    }

    fig, axes = plt.subplots(1, 3, figsize=(15, 6), sharey=False)
    routes = df['corridor'].unique()

    for ax, route, color in zip(axes, routes, CORR_COLORS):
        sub = df[df['corridor'] == route].copy()
        sub['fuel_scenario'] = pd.Categorical(sub['fuel_scenario'],
                                               categories=scenarios_order, ordered=True)
        sub = sub.sort_values('fuel_scenario')

        baselines = sub['annual_baseline_t'].iloc[0]
        bars_rem  = sub['remaining_co2_t'] / 1e6   # Mt
        bars_save = sub['co2_saved_t'] / 1e6

        # Remaining CO2 bars
        bar_colors = [colors_scen.get(s, '#999') for s in sub['fuel_scenario']]
        bars = ax.bar(range(len(sub)), bars_rem, color=bar_colors, edgecolor='white',
                      linewidth=0.5, width=0.7, zorder=3)

        # Labels on bars
        for i, (rem, sav, scen) in enumerate(zip(bars_rem, bars_save, sub['fuel_scenario'])):
            if rem > 0:
                ax.text(i, rem + bars_rem.max() * 0.01,
                        f'{rem:.0f}', ha='center', va='bottom', fontsize=6.5,
                        fontweight='bold', color='#333')

        # IMO 2030 threshold line
        imo_target = baselines * 0.70 / 1e6  # -30% = 70% remains
        ax.axhline(imo_target, color='#1D3557', lw=1.5, ls='--', zorder=4)
        ax.text(len(sub) - 0.5, imo_target * 1.02, 'IMO -30% (2030)',
                ha='right', fontsize=7, color='#1D3557', fontweight='bold')

        # Zero carbon line
        ax.axhline(0, color='#2D6A4F', lw=1, ls=':', zorder=4)

        route_short = route.replace('Route 1: ', '').replace('Route 2: ', '').replace('Route 3: ', '')
        ax.set_title(f'{route_short}', fontsize=10, fontweight='bold', color=color)
        ax.set_xticks(range(len(sub)))
        ax.set_xticklabels([s.replace(' + ', '+\n').replace(' ', '\n', 1)
                            for s in sub['fuel_scenario']],
                           fontsize=7, rotation=0)
        ax.set_ylabel('Remaining CO2 (Mt / year)' if ax == axes[0] else '', fontsize=9)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}'))
        ax.grid(axis='y', alpha=0.3, zorder=1)

    fig.suptitle('CO2 Remaining After Fuel Transition — Per Corridor (2024 Baseline)',
                 fontsize=13, fontweight='bold', y=1.01)
    axes[-1].annotate(SOURCE_NOTE, xy=(1, -0.25), xycoords='axes fraction',
                      fontsize=7, color='grey', ha='right')
    plt.tight_layout()
    _save(fig, 'ext_02_co2_savings_waterfall.png')


# ============================================================================
# ext_03 — THETIS FLEET BREAKDOWN (donut + corridor relevance)
# ============================================================================
def chart_03_thetis_fleet():
    thetis = pd.read_csv(
        Path(workspace) / "data" / "external" / "thetis_rotterdam_ships.csv"
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # Left: Donut — CO2 by vessel type
    co2_vals = thetis['total_co2_million_t']
    labels   = thetis['ship_type']
    total    = co2_vals.sum()

    palette = ['#E63946','#457B9D','#2A9D8F','#E9C46A','#F4A261',
               '#A8DADC','#52B788','#2D6A4F','#1D3557','#6D6875']
    wedges, texts, autotexts = ax1.pie(
        co2_vals, labels=None, autopct='%1.1f%%',
        colors=palette[:len(thetis)],
        pctdistance=0.82, startangle=140,
        wedgeprops={'width': 0.55, 'edgecolor': 'white', 'linewidth': 1.5},
    )
    for at in autotexts:
        at.set_fontsize(7.5)
        at.set_fontweight('bold')

    ax1.text(0, 0, f'{total:.0f}\nMt CO2\n(2023)',
             ha='center', va='center', fontsize=11, fontweight='bold', color=DARK)
    ax1.set_title('EU Fleet CO2 by Vessel Type\n(THETIS-MRV 2023 — 28,774 ships)',
                  fontsize=10, fontweight='bold', pad=10)

    legend_labels = [f'{row.ship_type} ({row.total_co2_million_t:.1f} Mt)'
                     for _, row in thetis.iterrows()]
    ax1.legend(wedges, legend_labels, loc='lower center', bbox_to_anchor=(0.5, -0.22),
               fontsize=7.5, ncol=2, frameon=False)

    # Right: Horizontal bar — ships by type + CO2 trend arrow
    thetis_sorted = thetis.sort_values('ships_reporting')
    bar_colors = [palette[i] for i in range(len(thetis_sorted))]
    bars = ax2.barh(range(len(thetis_sorted)), thetis_sorted['ships_reporting'],
                    color=bar_colors, edgecolor='white', lw=0.8, height=0.6)

    for i, (_, row) in enumerate(thetis_sorted.iterrows()):
        trend = row['co2_trend_vs_2022_pct']
        arrow = 'up' if trend > 0 else 'down'
        color_t = '#E63946' if trend > 0 else '#2D6A4F'
        sign    = '+' if trend > 0 else ''
        ax2.text(row['ships_reporting'] + 50, i,
                 f'{sign}{trend:.1f}% CO2 vs 2022',
                 va='center', fontsize=7.5, color=color_t, fontweight='bold')

    ax2.set_yticks(range(len(thetis_sorted)))
    ax2.set_yticklabels(thetis_sorted['ship_type'], fontsize=8)
    ax2.set_xlabel('Ships Reporting to EMSA (2023)', fontsize=9)
    ax2.set_title('Ships Reporting per Type + CO2 Trend vs 2022',
                  fontsize=10, fontweight='bold')
    ax2.set_xlim(0, thetis_sorted['ships_reporting'].max() * 1.45)
    ax2.grid(axis='x', alpha=0.3)

    ax2.annotate(SOURCE_NOTE, xy=(0, -0.14), xycoords='axes fraction',
                 fontsize=7, color='grey', ha='left')
    plt.tight_layout()
    _save(fig, 'ext_03_thetis_fleet_breakdown.png')


# ============================================================================
# ext_04 — CII COMPLIANCE HEATMAP
# ============================================================================
def chart_04_cii_heatmap():
    df_cii = pd.read_csv(insights_dir / "03b_vessel_cii_rep.csv")

    # Matrix: vessel types vs metric columns
    vtypes   = df_cii['vessel_type'].tolist()
    metrics  = ['cii_reference_2023', 'actual_avg_cii_2023', 'cii_target_2026', 'cii_target_2030']
    labels   = ['CII Ref\n2023', 'Actual\n(THETIS 2023)', 'Target\n2026', 'Target\n2030']

    data_mat = df_cii[metrics].values

    # Grade colors per cell (relative to reference)
    grade_color = {'A': '#2D6A4F', 'B': '#52B788', 'C': '#E9C46A',
                   'D': '#F4A261', 'E': '#E63946', 'N/A': '#cccccc'}

    fig, ax = plt.subplots(figsize=(11, 6))

    for j, (col, lbl) in enumerate(zip(metrics, labels)):
        for i, vtype in enumerate(vtypes):
            val = df_cii.iloc[i][col]
            ref = df_cii.iloc[i]['cii_reference_2023']
            actual = df_cii.iloc[i]['actual_avg_cii_2023']

            # Color by performance relative to 2023 reference
            if col == 'actual_avg_cii_2023':
                grade = df_cii.iloc[i]['implied_grade_2023']
                bg = grade_color.get(grade, '#ccc')
                txt_color = 'white' if grade in ('D', 'E', 'A') else 'black'
                label_val = f'{val:.1f}\n({grade})'
            else:
                ratio = val / actual if actual > 0 else 1
                if ratio < 0.85:
                    bg = '#2D6A4F'
                    txt_color = 'white'
                elif ratio < 1.0:
                    bg = '#52B788'
                    txt_color = 'white'
                elif ratio <= 1.05:
                    bg = '#E9C46A'
                    txt_color = 'black'
                else:
                    bg = '#F4A261'
                    txt_color = 'black'
                label_val = f'{val:.1f}'

            rect = FancyBboxPatch((j - 0.45, i - 0.4), 0.9, 0.8,
                                  boxstyle='round,pad=0.05', fc=bg,
                                  ec='white', lw=1.5, zorder=3)
            ax.add_patch(rect)
            ax.text(j, i, label_val, ha='center', va='center', fontsize=8.5,
                    color=txt_color, fontweight='bold', zorder=4)

    # Column headers
    for j, lbl in enumerate(labels):
        ax.text(j, len(vtypes) - 0.2, lbl, ha='center', va='bottom', fontsize=9,
                fontweight='bold', color=DARK)

    # Row labels
    for i, vt in enumerate(vtypes):
        ax.text(-0.6, i, vt, ha='right', va='center', fontsize=9, color=DARK)

    # Unit label
    ax.text(1.5, -0.9, 'Unit: g CO2 / (dwt·nm)   |   "Actual" = THETIS-MRV 2023 fleet avg',
            ha='center', va='top', fontsize=8, color='grey', style='italic')

    # Grade legend
    handles = [mpatches.FancyArrow(0, 0, 0, 0, width=0, head_width=0,
                                    fc=grade_color[g], ec=grade_color[g],
                                    label=f'Grade {g}')
               for g in ['A', 'B', 'C', 'D', 'E']]
    handles = [plt.Rectangle((0, 0), 1, 1, fc=grade_color[g], ec='white',
                              label=f'Grade {g}') for g in ['A', 'B', 'C', 'D', 'E']]
    ax.legend(handles=handles, loc='lower right', fontsize=8, ncol=5,
              bbox_to_anchor=(1.0, -0.14), frameon=False, title='CII Grade')

    ax.set_xlim(-1.2, len(metrics) - 0.4)
    ax.set_ylim(-1.1, len(vtypes))
    ax.axis('off')
    ax.set_title('IMO CII Compliance — Actual Fleet vs 2023/2026/2030 Targets',
                 pad=12, loc='left', fontweight='bold')
    ax.annotate(SOURCE_NOTE, xy=(0, -0.15), xycoords='axes fraction',
                fontsize=7, color='grey', ha='left')
    _save(fig, 'ext_04_cii_compliance_heatmap.png')


# ============================================================================
# ext_05 — VOYAGE EMISSIONS BUBBLE
# ============================================================================
def chart_05_voyage_bubble():
    df = pd.read_csv(insights_dir / "06_annual_voyage_emissions.csv")

    fig, ax = plt.subplots(figsize=(10, 6))

    bubble_scale = 2e-4  # scale CO2 -> bubble area

    for i, (_, row) in enumerate(df.iterrows()):
        x = row['distance_nm']
        y = row['annual_voyages_est']
        s = row['co2_annual_baseline_Mt'] * bubble_scale * 4000

        color = CORR_COLORS[i]
        ax.scatter(x, y, s=s, color=color, alpha=0.75, edgecolors='white',
                   linewidths=2, zorder=5)

        route_label = (row['corridor']
                       .replace('Route 1: ', '').replace('Route 2: ', '')
                       .replace('Route 3: ', ''))
        ax.annotate(
            f"{route_label}\n"
            f"{row['co2_annual_baseline_Mt']:.0f} Mt/yr\n"
            f"{row['co2_per_voyage_t']/1e3:.0f} kt/voyage",
            xy=(x, y),
            xytext=(x + 150, y + 200 * (1 if i < 2 else -1)),
            fontsize=8.5, color=color, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=color, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, lw=1, alpha=0.9),
        )

    # IMO 2030 annotation
    ax.text(4000, 5800, 'Bubble size = annual CO2 baseline (Mt)', fontsize=8,
            color='grey', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', fc='#f8f8f8', ec='#ccc', lw=0.8))

    ax.set_xlabel('Route Distance (nautical miles)', fontsize=10)
    ax.set_ylabel('Estimated Annual Voyages', fontsize=10)
    ax.set_title('Corridor Scale: Distance vs Annual Voyages (bubble = total CO2)',
                 fontsize=12, fontweight='bold', pad=10)
    ax.set_xlim(3500, 8200)
    ax.set_ylim(1500, 7000)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f} nm'))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.grid(alpha=0.3)
    _source(ax)
    _save(fig, 'ext_05_voyage_emissions_bubble.png')


# ============================================================================
# ext_06 — FUEL DEPLOYMENT GANTT (TRL + timeline)
# ============================================================================
def chart_06_fuel_gantt():
    df = pd.read_csv(insights_dir / "05_fuel_deployment_status.csv")

    # Unique fuels, sorted by TRL desc
    fuels_meta = df.drop_duplicates('fuel')[['fuel', 'trl_level', 'commercial_status',
                                              'est_cost_usd_per_tonne', 'covers_imo_2030']
                                            ].copy()
    fuels_meta['trl_level'] = pd.to_numeric(fuels_meta['trl_level'], errors='coerce').fillna(5)
    fuels_meta = fuels_meta.sort_values('trl_level', ascending=True)

    # Commercial availability windows (start_year, width_years, notes)
    readiness_windows = {
        'Shore Power':        (2015, 15, 2040, '#2D6A4F'),
        'LNG dual-fuel':      (2015, 15, 2040, '#52B788'),
        'Wind-Assist':        (2022,  8, 2035, '#74C69D'),
        'Bio/e-Methanol':     (2023,  7, 2035, '#E9C46A'),
        'Green Methanol':     (2023,  7, 2035, '#F4A261'),
        'Green Ammonia':      (2027,  6, 2038, '#E63946'),
        'Green Hydrogen':     (2030,  5, 2040, '#9D0208'),
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5),
                                    gridspec_kw={'width_ratios': [1, 2]})

    # LEFT: TRL bar chart
    colors_trl = ['#2D6A4F' if t >= 8 else '#E9C46A' if t >= 6 else '#E63946'
                  for t in fuels_meta['trl_level']]
    bars = ax1.barh(range(len(fuels_meta)), fuels_meta['trl_level'],
                    color=colors_trl, edgecolor='white', lw=1, height=0.6)
    ax1.set_yticks(range(len(fuels_meta)))
    ax1.set_yticklabels(fuels_meta['fuel'], fontsize=9)
    ax1.set_xlabel('Technology Readiness Level (TRL 1-9)', fontsize=9)
    ax1.set_xlim(0, 11)
    ax1.set_title('Fuel TRL', fontsize=10, fontweight='bold')
    ax1.axvline(7, color='#457B9D', lw=1.5, ls='--', alpha=0.7)
    ax1.text(7.1, -0.7, 'Commercial\nthreshold', fontsize=7.5, color='#457B9D')
    for i, (trl, status) in enumerate(zip(fuels_meta['trl_level'],
                                          fuels_meta['commercial_status'])):
        ax1.text(trl + 0.15, i, f'{trl:.0f} — {status}', va='center', fontsize=7.5,
                 color='#333')
    ax1.grid(axis='x', alpha=0.3)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    # RIGHT: Gantt timeline 2020-2050
    years = list(range(2020, 2051))
    ax2.axvspan(2020, 2030, color='#fff7e6', alpha=0.6, zorder=0)
    ax2.axvspan(2030, 2040, color='#e6f4f1', alpha=0.6, zorder=0)
    ax2.axvspan(2040, 2050, color='#e6f0ff', alpha=0.6, zorder=0)
    ax2.text(2025, len(fuels_meta) - 0.1, 'Near-term\n(2020-30)', ha='center',
             fontsize=8, color='#b7791f', fontweight='bold')
    ax2.text(2035, len(fuels_meta) - 0.1, 'Mid-term\n(2030-40)', ha='center',
             fontsize=8, color='#2A9D8F', fontweight='bold')
    ax2.text(2045, len(fuels_meta) - 0.1, 'Long-term\n(2040-50)', ha='center',
             fontsize=8, color='#457B9D', fontweight='bold')

    for i, (_, row) in enumerate(fuels_meta.iterrows()):
        fuel = row['fuel']
        if fuel in readiness_windows:
            start, width, end, color = readiness_windows[fuel]
            ax2.barh(i, width, left=start, color=color, alpha=0.7, height=0.5,
                     edgecolor='white', lw=1)
            ax2.text(start + width / 2, i, f'${row["est_cost_usd_per_tonne"]}/t',
                     ha='center', va='center', fontsize=7.5, color='white',
                     fontweight='bold')
            # Arrow to sustain beyond window
            if end > start + width:
                ax2.annotate('', xy=(end, i), xytext=(start + width, i),
                             arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

    # IMO milestones
    for yr, label in [(2030, 'IMO -30%'), (2040, 'IMO -70%'), (2050, 'Net-zero')]:
        ax2.axvline(yr, color='#1D3557', lw=1.2, ls=':', zorder=5)
        ax2.text(yr, -0.8, label, ha='center', fontsize=7.5, color='#1D3557',
                 fontweight='bold', rotation=0)

    ax2.set_yticks(range(len(fuels_meta)))
    ax2.set_yticklabels(fuels_meta['fuel'], fontsize=9)
    ax2.set_xlim(2018, 2052)
    ax2.set_title('Commercial Deployment Timeline + Cost (USD/tonne)', fontsize=10,
                  fontweight='bold')
    ax2.set_xlabel('Year', fontsize=9)
    ax2.grid(axis='x', alpha=0.3)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    plt.suptitle('Green Fuel Readiness Roadmap — Technology & Deployment Status',
                 fontsize=13, fontweight='bold', y=1.01)
    ax2.annotate(SOURCE_NOTE, xy=(1, -0.16), xycoords='axes fraction',
                 fontsize=7, color='grey', ha='right')
    plt.tight_layout()
    _save(fig, 'ext_06_fuel_deployment_gantt.png')


# ============================================================================
# ext_07 — IMO 2030 GAP PER CORRIDOR
# ============================================================================
def chart_07_imo_gap():
    df_voy = pd.read_csv(insights_dir / "06_annual_voyage_emissions.csv")
    df_sav = pd.read_csv(insights_dir / "02_co2_savings_by_scenario.csv")

    routes_short = [r.replace('Route 1: ', '').replace('Route 2: ', '')
                     .replace('Route 3: ', '') for r in df_voy['corridor']]
    x = np.arange(len(df_voy))
    width = 0.22

    fig, ax = plt.subplots(figsize=(12, 6.5))

    # Bars: current, IMO target, LNG+Wind, Green Ammonia
    baselines = df_voy['co2_annual_baseline_Mt'].values
    imo_targets = (df_voy['imo_2030_target_t'] / 1e6).values

    lng_wind  = np.array([
        df_sav[(df_sav['corridor'] == r) & (df_sav['fuel_scenario'] == 'LNG + Wind-Assist')
               ]['remaining_co2_t'].values[0] / 1e6
        for r in df_voy['corridor']
    ])
    g_ammonia = np.array([
        df_sav[(df_sav['corridor'] == r) & (df_sav['fuel_scenario'] == 'Green Ammonia')
               ]['remaining_co2_t'].values[0] / 1e6
        for r in df_voy['corridor']
    ])

    b1 = ax.bar(x - 1.5*width, baselines,  width, label='Current (2024)',
                color=[C1, C2, C3], alpha=0.9, edgecolor='white', lw=1)
    b2 = ax.bar(x - 0.5*width, imo_targets, width, label='IMO 2030 Target (-30%)',
                color='#1D3557', alpha=0.75, edgecolor='white', lw=1)
    b3 = ax.bar(x + 0.5*width, lng_wind,   width, label='LNG + Wind-Assist (-35%)',
                color='#E9C46A', alpha=0.9, edgecolor='white', lw=1)
    b4 = ax.bar(x + 1.5*width, g_ammonia, width, label='Green Ammonia (-92%)',
                color='#2D6A4F', alpha=0.9, edgecolor='white', lw=1)

    # Value labels on current bars
    for rect, val in zip(b1, baselines):
        ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 2,
                f'{val:.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Gap annotation arrows (current -> IMO target)
    for i, (base, imo) in enumerate(zip(baselines, imo_targets)):
        gap = base - imo
        ax.annotate('', xy=(i - 0.5*width + width/2, imo + 2),
                    xytext=(i - 1.5*width + width/2, base - 2),
                    arrowprops=dict(arrowstyle='fancy', color='#E63946',
                                   fc='#E63946', mutation_scale=15))
        ax.text(i - width, (base + imo) / 2,
                f'-{gap:.0f}\nMt gap',
                ha='center', va='center', fontsize=7.5, color='#E63946',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#E63946', lw=0.8))

    # Corridor-specific targets callout
    g2z_targets = {
        'Shanghai->LA': ('-30%', C1),
        'Rotterdam->Singapore': ('-25%', C2),
        'Australia->East Asia': ('-5%\n(nascent)', C3),
    }
    for i, (route_short, base) in enumerate(zip(routes_short, baselines)):
        target_key = 'Shanghai->LA' if 'Shanghai' in route_short else \
                     'Rotterdam->Singapore' if 'Rotterdam' in route_short else \
                     'Australia->East Asia'
        t_label, t_color = g2z_targets[target_key]
        ax.text(i + 1.5*width + 0.18, baselines[i] * 0.55,
                f'G2Z target:\n{t_label}',
                ha='left', fontsize=7.5, color=t_color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=t_color, lw=0.8))

    ax.set_xticks(x)
    ax.set_xticklabels(routes_short, fontsize=10)
    ax.set_ylabel('CO2 Emissions (Mt / year, 2024 basis)', fontsize=10)
    ax.set_title('2030 IMO Target vs Corridor Commitments vs Fuel Scenarios',
                 fontsize=12, fontweight='bold', pad=12)
    ax.legend(loc='upper right', fontsize=8.5, framealpha=0.9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f} Mt'))
    ax.grid(axis='y', alpha=0.3)
    _source(ax)
    _save(fig, 'ext_07_imo_vs_corridor_gap.png')


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("\n" + "=" * 65)
    print("  SPACEHACK 2026 — EXTERNAL VISUALIZATIONS")
    print("  Generating 7 charts from external_insights/")
    print("=" * 65 + "\n")

    chart_01_maturity()
    chart_02_waterfall()
    chart_03_thetis_fleet()
    chart_04_cii_heatmap()
    chart_05_voyage_bubble()
    chart_06_fuel_gantt()
    chart_07_imo_gap()

    print("\n" + "=" * 65)
    print("  DONE — saved to external_results/")
    print("=" * 65)
    saved = sorted(results_dir.glob("ext_*.png"))
    for f in saved:
        kb = f.stat().st_size / 1024
        print(f"    {f.name:<45} {kb:>6.0f} KB")


if __name__ == '__main__':
    main()
