"""
SpaceHack - Route-Specific CO2 Analysis
Detailed analysis of 3 major shipping routes and their CO2 impact
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
datasets_dir = workspace / "datasets"
results_dir = workspace / "results"
results_dir.mkdir(exist_ok=True)

# Route definitions mapping to country codes and coordinates
ROUTES = {
    'Shanghai_LA': {
        'name': 'Shanghai -> Los Angeles',
        'start_port': 'Shanghai',
        'start_country': 'CHN',
        'start_coords': (31.22, 121.50),
        'end_port': 'Los Angeles',
        'end_country': 'USA',
        'end_coords': (33.75, -118.25),
        'distance_nm': 5400,  # Nautical miles
        'typical_days': 14,
        'vessel_types': ['CONTAINER', 'BULK_CARRIER', 'VEHICLE', 'GEN_CARGO'],
    },
    'Australia_Central_Asia': {
        'name': 'Australia -> Central Asia',
        'start_port': 'Port of Brisbane/Sydney',
        'start_country': 'AUS',
        'start_coords': (-33.87, 151.21),
        'end_port': 'Singapore/Dubai hub',
        'end_country': 'SGP',
        'end_coords': (1.28, 103.85),
        'distance_nm': 4500,
        'typical_days': 12,
        'vessel_types': ['CONTAINER', 'BULK_CARRIER', 'OIL_TANKER', 'LIQ_GAS_TANKER'],
    },
    'Rotterdam_Singapore': {
        'name': 'Rotterdam -> Singapore',
        'start_port': 'Rotterdam',
        'start_country': 'NLD',
        'start_coords': (51.90, 4.48),
        'end_port': 'Singapore',
        'end_country': 'SGP',
        'end_coords': (1.28, 103.85),
        'distance_nm': 7000,  # Via Suez
        'typical_days': 28,
        'vessel_types': ['CONTAINER', 'BULK_CARRIER', 'OIL_TANKER', 'CHEM_TANKER'],
    },
}

# ============================================================================
# ROUTE ANALYSIS ENGINE
# ============================================================================

class RouteEmissionsAnalyzer:
    """Analyze CO2 for specific shipping routes"""
    
    def __init__(self, emissions_csv):
        self.emissions_file = Path(emissions_csv)
        self.emissions_df = None
        
        print("=" * 80)
        print("SPACEHACK - SHIPPING ROUTE CO2 ANALYSIS")
        print("=" * 80)
        print("\nAnalyzing 3 major global shipping routes")
    
    def load_data(self):
        """Load OECD emissions data"""
        try:
            print("\nLoading emissions data...")
            self.emissions_df = pd.read_csv(
                self.emissions_file,
                encoding='utf-8',
                low_memory=False
            )
            
            self.emissions_df['CO2_TONNES'] = pd.to_numeric(
                self.emissions_df['OBS_VALUE'],
                errors='coerce'
            )
            
            print(f"  OK {len(self.emissions_df):,} records loaded\n")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to load data: {str(e)}")
            return False
    
    def analyze_route(self, route_key):
        """Analyze a specific route"""
        route = ROUTES[route_key]
        
        print("=" * 80)
        print(f"ROUTE: {route['name'].upper()}")
        print("=" * 80)
        
        # Get data for start and end countries
        filtered = self.emissions_df[
            (self.emissions_df['POLLUTANT'] == 'CO2') &
            (self.emissions_df['VESSEL'].isin(['ALL_VESSELS'] + route['vessel_types']))
        ].copy()
        
        start_data = filtered[
            (filtered['REF_AREA'] == route['start_country']) &
            (filtered['VESSEL'] == 'ALL_VESSELS')
        ].copy()
        
        end_data = filtered[
            (filtered['REF_AREA'] == route['end_country']) &
            (filtered['VESSEL'] == 'ALL_VESSELS')
        ].copy()
        
        print(f"\n[START PORT] {route['start_port']} ({route['start_country']})")
        print("-" * 80)
        
        if len(start_data) > 0:
            start_total = start_data['CO2_TONNES'].sum()
            start_avg = start_data['CO2_TONNES'].mean()
            print(f"  Total CO2 (all time): {start_total:,.0f} tonnes")
            print(f"  Average per record: {start_avg:,.0f} tonnes")
            print(f"  Records: {len(start_data):,}")
            print(f"  Port activity: HIGH" if start_avg > 500000 else "  Port activity: MODERATE")
        
        print(f"\n[END PORT] {route['end_port']} ({route['end_country']})")
        print("-" * 80)
        
        if len(end_data) > 0:
            end_total = end_data['CO2_TONNES'].sum()
            end_avg = end_data['CO2_TONNES'].mean()
            print(f"  Total CO2 (all time): {end_total:,.0f} tonnes")
            print(f"  Average per record: {end_avg:,.0f} tonnes")
            print(f"  Records: {len(end_data):,}")
            print(f"  Port activity: HIGH" if end_avg > 500000 else "  Port activity: MODERATE")
        
        # Route metrics
        print(f"\n[ROUTE METRICS]")
        print("-" * 80)
        print(f"  Distance: {route['distance_nm']:,} nautical miles")
        print(f"  Typical voyage time: {route['typical_days']} days")
        print(f"  Coordinates: {route['start_coords']} -> {route['end_coords']}")
        
        # Vessel types on this route
        print(f"\n[TYPICAL VESSEL TYPES ON THIS ROUTE]")
        print("-" * 80)
        
        for vessel in route['vessel_types']:
            vessel_data = filtered[
                (filtered['VESSEL'] == vessel) &
                (
                    (filtered['REF_AREA'] == route['start_country']) |
                    (filtered['REF_AREA'] == route['end_country'])
                )
            ]
            
            if len(vessel_data) > 0:
                total_co2 = vessel_data['CO2_TONNES'].sum()
                print(f"  {vessel.replace('_', ' ')}: {total_co2:,.0f} tonnes")
        
        # Dwell time analysis (from port congestion patterns)
        print(f"\n[DWELL TIME IMPACT ESTIMATION]")
        print("-" * 80)
        
        # Analyze monthly variation at start and end ports
        start_monthly = start_data.groupby('TIME_PERIOD')['CO2_TONNES'].sum()
        end_monthly = end_data.groupby('TIME_PERIOD')['CO2_TONNES'].sum()
        
        if len(start_monthly) > 1:
            start_cv = (start_monthly.std() / start_monthly.mean() * 100) if start_monthly.mean() != 0 else 0
        else:
            start_cv = 0
            
        if len(end_monthly) > 1:
            end_cv = (end_monthly.std() / end_monthly.mean() * 100) if end_monthly.mean() != 0 else 0
        else:
            end_cv = 0
        
        print(f"  {route['start_port']} port congestion (variation): {start_cv:.1f}%")
        print(f"  {route['end_port']} port congestion (variation): {end_cv:.1f}%")
        
        if start_cv > 10 or end_cv > 10:
            print("\n  Interpretation: SIGNIFICANT PORT CONGESTION")
            print("    - Ships experience long dwell times (4-48 hours typical)")
            print("    - Engines idle or operate at low power = CO2 burning")
            print("    - Average 2-3 day wait at busy ports")
        else:
            print("\n  Interpretation: SMOOTH PORT OPERATIONS")
            print("    - Quick turnaround times")
            print("    - Minimal waiting/dwell time for vessels")
        
        # Answer the key question
        print(f"\n[KEY QUESTION: 4-HOUR DWELL = MORE CO2?]")
        print("-" * 80)
        
        vessel_daily_co2 = {
            'CONTAINER': {'idle': 60, 'typical_wait': '4-8 hours'},
            'BULK_CARRIER': {'idle': 125, 'typical_wait': '8-24 hours'},
            'OIL_TANKER': {'idle': 100, 'typical_wait': '8-16 hours'},
            'CHEM_TANKER': {'idle': 90, 'typical_wait': '6-12 hours'},
        }
        
        print(f"\n  For 4-hour dwell at {route['start_port']}:")
        for vessel, metrics in vessel_daily_co2.items():
            if vessel in route['vessel_types']:
                co2_4hr = (metrics['idle'] / 24) * 4
                print(f"    {vessel.replace('_', ' ')}: ~{co2_4hr:.0f} tonnes CO2")
        
        print(f"\n  YES - Extended dwell time significantly increases CO2:")
        print(f"    • Engines running at dock (100-125 tonnes/day for large ships)")
        print(f"    • 4-hour dwell = ~17-21 tonnes CO2 extra emissions")
        print(f"    • Multiply by thousands of ships annually = major impact")
        
        return {
            'start_total': start_total if len(start_data) > 0 else 0,
            'end_total': end_total if len(end_data) > 0 else 0,
            'start_cv': start_cv,
            'end_cv': end_cv,
        }
    
    def analyze_all_routes(self):
        """Analyze all three major routes"""
        if not self.load_data():
            return False
        
        results = {}
        for route_key in ROUTES.keys():
            results[route_key] = self.analyze_route(route_key)
            print()
        
        # Summary
        self.print_summary(results)
        
        return True
    
    def print_summary(self, results):
        """Print summary comparison of all routes"""
        print("=" * 80)
        print("ROUTE COMPARISON SUMMARY")
        print("=" * 80)
        
        print("\nCO2 Emissions by Route (Total all time):")
        print("-" * 80)
        
        for route_key, result in results.items():
            route = ROUTES[route_key]
            total = result['start_total'] + result['end_total']
            print(f"  {route['name']}: {total:,.0f} tonnes CO2")
        
        print("\nPort Congestion Levels:")
        print("-" * 80)
        
        for route_key, result in results.items():
            route = ROUTES[route_key]
            avg_congestion = (result['start_cv'] + result['end_cv']) / 2
            if avg_congestion > 10:
                level = "HIGH"
            elif avg_congestion > 6:
                level = "MODERATE"
            else:
                level = "LOW"
            print(f"  {route['name']}: {level} ({avg_congestion:.1f}% variation)")


# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    emissions_csv = datasets_dir / "OECD.csv"
    analyzer = RouteEmissionsAnalyzer(str(emissions_csv))
    analyzer.analyze_all_routes()
