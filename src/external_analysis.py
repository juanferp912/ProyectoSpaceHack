"""
SpaceHack 2026 — External Data Analysis
=========================================
Reads data/external/ CSVs (from fetch_corridor_data.py) and produces
deeper insight tables in external_insights/.

Outputs (6 CSVs):
  01_corridor_co2_yoy.csv         — Year-over-year CO2 trend per corridor country
  02_co2_savings_by_scenario.csv  — Absolute CO2 saved per corridor × fuel scenario
  03_vessel_cii_gap.csv           — CII compliance gap per vessel type (THETIS vs IMO targets)
  04_corridor_green_maturity.csv  — Composite green readiness score per corridor
  05_fuel_deployment_status.csv   — Fuel type readiness + volume deployed per corridor
  06_annual_voyage_emissions.csv  — Per-voyage and per-nm CO2 estimates per corridor
"""

import sys
import io
import warnings
from pathlib import Path

import pandas as pd
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

# ── paths ────────────────────────────────────────────────────────────────────
workspace        = Path(__file__).parent.parent
ext_data_dir     = workspace / "data" / "external"
ext_insights_dir = workspace / "external_insights"
ext_insights_dir.mkdir(exist_ok=True)

def banner(t): print(f"\n{'='*65}\n  {t}\n{'='*65}")
def ok(m):     print(f"  [OK] {m}")
def info(m):   print(f"       {m}")

# ── load source tables ────────────────────────────────────────────────────────
oecd      = pd.read_csv(ext_data_dir / "oecd_corridor_co2.csv")
thetis    = pd.read_csv(ext_data_dir / "thetis_rotterdam_ships.csv")
g2z       = pd.read_csv(ext_data_dir / "green_corridor_status.csv")
cii       = pd.read_csv(ext_data_dir / "imo_cii_benchmarks.csv")
corr_summ = pd.read_csv(ext_data_dir / "corridor_summary.csv")

# Corridor country groupings (same as fetch script)
CORRIDOR_COUNTRIES = {
    'Route 1: Shanghai -> Los Angeles': {
        'countries': ['CHN', 'USA'],
        'distance_nm': 5400,
        'annual_voyages': 2800,
        'dominant_vessel': 'Container Ship',
        'cii_size': 'Post-Panamax (8k+)',
    },
    'Route 2: Rotterdam -> Singapore': {
        'countries': ['NLD', 'SGP'],
        'distance_nm': 7000,
        'annual_voyages': 3400,
        'dominant_vessel': 'Container Ship',
        'cii_size': 'Panamax (3-8k TEU)',
    },
    'Route 3: Australia -> East Asia': {
        'countries': ['AUS', 'CHN'],
        'distance_nm': 4200,
        'annual_voyages': 5600,
        'dominant_vessel': 'Bulk Carrier',
        'cii_size': 'Capesize (80k+)',
    },
}

FUEL_SCENARIOS = {
    'HFO Baseline':      0.00,
    'LNG':               0.23,
    'Wind-Assist':       0.15,
    'LNG + Wind-Assist': 0.35,
    'Green Methanol':    0.75,
    'Green Ammonia':     0.92,
    'Green Hydrogen':    0.95,
}

# ============================================================================
# 01 — YEAR-OVER-YEAR CO2 TREND
# ============================================================================
banner("01: YEAR-OVER-YEAR CO2 TREND PER CORRIDOR")

oecd['TIME_PERIOD'] = oecd['TIME_PERIOD'].astype(str)
oecd['year'] = oecd['year'].astype(int)

# Annual totals per country
annual = (
    oecd.groupby(['REF_AREA', 'country_label', 'year'])['co2_tonnes_monthly']
    .sum()
    .reset_index()
    .rename(columns={'co2_tonnes_monthly': 'co2_annual'})
)

# YoY % change
annual = annual.sort_values(['REF_AREA', 'year'])
annual['co2_prev_year'] = annual.groupby('REF_AREA')['co2_annual'].shift(1)
annual['yoy_change_pct'] = ((annual['co2_annual'] - annual['co2_prev_year'])
                             / annual['co2_prev_year'] * 100).round(2)

# Tag each country with its corridor
country_to_route = {
    'CHN': 'Routes 1 + 3', 'USA': 'Route 1',
    'NLD': 'Route 2',      'SGP': 'Route 2',
    'AUS': 'Route 3',
}
annual['corridor'] = annual['REF_AREA'].map(country_to_route)

# Corridor-level annual totals (sum both endpoints)
corridor_annual = []
for route, meta in CORRIDOR_COUNTRIES.items():
    grp = oecd[oecd['REF_AREA'].isin(meta['countries'])]
    yr_totals = grp.groupby('year')['co2_tonnes_monthly'].sum().reset_index()
    yr_totals.columns = ['year', 'co2_annual_corridor']
    yr_totals['corridor'] = route
    yr_totals['countries'] = ' + '.join(meta['countries'])
    corridor_annual.append(yr_totals)

corr_yr = pd.concat(corridor_annual, ignore_index=True)
corr_yr = corr_yr.sort_values(['corridor', 'year'])
corr_yr['co2_prev'] = corr_yr.groupby('corridor')['co2_annual_corridor'].shift(1)
corr_yr['yoy_pct']  = ((corr_yr['co2_annual_corridor'] - corr_yr['co2_prev'])
                        / corr_yr['co2_prev'] * 100).round(2)
corr_yr['co2_annual_Gt'] = (corr_yr['co2_annual_corridor'] / 1e9).round(4)

# Only keep complete years (exclude partial 2025)
complete_years = corr_yr[corr_yr['year'] < 2025].copy()

out = ext_insights_dir / "01_corridor_co2_yoy.csv"
complete_years.to_csv(out, index=False)
ok(f"Saved -> {out.name}  ({len(complete_years)} rows)")

for route in CORRIDOR_COUNTRIES:
    sub = complete_years[complete_years['corridor'] == route]
    print(f"\n  [{route}]")
    for _, r in sub.iterrows():
        trend = f"(+{r['yoy_pct']:.1f}%)" if pd.notna(r['yoy_pct']) and r['yoy_pct'] > 0 \
               else (f"({r['yoy_pct']:.1f}%)" if pd.notna(r['yoy_pct']) else "(base year)")
        info(f"  {int(r['year'])}: {r['co2_annual_Gt']:.3f} Gt  {trend}")


# ============================================================================
# 02 — CO2 SAVINGS BY FUEL SCENARIO
# ============================================================================
banner("02: CO2 SAVINGS BY FUEL SCENARIO PER CORRIDOR")

rows = []
for route, meta in CORRIDOR_COUNTRIES.items():
    baseline = oecd[oecd['REF_AREA'].isin(meta['countries'])]['co2_tonnes_monthly'].sum()
    # Use most recent complete year (2024) as the annual baseline
    yr2024 = oecd[
        (oecd['REF_AREA'].isin(meta['countries'])) & (oecd['year'] == 2024)
    ]['co2_tonnes_monthly'].sum()
    annual_base = yr2024 if yr2024 > 0 else baseline / 3  # fallback to 3-year avg

    # CO2 per nm (rough corridor attribution)
    co2_per_nm = annual_base / (meta['annual_voyages'] * meta['distance_nm'])

    for fuel, reduction in FUEL_SCENARIOS.items():
        remaining  = annual_base * (1 - reduction)
        saved      = annual_base * reduction
        rows.append({
            'corridor':           route,
            'countries':          ' + '.join(meta['countries']),
            'fuel_scenario':      fuel,
            'reduction_pct':      round(reduction * 100, 0),
            'annual_baseline_t':  round(annual_base, 0),
            'remaining_co2_t':    round(remaining, 0),
            'co2_saved_t':        round(saved, 0),
            'co2_saved_Mt':       round(saved / 1e6, 2),
            'annual_base_Gt':     round(annual_base / 1e9, 3),
            'co2_per_nm_kg':      round(co2_per_nm / 1e3, 4),  # tonnes/nm -> kg/nm
            'data_year':          2024,
            'source':             'OECD.csv + IMO GHG Study 2020 reduction factors',
        })

df_savings = pd.DataFrame(rows)
out = ext_insights_dir / "02_co2_savings_by_scenario.csv"
df_savings.to_csv(out, index=False)
ok(f"Saved -> {out.name}  ({len(df_savings)} rows = 3 corridors x 7 fuel scenarios)")

print("\n  [KEY SAVINGS — Green Ammonia scenario (2024 annual baseline)]")
top = df_savings[df_savings['fuel_scenario'] == 'Green Ammonia'].sort_values('co2_saved_Mt', ascending=False)
for _, r in top.iterrows():
    info(f"  {r['corridor']:<40}  saves {r['co2_saved_Mt']:>7.1f} Mt CO2/yr  (-{r['reduction_pct']:.0f}%)")


# ============================================================================
# 03 — VESSEL CII COMPLIANCE GAP
# ============================================================================
banner("03: VESSEL CII COMPLIANCE GAP (THETIS vs IMO 2023)")

rows = []
for _, t in thetis.iterrows():
    vtype = t['ship_type']
    actual_eff = t['avg_efficiency_gCO2_dwt_nm']  # from THETIS-MRV 2023

    # Find matching CII rows (may be multiple size categories)
    cii_match = cii[cii['vessel_type'] == vtype]

    for _, c in cii_match.iterrows():
        ref_2023 = c['cii_reference_2023']
        ref_2026 = c['cii_target_2026']
        ref_2030 = c['cii_target_2030']

        # CII grade based on thresholds
        if actual_eff <= c['grading_a_threshold']:
            grade_2023 = 'A'
        elif actual_eff <= ref_2023:
            grade_2023 = 'B'
        elif actual_eff <= c['grading_d_threshold']:
            grade_2023 = 'C'
        elif actual_eff <= c['grading_e_threshold']:
            grade_2023 = 'D'
        else:
            grade_2023 = 'E'

        gap_to_c_pct = ((actual_eff - ref_2023) / ref_2023 * 100) if actual_eff > ref_2023 else 0
        gap_to_2030  = ((actual_eff - ref_2030) / ref_2030 * 100) if actual_eff > ref_2030 else 0
        improvement_needed_pct = max(gap_to_2030, 0)

        rows.append({
            'vessel_type':                vtype,
            'size_category':              c['size_category'],
            'ships_reporting_eu':         t['ships_reporting'],
            'actual_avg_cii_2023':        round(actual_eff, 2),
            'cii_reference_2023':         ref_2023,
            'cii_target_2026':            ref_2026,
            'cii_target_2030':            ref_2030,
            'implied_grade_2023':         grade_2023,
            'gap_to_cii_ref_pct':         round(gap_to_c_pct, 1),
            'gap_to_2030_target_pct':     round(gap_to_2030, 1),
            'improvement_needed_to_2030': f"{improvement_needed_pct:.1f}% reduction in carbon intensity",
            'co2_trend_vs_2022_pct':      t['co2_trend_vs_2022_pct'],
            'total_co2_eu_Mt':            t['total_co2_million_t'],
            'corridor_relevance':         t['corridor_relevance'],
            'source_thetis':              'THETIS-MRV 2023 Annual Report (EMSA)',
            'source_cii':                 'IMO MEPC.338(76) + MEPC.339(76), July 2023',
        })

df_cii = pd.DataFrame(rows)
# Keep most relevant size category per vessel type (representative)
rep_sizes = {
    'Container Ship':  'Post-Panamax (8k+)',
    'Bulk Carrier':    'Capesize (80k+)',
    'Oil Tanker':      'VLCC (200k+)',
    'Chemical Tanker': 'Medium (20-80k DWT)',
    'LNG Carrier':     'Large (>100k m3)',
}
mask = df_cii.apply(
    lambda r: rep_sizes.get(r['vessel_type'], '') == r['size_category']
              or r['vessel_type'] not in rep_sizes,
    axis=1
)
df_cii_rep = df_cii[mask].copy()

out = ext_insights_dir / "03_vessel_cii_gap.csv"
df_cii.to_csv(out, index=False)
ok(f"Saved -> {out.name}  ({len(df_cii)} rows — all size categories)")

out2 = ext_insights_dir / "03b_vessel_cii_rep.csv"
df_cii_rep.to_csv(out2, index=False)
ok(f"Saved -> {out2.name}  ({len(df_cii_rep)} rows — representative sizes only)")

print("\n  [CII COMPLIANCE — dominant corridor vessel types]")
print(f"  {'Vessel Type':<20} {'Actual':<9} {'Ref2023':<9} {'Grade':<7} {'Gap to 2030'}")
print("  " + "-" * 60)
for vt in ['Container Ship', 'Bulk Carrier', 'Oil Tanker', 'LNG Carrier']:
    r = df_cii_rep[df_cii_rep['vessel_type'] == vt]
    if not r.empty:
        r = r.iloc[0]
        info(f"  {r['vessel_type']:<20} {r['actual_avg_cii_2023']:<9.1f} "
             f"{r['cii_reference_2023']:<9.1f} {r['implied_grade_2023']:<7} "
             f"-{r['gap_to_2030_target_pct']:.1f}% needed")


# ============================================================================
# 04 — CORRIDOR GREEN MATURITY SCORE
# ============================================================================
banner("04: CORRIDOR GREEN MATURITY COMPOSITE SCORE")

STAGE_SCORE   = {1: 10, 2: 25, 3: 45, 4: 70, 5: 100}  # G2Z stages 1-5
FUEL_SCORE    = {'Green Hydrogen': 10, 'Green Ammonia': 30,
                 'Green Methanol': 50, 'LNG': 70, 'Shore Power': 80,
                 'Bio/e-Methanol': 55, 'Green Methanol, LNG dual-fuel, Shore Power': 75}

rows = []
for _, r in g2z.iterrows():
    stage     = r['stage_numeric']
    target    = r['co2_reduction_target_pct']
    phase1    = 20 if r['phase1_complete'] else 0
    sigcount  = len(str(r['signatories']).split(','))
    sig_score = min(sigcount * 5, 30)  # up to 30 pts for 6+ signatories
    fuel_key  = str(r['primary_fuels']).split(',')[0].strip()
    fuel_scr  = FUEL_SCORE.get(fuel_key, 20)

    # Target ambition: -5% is weak, -30% is strong
    target_score = min(int(target * 2), 60)

    composite = STAGE_SCORE.get(stage, 0) + phase1 + sig_score + target_score
    composite = min(composite, 100)

    rows.append({
        'spacehack_route':        r['spacehack_route'],
        'corridor_name':          r['corridor_name'],
        'g2z_stage':              r['status'],
        'stage_score_0_100':      STAGE_SCORE.get(stage, 0),
        'phase1_bonus':           phase1,
        'signatory_score':        sig_score,
        'target_ambition_score':  target_score,
        'composite_green_score':  composite,
        'score_label':            ('Leading' if composite >= 75
                                   else 'On Track' if composite >= 45
                                   else 'Lagging'),
        'annual_voyages_est':     r['annual_voyages_est'],
        'distance_nm':            r['distance_nm'],
        'total_voyage_nm_yr':     r['annual_voyages_est'] * r['distance_nm'],
        'primary_fuels':          r['primary_fuels'],
        'co2_target_2030_pct':    target,
        'clydebank_declaration':  r['clydebank_declaration'],
        'source':                 r['source'],
    })

df_maturity = pd.DataFrame(rows).sort_values('composite_green_score', ascending=False)
out = ext_insights_dir / "04_corridor_green_maturity.csv"
df_maturity.to_csv(out, index=False)
ok(f"Saved -> {out.name}  ({len(df_maturity)} corridors)")

print("\n  [COMPOSITE GREEN SCORE — 0 to 100]")
for _, r in df_maturity.iterrows():
    bar = '#' * (r['composite_green_score'] // 5) + '-' * (20 - r['composite_green_score'] // 5)
    info(f"  {r['score_label']:<10}  [{bar}]  {r['composite_green_score']:>3}/100  {r['spacehack_route'][:35]}")


# ============================================================================
# 05 — FUEL DEPLOYMENT STATUS
# ============================================================================
banner("05: FUEL DEPLOYMENT STATUS PER CORRIDOR")

FUEL_READINESS = {
    'Green Methanol':   {'trl': 8, 'status': 'Commercial (early)', 'cost_usd_t': 800,  'imo_2030': True},
    'LNG dual-fuel':    {'trl': 9, 'status': 'Commercial scale',   'cost_usd_t': 550,  'imo_2030': True},
    'Shore Power':      {'trl': 9, 'status': 'Operational',        'cost_usd_t': 0,    'imo_2030': True},
    'Bio/e-Methanol':   {'trl': 7, 'status': 'Early commercial',   'cost_usd_t': 900,  'imo_2030': True},
    'Green Ammonia':    {'trl': 5, 'status': 'Pilot/demo',         'cost_usd_t': 1100, 'imo_2030': False},
    'Green Hydrogen':   {'trl': 4, 'status': 'R&D/Pilot',          'cost_usd_t': 1800, 'imo_2030': False},
    'Wind-Assist':      {'trl': 8, 'status': 'Early commercial',   'cost_usd_t': 200,  'imo_2030': True},
}

rows = []
for _, r in g2z.iterrows():
    fuels = [f.strip() for f in str(r['primary_fuels']).split(',')]
    for fuel in fuels:
        meta = FUEL_READINESS.get(fuel, {})
        vol_2023 = r['green_methanol_bunkered_t_2023'] if 'Methanol' in fuel else 0
        rows.append({
            'spacehack_route':              r['spacehack_route'],
            'fuel':                         fuel,
            'trl_level':                    meta.get('trl', 'N/A'),
            'commercial_status':            meta.get('status', 'Unknown'),
            'est_cost_usd_per_tonne':       meta.get('cost_usd_t', 'N/A'),
            'covers_imo_2030':              meta.get('imo_2030', False),
            'volume_deployed_2023_tonnes':  vol_2023,
            'corridor_g2z_stage':           r['status'],
            'distance_nm':                  r['distance_nm'],
            'annual_voyages':               r['annual_voyages_est'],
            'source':                       r['source'],
        })

df_fuel = pd.DataFrame(rows)
out = ext_insights_dir / "05_fuel_deployment_status.csv"
df_fuel.to_csv(out, index=False)
ok(f"Saved -> {out.name}  ({len(df_fuel)} rows — {len(df_fuel['fuel'].unique())} unique fuels)")

print("\n  [FUEL DEPLOYMENT — volume known]")
deployed = df_fuel[df_fuel['volume_deployed_2023_tonnes'] > 0]
for _, r in deployed.iterrows():
    info(f"  {r['fuel']:<20} {r['volume_deployed_2023_tonnes']:>10,.0f} t  "
         f"deployed  ({r['spacehack_route'][:35]})")


# ============================================================================
# 06 — ANNUAL VOYAGE EMISSIONS
# ============================================================================
banner("06: ANNUAL VOYAGE EMISSIONS PER CORRIDOR")

# 2024 CO2 annual per corridor (most recent complete year)
yr_data = corr_yr[corr_yr['year'] == 2024].copy() if not corr_yr.empty else pd.DataFrame()

rows = []
for route, meta in CORRIDOR_COUNTRIES.items():
    baseline_2024 = oecd[
        (oecd['REF_AREA'].isin(meta['countries'])) & (oecd['year'] == 2024)
    ]['co2_tonnes_monthly'].sum()
    if baseline_2024 == 0:  # fall back to 2023
        baseline_2024 = oecd[
            (oecd['REF_AREA'].isin(meta['countries'])) & (oecd['year'] == 2023)
        ]['co2_tonnes_monthly'].sum()

    annual_voy = meta['annual_voyages']
    dist       = meta['distance_nm']
    total_nm   = annual_voy * dist

    co2_per_voyage = baseline_2024 / annual_voy
    co2_per_nm     = baseline_2024 / total_nm   # tonnes/nm
    co2_per_nm_km  = co2_per_nm / 1.852         # nm -> km

    # Dwell time impact: 4h idle adds ~15t per average vessel (weighted mix)
    dwell_4h_avg_t = 15  # tonnes per vessel per 4h idle

    rows.append({
        'corridor':                       route,
        'countries':                      ' + '.join(meta['countries']),
        'distance_nm':                    dist,
        'annual_voyages_est':             annual_voy,
        'total_route_nm_per_year':        total_nm,
        'co2_annual_baseline_t':          round(baseline_2024, 0),
        'co2_annual_baseline_Mt':         round(baseline_2024 / 1e6, 2),
        'co2_per_voyage_t':               round(co2_per_voyage, 0),
        'co2_per_nm_t':                   round(co2_per_nm, 4),
        'co2_per_km_t':                   round(co2_per_nm_km, 4),
        'co2_per_nm_kg':                  round(co2_per_nm * 1000, 2),
        'dwell_4h_idle_impact_t':         dwell_4h_avg_t,
        'dwell_pct_of_voyage':            round(dwell_4h_avg_t / co2_per_voyage * 100, 3),
        'co2_saved_lng_wind_t_yr':        round(baseline_2024 * 0.35, 0),
        'co2_saved_green_ammonia_t_yr':   round(baseline_2024 * 0.92, 0),
        'imo_2030_target_t':              round(baseline_2024 * 0.70, 0),  # -30% from baseline
        'gap_to_imo_2030_t':              round(baseline_2024 * 0.30, 0),
        'data_year':                      2024,
        'dominant_vessel':                meta['dominant_vessel'],
        'source':                         'OECD.csv + Getting to Zero Coalition voyage estimates',
    })

df_voyage = pd.DataFrame(rows)
out = ext_insights_dir / "06_annual_voyage_emissions.csv"
df_voyage.to_csv(out, index=False)
ok(f"Saved -> {out.name}  ({len(df_voyage)} corridors)")

print("\n  [VOYAGE EMISSIONS — 2024 annual baseline]")
print(f"  {'Corridor':<40} {'CO2/voyage (t)':>15} {'CO2/nm (kg)':>13} {'IMO 2030 gap (Mt)':>18}")
print("  " + "-" * 88)
for _, r in df_voyage.iterrows():
    info(f"  {r['corridor']:<40} {r['co2_per_voyage_t']:>15,.0f} "
         f"{r['co2_per_nm_kg']:>13.1f} "
         f"{r['gap_to_imo_2030_t']/1e6:>18.1f}")


# ============================================================================
# SUMMARY
# ============================================================================
banner("ANALYSIS COMPLETE")

saved = sorted(ext_insights_dir.glob("*.csv"))
print(f"\n  Saved {len(saved)} insight CSVs to external_insights/")
for f in saved:
    kb = f.stat().st_size / 1024
    print(f"    {f.name:<45} {kb:>6.1f} KB")

print("\n  These CSVs feed directly into:")
print("    external_visualizations.py  -> PNGs in external_results/")
print("    gee_export.py update        -> enriched GeoJSON properties")
