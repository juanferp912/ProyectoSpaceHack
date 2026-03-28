"""
SpaceHack - Google Earth Engine Export
Generates GeoJSON + self-contained GEE JavaScript for corridor visualization.

Outputs:
  results/gee/green_corridors.geojson  — Load in geojson.io or GEE
  results/gee/gee_corridors.js         — Paste directly into GEE Code Editor

Usage:
  python src/gee_export.py

Then paste gee_corridors.js into: https://code.earthengine.google.com/
"""

import sys
import io
import json
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================================================
# CONFIGURATION
# ============================================================================

workspace    = Path(__file__).parent.parent
datasets_dir = workspace / "data"
gee_dir      = workspace / "results" / "gee"
gee_dir.mkdir(parents=True, exist_ok=True)

# Green corridor definitions
CORRIDORS = {
    'Shanghai_LA': {
        'name':           'Shanghai → Los Angeles',
        'label':          'Trans-Pacific Green Corridor',
        'start_port':     'Shanghai',
        'start_country':  'CHN',
        'start_coords':   [121.50, 31.22],   # [lon, lat] — GeoJSON convention
        'end_port':       'Los Angeles',
        'end_country':    'USA',
        'end_coords':     [-118.25, 33.75],
        'waypoints':      [[145.0, 40.0], [180.0, 38.0], [-155.0, 25.0]],  # Pacific arc
        'distance_nm':    5400,
        'typical_days':   14,
        'vessel_types':   'Container, Bulk Carrier, Vehicle Carrier',
        'dominant_cargo': 'Consumer goods, electronics, vehicles',
        'color_hex':      '#E63946',
    },
    'Rotterdam_Singapore': {
        'name':           'Rotterdam → Singapore',
        'label':          'Europe-Asia Green Corridor (Suez)',
        'start_port':     'Rotterdam',
        'start_country':  'NLD',
        'start_coords':   [4.48, 51.90],
        'end_port':       'Singapore',
        'end_country':    'SGP',
        'end_coords':     [103.85, 1.28],
        'waypoints':      [[12.0, 37.0], [32.0, 30.0], [43.0, 12.5], [58.0, 22.0], [72.0, 20.0]],  # Med-Suez-Indian Ocean
        'distance_nm':    7000,
        'typical_days':   28,
        'vessel_types':   'Container, Bulk Carrier, Oil Tanker, Chemical Tanker',
        'dominant_cargo': 'Chemicals, petroleum products, general cargo',
        'color_hex':      '#457B9D',
    },
    'Australia_East_Asia': {
        'name':           'Australia → East Asia',
        'label':          'Australia-East Asia Green Corridor',
        'start_port':     'Sydney / Brisbane',
        'start_country':  'AUS',
        'start_coords':   [151.21, -33.87],
        'end_port':       'Shanghai / Yokohama',
        'end_country':    'CHN',
        'end_coords':     [121.50, 31.22],
        'waypoints':      [[153.0, -20.0], [143.0, -5.0], [130.0, 15.0]],  # Torres Strait arc
        'distance_nm':    4200,
        'typical_days':   11,
        'vessel_types':   'Bulk Carrier, LNG Tanker, Oil Tanker, Container',
        'dominant_cargo': 'Iron ore, coal, LNG, grain',
        'color_hex':      '#2A9D8F',
    },
}

# Key port coordinates (from WIP dataset approximate values)
PORTS = {
    'Shanghai':   {'lat': 31.22,  'lon': 121.50, 'country': 'CHN', 'color': '#E63946'},
    'Los Angeles':{'lat': 33.75,  'lon': -118.25,'country': 'USA', 'color': '#F77F00'},
    'Rotterdam':  {'lat': 51.90,  'lon': 4.48,   'country': 'NLD', 'color': '#06A77D'},
    'Singapore':  {'lat': 1.28,   'lon': 103.85, 'country': 'SGP', 'color': '#00B4D8'},
    'Sydney':     {'lat': -33.87, 'lon': 151.21, 'country': 'AUS', 'color': '#8338EC'},
}

# Green fuel reduction factors
FUEL_REDUCTIONS = {
    'HFO (Baseline)':    0.00,
    'LNG':               0.23,
    'LNG + Wind-Assist': 0.35,
    'Green Methanol':    0.75,
    'Green Ammonia':     0.92,
}


# ============================================================================
# DATA LOADING
# ============================================================================

def load_external_insights():
    """
    Load the enriched external_insights/ CSVs produced by external_analysis.py.
    Returns a dict keyed by corridor_key (Shanghai_LA / Rotterdam_Singapore / Australia_East_Asia).
    Falls back gracefully if the files don't exist.
    """
    ext_ins = workspace / "external_insights"
    ext_dat = workspace / "data" / "external"

    result = {k: {} for k in CORRIDORS}
    route_to_key = {
        'Route 1': 'Shanghai_LA',
        'Route 2': 'Rotterdam_Singapore',
        'Route 3': 'Australia_East_Asia',
    }

    # Getting to Zero maturity
    try:
        g2z = pd.read_csv(ext_dat / "green_corridor_status.csv")
        mat = pd.read_csv(ext_ins / "04_corridor_green_maturity.csv")
        for _, row in g2z.iterrows():
            rkey = next((v for k, v in route_to_key.items()
                         if k in str(row['spacehack_route'])), None)
            if rkey:
                mat_row = mat[mat['spacehack_route'].str.contains(rkey.split('_')[0],
                              na=False, case=False)]
                result[rkey]['g2z_stage']              = row['status']
                result[rkey]['g2z_stage_numeric']      = int(row['stage_numeric'])
                result[rkey]['g2z_phase1_complete']    = bool(row['phase1_complete'])
                result[rkey]['g2z_signatories_count']  = len(str(row['signatories']).split(','))
                result[rkey]['annual_voyages_est']      = int(row['annual_voyages_est'])
                result[rkey]['co2_target_2030_pct']    = int(row['co2_reduction_target_pct'])
                result[rkey]['clydebank_declaration']  = bool(row['clydebank_declaration'])
                result[rkey]['fuel_deployed_2023_t']   = int(row['green_methanol_bunkered_t_2023'])
                result[rkey]['key_milestone']          = str(row['key_milestone'])[:120]
                if not mat_row.empty:
                    result[rkey]['composite_green_score'] = int(mat_row.iloc[0]['composite_green_score'])
                    result[rkey]['score_label']           = str(mat_row.iloc[0]['score_label'])
        print("  [EXT] Getting to Zero + Maturity data loaded")
    except Exception as e:
        print(f"  [WARN] G2Z data not available: {e}")

    # Voyage emissions
    try:
        voy = pd.read_csv(ext_ins / "06_annual_voyage_emissions.csv")
        for _, row in voy.iterrows():
            rkey = next((v for k, v in route_to_key.items()
                         if k in str(row['corridor'])), None)
            if rkey:
                result[rkey]['co2_per_voyage_t']            = round(float(row['co2_per_voyage_t']), 0)
                result[rkey]['co2_per_nm_kg']               = round(float(row['co2_per_nm_kg']), 2)
                result[rkey]['total_route_nm_per_year']     = int(row['total_route_nm_per_year'])
                result[rkey]['co2_saved_green_ammonia_t']   = round(float(row['co2_saved_green_ammonia_t_yr']), 0)
                result[rkey]['co2_saved_lng_wind_t']        = round(float(row['co2_saved_lng_wind_t_yr']), 0)
                result[rkey]['gap_to_imo_2030_t']           = round(float(row['gap_to_imo_2030_t']), 0)
                result[rkey]['dwell_4h_impact_t']           = int(row['dwell_4h_idle_impact_t'])
        print("  [EXT] Voyage emissions data loaded")
    except Exception as e:
        print(f"  [WARN] Voyage data not available: {e}")

    # CII compliance for dominant vessel
    try:
        cii = pd.read_csv(ext_ins / "03b_vessel_cii_rep.csv")
        dominant_map = {
            'Shanghai_LA':          'Container Ship',
            'Rotterdam_Singapore':  'Container Ship',
            'Australia_East_Asia':  'Bulk Carrier',
        }
        for rkey, vtype in dominant_map.items():
            row = cii[cii['vessel_type'] == vtype]
            if not row.empty:
                row = row.iloc[0]
                result[rkey]['cii_dominant_vessel']      = vtype
                result[rkey]['cii_actual_2023']          = round(float(row['actual_avg_cii_2023']), 1)
                result[rkey]['cii_ref_2023']             = round(float(row['cii_reference_2023']), 1)
                result[rkey]['cii_grade_2023']           = str(row['implied_grade_2023'])
                result[rkey]['cii_gap_to_2030_pct']      = round(float(row['gap_to_2030_target_pct']), 1)
        print("  [EXT] CII compliance data loaded")
    except Exception as e:
        print(f"  [WARN] CII data not available: {e}")

    # YoY trend
    try:
        yoy = pd.read_csv(ext_ins / "01_corridor_co2_yoy.csv")
        # Get 2024 YoY change per corridor
        for rkey, meta in CORRIDORS.items():
            countries = meta.get('start_country', '') + '_' + meta.get('end_country', '')
            for country in [meta['start_country'], meta['end_country']]:
                row = yoy[(yoy['corridor'].str.contains('Route', na=False)) &
                          (yoy['year'] == 2024)]
                # Match by countries string in the corridor name
                corr_row = yoy[
                    (yoy['countries'].str.contains(meta['start_country'], na=False)) &
                    (yoy['year'] == 2024)
                ]
                if not corr_row.empty:
                    result[rkey]['co2_yoy_2024_pct'] = round(float(corr_row.iloc[0]['yoy_pct']), 1)
                    result[rkey]['co2_annual_2024_Gt'] = round(float(corr_row.iloc[0]['co2_annual_Gt']), 3)
                    break
        print("  [EXT] YoY trend data loaded")
    except Exception as e:
        print(f"  [WARN] YoY data not available: {e}")

    return result


def load_country_co2():
    """Load OECD and compute per-country CO2 stats"""
    df = pd.read_csv(datasets_dir / "OECD.csv", encoding='utf-8', low_memory=False)
    df['CO2_TONNES'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')

    filtered = df[(df['POLLUTANT'] == 'CO2') & (df['VESSEL'] == 'ALL_VESSELS')]

    stats = {}
    for country in ['CHN', 'USA', 'NLD', 'SGP', 'AUS']:
        cd = filtered[filtered['REF_AREA'] == country]
        if len(cd) > 0:
            monthly = cd.groupby('TIME_PERIOD')['CO2_TONNES'].sum()
            cv      = (monthly.std() / monthly.mean() * 100) if monthly.mean() > 0 else 0
            stats[country] = {
                'total_co2':      float(cd['CO2_TONNES'].sum()),
                'avg_monthly_co2': float(monthly.mean()),
                'congestion_cv':  float(cv),
                'congestion_level': 'HIGH' if cv > 20 else ('MODERATE' if cv > 10 else 'LOW'),
            }
        else:
            stats[country] = {
                'total_co2': 0.0, 'avg_monthly_co2': 0.0,
                'congestion_cv': 0.0, 'congestion_level': 'UNKNOWN',
            }

    return stats


# ============================================================================
# GEOJSON EXPORT
# ============================================================================

def build_geojson(country_stats, external=None):
    """Build GeoJSON FeatureCollection with corridors + ports.
    external: dict from load_external_insights() — adds G2Z, CII, voyage data.
    """
    if external is None:
        external = {}
    features = []

    # --- Corridor LineStrings ---
    for corridor_key, corridor in CORRIDORS.items():
        c1 = corridor['start_country']
        c2 = corridor['end_country']

        # CO2 stats for this corridor
        co2_start  = country_stats.get(c1, {}).get('total_co2', 0)
        co2_end    = country_stats.get(c2, {}).get('total_co2', 0)
        co2_total  = co2_start + co2_end
        congestion = country_stats.get(c1, {}).get('congestion_level', 'UNKNOWN')

        # Best near-term green fuel reduction
        co2_reduction_potential_pct = FUEL_REDUCTIONS['LNG + Wind-Assist'] * 100

        # Build route geometry: start -> waypoints -> end
        coordinates = (
            [corridor['start_coords']]
            + corridor.get('waypoints', [])
            + [corridor['end_coords']]
        )

        ext = external.get(corridor_key, {})

        props = {
            # ── OECD baseline ──────────────────────────────────────────────
            "corridor_key":                corridor_key,
            "corridor_name":               corridor['name'],
            "corridor_label":              corridor['label'],
            "start_port":                  corridor['start_port'],
            "start_country":               c1,
            "end_port":                    corridor['end_port'],
            "end_country":                 c2,
            "distance_nm":                 corridor['distance_nm'],
            "typical_days":                corridor['typical_days'],
            "dominant_cargo":              corridor['dominant_cargo'],
            "vessel_types":                corridor['vessel_types'],
            "co2_total_tonnes":            round(co2_total, 0),
            "co2_avg_monthly":             round((co2_start + co2_end) / 40, 0),
            "co2_reduction_potential_pct": co2_reduction_potential_pct,
            "co2_after_lng_wind_tonnes":   round(co2_total * (1 - FUEL_REDUCTIONS['LNG + Wind-Assist']), 0),
            "congestion_level":            congestion,
            "color":                       corridor['color_hex'],
            # ── Getting to Zero Coalition (external) ───────────────────────
            "g2z_stage":                   ext.get('g2z_stage', 'N/A'),
            "g2z_stage_numeric":           ext.get('g2z_stage_numeric', 0),
            "g2z_phase1_complete":         ext.get('g2z_phase1_complete', False),
            "g2z_signatories_count":       ext.get('g2z_signatories_count', 0),
            "g2z_composite_score":         ext.get('composite_green_score', 0),
            "g2z_score_label":             ext.get('score_label', 'N/A'),
            "g2z_co2_target_2030_pct":     ext.get('co2_target_2030_pct', 0),
            "g2z_clydebank":               ext.get('clydebank_declaration', False),
            "g2z_fuel_deployed_2023_t":    ext.get('fuel_deployed_2023_t', 0),
            "g2z_key_milestone":           ext.get('key_milestone', ''),
            # ── Voyage emissions (external) ────────────────────────────────
            "annual_voyages_est":          ext.get('annual_voyages_est', 0),
            "co2_per_voyage_t":            ext.get('co2_per_voyage_t', 0),
            "co2_per_nm_kg":               ext.get('co2_per_nm_kg', 0),
            "co2_yoy_2024_pct":            ext.get('co2_yoy_2024_pct', 0),
            "co2_annual_2024_Gt":          ext.get('co2_annual_2024_Gt', 0),
            "gap_to_imo_2030_t":           ext.get('gap_to_imo_2030_t', 0),
            "co2_saved_green_ammonia_t":   ext.get('co2_saved_green_ammonia_t', 0),
            "dwell_4h_impact_t":           ext.get('dwell_4h_impact_t', 0),
            # ── CII compliance (external) ──────────────────────────────────
            "cii_dominant_vessel":         ext.get('cii_dominant_vessel', ''),
            "cii_actual_2023":             ext.get('cii_actual_2023', 0),
            "cii_ref_2023":                ext.get('cii_ref_2023', 0),
            "cii_grade_2023":              ext.get('cii_grade_2023', 'N/A'),
            "cii_gap_to_2030_pct":         ext.get('cii_gap_to_2030_pct', 0),
        }

        feature = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coordinates},
            "properties": props,
        }
        features.append(feature)

    # --- Port Points ---
    for port_name, port in PORTS.items():
        country    = port['country']
        stats      = country_stats.get(country, {})
        co2_total  = stats.get('total_co2', 0)
        congestion = stats.get('congestion_level', 'UNKNOWN')

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [port['lon'], port['lat']],
            },
            "properties": {
                "port_name":        port_name,
                "country":          country,
                "co2_total_tonnes": round(co2_total, 0),
                "co2_avg_monthly":  round(stats.get('avg_monthly_co2', 0), 0),
                "congestion_level": congestion,
                "congestion_cv_pct": round(stats.get('congestion_cv', 0), 1),
                "color":            port['color'],
                "marker_size":      max(5, min(30, co2_total / 1e11)),  # scaled for display
            },
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "metadata": {
            "title":      "SpaceHack 2026 — Green Shipping Corridors",
            "source":     "OECD Maritime CO2 Emissions (experimental data)",
            "corridors":  list(CORRIDORS.keys()),
            "period":     "2022-2025 (monthly)",
            "note":       "CO2 values are country-level totals used as corridor proxies",
        },
        "features": features,
    }


# ============================================================================
# GEE JAVASCRIPT EXPORT (self-contained)
# ============================================================================

def build_gee_js(geojson_data, country_stats):
    """Generate self-contained GEE JavaScript for the Code Editor"""

    # Inline the GeoJSON as a JS variable
    geojson_str = json.dumps(geojson_data, indent=2)

    # Build corridor stats table for the panel
    stats_rows = ""
    for corridor_key, corridor in CORRIDORS.items():
        c1 = corridor['start_country']
        c2 = corridor['end_country']
        co2  = (country_stats.get(c1, {}).get('total_co2', 0) +
                country_stats.get(c2, {}).get('total_co2', 0))
        saved = co2 * FUEL_REDUCTIONS['LNG + Wind-Assist']
        cname = corridor['name']
        cdays = corridor['typical_days']
        cnm   = f"{corridor['distance_nm']:,}"
        co2_str   = f"{co2/1e12:.2f}T t"
        saved_str = f"{saved/1e12:.2f}T t (-35%)"
        stats_rows += f"    ['<b>{cname}</b>', '{co2_str}', '{saved_str}', '{cdays} days', '{cnm} nm'],\n"

    js = f"""// ============================================================
// SpaceHack 2026 — Green Shipping Corridors
// Google Earth Engine Code Editor script
//
// HOW TO USE:
//   1. Go to https://code.earthengine.google.com/
//   2. Paste this entire script
//   3. Click "Run"
//
// DATA SOURCE: OECD Maritime CO2 Emissions (experimental estimates)
// CORRIDORS:
//   - Shanghai -> Los Angeles  (Trans-Pacific)
//   - Rotterdam -> Singapore   (Europe-Asia via Suez)
//   - Australia -> East Asia   (Iron ore / LNG exports)
// ============================================================

// ---- INLINE DATA (no asset upload needed) ----
var corridorData = {geojson_str};

var corridors = ee.FeatureCollection(corridorData.features
  .filter(function(f) {{ return f.geometry.type === 'LineString'; }})
  .map(function(f) {{ return ee.Feature(f); }})
);

var ports = ee.FeatureCollection(corridorData.features
  .filter(function(f) {{ return f.geometry.type === 'Point'; }})
  .map(function(f) {{ return ee.Feature(f); }})
);

// ---- BASEMAP ----
Map.setOptions('SATELLITE');
Map.setCenter(90, 15, 3);  // Indian Ocean centered view

// ---- CORRIDOR LINES ----
// Color each corridor by its assigned color property
var corridorStyle = {{
  width: 3,
  fillColor: '00000000',
}};

// Paint corridors with their corridor color
var corridorVis = corridors.style({{
  styleProperty: 'color',
  width: 4,
  lineType: 'solid',
}});

Map.addLayer(corridorVis, {{}}, 'Green Corridors', true);

// ---- PORT CIRCLES ----
// Scale circle size by congestion + CO2
var portVis = ports.style({{
  styleProperty: 'color',
  width: 2,
  fillColor: 'FFFFFF80',
  pointSize: 8,
}});

Map.addLayer(portVis, {{}}, 'Key Ports', true);

// ---- CO2 COUNTRY HEAT (approximate) ----
// Use a simple polygon overlay for corridor countries
var countryColors = {{
  'CHN': 'E63946', 'USA': 'F77F00',
  'NLD': '06A77D', 'SGP': '00B4D8', 'AUS': '8338EC',
}};

// ---- PANEL: CORRIDOR STATISTICS ----
var panel = ui.Panel({{
  style: {{
    position: 'bottom-left',
    padding: '10px',
    width: '480px',
    backgroundColor: 'rgba(255,255,255,0.92)',
  }}
}});

var title = ui.Label({{
  value: 'SpaceHack 2026 — Green Shipping Corridors',
  style: {{ fontWeight: 'bold', fontSize: '14px', margin: '0 0 6px 0' }}
}});

var subtitle = ui.Label({{
  value: 'CO2 emissions from OECD maritime data (2022-2025)',
  style: {{ fontSize: '11px', color: '#666', margin: '0 0 10px 0' }}
}});

panel.add(title);
panel.add(subtitle);

// Corridor legend entries
var legendItems = [
  {{ color: '#E63946', name: 'Shanghai -> Los Angeles', nm: '5,400 nm' }},
  {{ color: '#457B9D', name: 'Rotterdam -> Singapore',  nm: '7,000 nm' }},
  {{ color: '#2A9D8F', name: 'Australia -> East Asia',  nm: '4,200 nm' }},
];

legendItems.forEach(function(item) {{
  var row = ui.Panel({{layout: ui.Panel.Layout.flow('horizontal'), style: {{margin: '2px 0'}}}});
  var colorBox = ui.Label({{
    value: '  ',
    style: {{
      backgroundColor: item.color,
      padding: '4px 12px',
      margin: '2px 6px 2px 0',
      border: '1px solid #ccc',
    }}
  }});
  var label = ui.Label(item.name + '  (' + item.nm + ')', {{fontSize: '11px'}});
  row.add(colorBox);
  row.add(label);
  panel.add(row);
}});

panel.add(ui.Label('', {{margin: '6px 0'}}));

// Stats table header
panel.add(ui.Label(
  'Green Transition Potential (LNG + Wind-Assist = -35% CO2):',
  {{ fontWeight: 'bold', fontSize: '11px', margin: '4px 0' }}
));

var statsData = [
{stats_rows}];

statsData.forEach(function(row) {{
  var rowPanel = ui.Panel({{
    layout: ui.Panel.Layout.flow('horizontal'),
    style: {{margin: '1px 0'}}
  }});
  row.forEach(function(cell) {{
    rowPanel.add(ui.Label(cell, {{
      fontSize: '10px',
      margin: '0 4px',
      width: '130px',
    }}));
  }});
  panel.add(rowPanel);
}});

panel.add(ui.Label(
  'Note: CO2 values are country-level OECD totals (corridor proxies)',
  {{ fontSize: '9px', color: '#999', margin: '8px 0 0 0' }}
));

Map.add(panel);

print('Green Corridors loaded:', corridors.size(), 'corridors,', ports.size(), 'ports');
"""
    return js


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print("SPACEHACK - GENERATING GEE EXPORTS")
    print("=" * 80)

    print("\nLoading OECD CO2 data...")
    country_stats = load_country_co2()

    print(f"  OK CO2 stats computed for: {', '.join(country_stats.keys())}")
    for country, stats in country_stats.items():
        print(f"  {country}: {stats['total_co2']/1e9:.1f}B tonnes total, "
              f"congestion={stats['congestion_level']} ({stats['congestion_cv']:.1f}% CV)")

    print("\nLoading external insights (G2Z, CII, voyage, YoY)...")
    external = load_external_insights()
    ext_fields = sum(len(v) for v in external.values())
    print(f"  OK {ext_fields} enrichment fields loaded across {len(external)} corridors")

    print("\nBuilding GeoJSON (enriched with external data)...")
    geojson_data = build_geojson(country_stats, external)
    geojson_path = gee_dir / "green_corridors.geojson"
    with open(geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, indent=2, ensure_ascii=False)
    print(f"  OK Saved: {geojson_path}")
    n_lines  = sum(1 for f in geojson_data['features'] if f['geometry']['type'] == 'LineString')
    n_points = sum(1 for f in geojson_data['features'] if f['geometry']['type'] == 'Point')
    n_props  = len(geojson_data['features'][0]['properties']) if geojson_data['features'] else 0
    print(f"     {n_lines} corridor lines + {n_points} port points | {n_props} properties per corridor")

    print("\nBuilding GEE JavaScript...")
    js_code  = build_gee_js(geojson_data, country_stats)
    js_path  = gee_dir / "gee_corridors.js"
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_code)
    print(f"  OK Saved: {js_path}")
    print(f"     Self-contained — no asset upload needed")

    print("\n" + "=" * 80)
    print("GEE EXPORT COMPLETE")
    print("=" * 80)
    print("\nUsage:")
    print("  GeoJSON: Open results/gee/green_corridors.geojson in geojson.io or QGIS")
    print("  GEE JS:  Paste results/gee/gee_corridors.js into https://code.earthengine.google.com/")
    print("\nThe GEE script is fully self-contained — no Google Cloud asset upload required.")


if __name__ == "__main__":
    main()
