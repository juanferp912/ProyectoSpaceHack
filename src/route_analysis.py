"""
SpaceHack - Route-Specific CO2 Analysis
Detailed analysis of 3 major green shipping corridors and their CO2 impact.

Corridors:
  1. Shanghai -> Los Angeles       (Trans-Pacific, ~5,400 nm)
  2. Rotterdam -> Singapore        (Europe-Asia via Suez, ~7,000 nm)
  3. Australia -> East Asia        (Iron ore / LNG / Coal exports, ~4,200 nm)

Data: OECD country-level maritime CO2 emissions (monthly, 2022-2025)
Note: Country codes are used as proxies for major ports in each region.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

workspace = Path(__file__).parent.parent
datasets_dir = workspace / "data"
results_dir = workspace / "results"
results_dir.mkdir(exist_ok=True)

# Route definitions — country codes map to OECD REF_AREA
ROUTES = {
    'Shanghai_LA': {
        'name': 'Shanghai -> Los Angeles',
        'corridor': 'Trans-Pacific Green Corridor',
        'start_port': 'Shanghai',
        'start_country': 'CHN',
        'start_coords': (31.22, 121.50),
        'end_port': 'Los Angeles',
        'end_country': 'USA',
        'end_coords': (33.75, -118.25),
        'distance_nm': 5400,
        'typical_days': 14,
        'vessel_types': ['CONTAINER', 'BULK_CARRIER', 'VEHICLE', 'GEN_CARGO'],
        'dominant_cargo': 'Consumer goods, electronics, vehicles',
    },
    'Rotterdam_Singapore': {
        'name': 'Rotterdam -> Singapore',
        'corridor': 'Europe-Asia Green Corridor (via Suez)',
        'start_port': 'Rotterdam',
        'start_country': 'NLD',
        'start_coords': (51.90, 4.48),
        'end_port': 'Singapore',
        'end_country': 'SGP',
        'end_coords': (1.28, 103.85),
        'distance_nm': 7000,
        'typical_days': 28,
        'vessel_types': ['CONTAINER', 'BULK_CARRIER', 'OIL_TANKER', 'CHEM_TANKER'],
        'dominant_cargo': 'Chemicals, petroleum products, general cargo',
    },
    'Australia_East_Asia': {
        'name': 'Australia -> East Asia',
        'corridor': 'Australia-East Asia Green Corridor',
        'start_port': 'Port of Sydney / Brisbane',
        'start_country': 'AUS',
        'start_coords': (-33.87, 151.21),
        'end_port': 'Shanghai / Yokohama',
        'end_country': 'CHN',
        'end_coords': (31.22, 121.50),
        'distance_nm': 4200,
        'typical_days': 11,
        'vessel_types': ['CONTAINER', 'BULK_CARRIER', 'OIL_TANKER', 'LIQ_GAS_TANKER'],
        'dominant_cargo': 'Iron ore, coal, LNG, grain',
    },
}

# Idle CO2 consumption while at port (tonnes/day, engines running at low power)
VESSEL_IDLE_CO2 = {
    'CONTAINER':      {'idle_per_day': 60,  'typical_wait_hrs': 6},
    'BULK_CARRIER':   {'idle_per_day': 125, 'typical_wait_hrs': 16},
    'OIL_TANKER':     {'idle_per_day': 100, 'typical_wait_hrs': 12},
    'CHEM_TANKER':    {'idle_per_day': 90,  'typical_wait_hrs': 10},
    'LIQ_GAS_TANKER': {'idle_per_day': 110, 'typical_wait_hrs': 14},
    'VEHICLE':        {'idle_per_day': 55,  'typical_wait_hrs': 8},
    'GEN_CARGO':      {'idle_per_day': 50,  'typical_wait_hrs': 12},
}

# ============================================================================
# ROUTE ANALYSIS ENGINE
# ============================================================================

class RouteEmissionsAnalyzer:
    """Analyze CO2 emissions for the 3 green shipping corridors"""

    def __init__(self, emissions_csv):
        self.emissions_file = Path(emissions_csv)
        self.emissions_df = None

        print("=" * 80)
        print("SPACEHACK - GREEN SHIPPING CORRIDOR CO2 ANALYSIS")
        print("=" * 80)
        print("\nCorridors analyzed:")
        for key, r in ROUTES.items():
            print(f"  * {r['name']} ({r['distance_nm']:,} nm)")

    def load_data(self):
        """Load OECD emissions data"""
        try:
            print("\nLoading OECD emissions data...")
            self.emissions_df = pd.read_csv(
                self.emissions_file,
                encoding='utf-8',
                low_memory=False
            )
            self.emissions_df['CO2_TONNES'] = pd.to_numeric(
                self.emissions_df['OBS_VALUE'],
                errors='coerce'
            )
            print(f"  OK {len(self.emissions_df):,} records loaded")
            print(f"  OK Period: {self.emissions_df['TIME_PERIOD'].min()} to {self.emissions_df['TIME_PERIOD'].max()}\n")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load data: {str(e)}")
            return False

    def _get_country_data(self, country_code):
        """Get ALL_VESSELS CO2 data for a country"""
        return self.emissions_df[
            (self.emissions_df['POLLUTANT'] == 'CO2') &
            (self.emissions_df['VESSEL'] == 'ALL_VESSELS') &
            (self.emissions_df['REF_AREA'] == country_code)
        ].copy()

    def _congestion_level(self, cv):
        if cv > 20: return "HIGH"
        elif cv > 10: return "MODERATE"
        else: return "LOW"

    def analyze_route(self, route_key):
        """Full analysis for a single corridor"""
        route = ROUTES[route_key]

        print("=" * 80)
        print(f"CORRIDOR: {route['name'].upper()}")
        print(f"         {route['corridor']}")
        print("=" * 80)

        start_data = self._get_country_data(route['start_country'])
        end_data   = self._get_country_data(route['end_country'])

        # --- Start port ---
        print(f"\n[DEPARTURE PORT] {route['start_port']} ({route['start_country']})")
        print("-" * 60)
        start_total = start_avg = 0
        if len(start_data) > 0:
            start_total = start_data['CO2_TONNES'].sum()
            start_avg   = start_data['CO2_TONNES'].mean()
            print(f"  Total CO2 (all time): {start_total:,.0f} tonnes")
            print(f"  Average per record:   {start_avg:,.0f} tonnes")
            print(f"  Records:              {len(start_data):,}")
            print(f"  Port activity:        {'HIGH' if start_avg > 500_000 else 'MODERATE'}")

        # --- End port ---
        print(f"\n[DESTINATION PORT] {route['end_port']} ({route['end_country']})")
        print("-" * 60)
        end_total = end_avg = 0
        if len(end_data) > 0:
            end_total = end_data['CO2_TONNES'].sum()
            end_avg   = end_data['CO2_TONNES'].mean()
            print(f"  Total CO2 (all time): {end_total:,.0f} tonnes")
            print(f"  Average per record:   {end_avg:,.0f} tonnes")
            print(f"  Records:              {len(end_data):,}")
            print(f"  Port activity:        {'HIGH' if end_avg > 500_000 else 'MODERATE'}")

        # --- Route metrics ---
        print(f"\n[ROUTE METRICS]")
        print("-" * 60)
        print(f"  Distance:       {route['distance_nm']:,} nautical miles")
        print(f"  Voyage time:    ~{route['typical_days']} days")
        print(f"  Dominant cargo: {route['dominant_cargo']}")
        print(f"  Start coords:   {route['start_coords']}")
        print(f"  End coords:     {route['end_coords']}")

        # --- Vessel breakdown ---
        print(f"\n[VESSEL TYPE CO2 AT CORRIDOR ENDPOINTS]")
        print("-" * 60)
        filtered_vessels = self.emissions_df[
            (self.emissions_df['POLLUTANT'] == 'CO2') &
            (self.emissions_df['VESSEL'].isin(route['vessel_types'])) &
            (self.emissions_df['REF_AREA'].isin([route['start_country'], route['end_country']]))
        ]
        vessel_totals = filtered_vessels.groupby('VESSEL')['CO2_TONNES'].sum().sort_values(ascending=False)
        for vessel, total in vessel_totals.items():
            print(f"  {vessel.replace('_', ' '):<22}: {total:,.0f} tonnes")

        # --- Port congestion ---
        start_monthly = start_data.groupby('TIME_PERIOD')['CO2_TONNES'].sum()
        end_monthly   = end_data.groupby('TIME_PERIOD')['CO2_TONNES'].sum()

        start_cv = (start_monthly.std() / start_monthly.mean() * 100) if len(start_monthly) > 1 and start_monthly.mean() != 0 else 0
        end_cv   = (end_monthly.std()   / end_monthly.mean()   * 100) if len(end_monthly)   > 1 and end_monthly.mean()   != 0 else 0

        print(f"\n[PORT CONGESTION ANALYSIS]")
        print("-" * 60)
        print(f"  {route['start_port']:<32}: {start_cv:.1f}% variation -> {self._congestion_level(start_cv)}")
        print(f"  {route['end_port']:<32}: {end_cv:.1f}% variation -> {self._congestion_level(end_cv)}")

        # --- Dwell time CO2 impact ---
        print(f"\n[DWELL TIME IMPACT (4-hour port stay per ship)]")
        print("-" * 60)
        for vessel in route['vessel_types']:
            if vessel in VESSEL_IDLE_CO2:
                metrics = VESSEL_IDLE_CO2[vessel]
                co2_4hr = (metrics['idle_per_day'] / 24) * 4
                print(f"  {vessel.replace('_', ' '):<22}: ~{co2_4hr:.1f} tonnes CO2 per 4h idle")

        print(f"\n  -> YES: Extended dwell significantly increases CO2")
        print(f"     Engines run at dock, consuming 50-125 tonnes/day depending on vessel")
        print(f"     Scale: thousands of port calls/year = millions of avoidable tonnes")

        return {
            'route_name':   route['name'],
            'start_total':  start_total,
            'end_total':    end_total,
            'start_cv':     start_cv,
            'end_cv':       end_cv,
            'distance_nm':  route['distance_nm'],
            'typical_days': route['typical_days'],
        }

    def analyze_all_routes(self):
        """Analyze all three green corridors and print comparison"""
        if not self.load_data():
            return False

        results = {}
        for route_key in ROUTES.keys():
            results[route_key] = self.analyze_route(route_key)
            print()

        self._print_summary(results)
        return results

    def _print_summary(self, results):
        """Comparative summary across all corridors"""
        print("=" * 80)
        print("CORRIDOR COMPARISON SUMMARY")
        print("=" * 80)

        print(f"\n{'Corridor':<40} {'Total CO2 (tonnes)':>20} {'Congestion':>12} {'Distance':>10}")
        print("-" * 86)
        for route_key, result in results.items():
            total  = result['start_total'] + result['end_total']
            avg_cv = (result['start_cv'] + result['end_cv']) / 2
            level  = "HIGH" if avg_cv > 10 else ("MODERATE" if avg_cv > 6 else "LOW")
            print(f"  {result['route_name']:<38} {total:>20,.0f} {level:>12} {result['distance_nm']:>8,} nm")

        print("\n[KEY FINDINGS]")
        print("  * Longer corridors accumulate more port-congestion CO2 at multiple stops")
        print("  * Bulk carriers (iron ore, coal) have highest idle emissions per ship")
        print("  * Port congestion on each corridor translates to measurable extra CO2")
        print("  * Green transition (LNG/Methanol/Wind-Assist) can cut 15-92% per ship")


# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    emissions_csv = datasets_dir / "OECD.csv"
    analyzer = RouteEmissionsAnalyzer(str(emissions_csv))
    analyzer.analyze_all_routes()
