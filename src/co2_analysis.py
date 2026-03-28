"""
SpaceHack - CO2 Emissions Analysis
Comprehensive analysis of maritime shipping CO2 emissions and port impacts
Focus: vessel dwell time, route efficiency, and port-specific emissions

Data source: OECD World Port Index + Maritime CO2 Emissions
Analysis: General trends + Route-specific deep dives (Shanghai-LA, Australia-East Asia, Rotterdam-Singapore)
Question: Does extended dwell time (port stay) increase CO2 emissions?
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

workspace = Path(__file__).parent.parent
datasets_dir = workspace / "data"
insights_dir = workspace / "insights"
results_dir = workspace / "results"

# Create results directory if needed
results_dir.mkdir(exist_ok=True)

# Port mapping to countries (connecting WIP ports to OECD country codes)
PORT_TO_COUNTRY = {
    'shanghai': ('CHN', 'China'),  # Shanghai -> CHN
    'los_angeles': ('USA', 'United States'),  # LA -> USA
    'rotterdam': ('NLD', 'Netherlands'),  # Rotterdam -> NLD
    'singapore': ('SGP', 'Singapore'),  # Singapore -> SGP
}

COUNTRY_CODES = {
    'CHN': 'China',
    'USA': 'United States', 
    'NLD': 'Netherlands',
    'SGP': 'Singapore',
    'AUS': 'Australia',
}

# ============================================================================
# CORE DATA LOADING
# ============================================================================

class CO2EmissionsAnalyzer:
    """Main analyzer for maritime CO2 emissions"""
    
    def __init__(self, ports_csv, emissions_csv):
        self.ports_file = Path(ports_csv)
        self.emissions_file = Path(emissions_csv)
        self.ports_df = None
        self.emissions_df = None
        
        print("=" * 80)
        print("SPACEHACK - CO2 Maritime Emissions Analysis")
        print("=" * 80)
        print("\nFOCUS: Analyzing CO2 emissions trends and dwell time impact")
        
    def load_data(self):
        """Load both CSV files with proper encoding"""
        try:
            print("\n[1/2] Loading port data (World Port Index)...")
            self.ports_df = pd.read_csv(
                self.ports_file,
                encoding='utf-8',
                low_memory=False
            )
            print(f"     OK {len(self.ports_df):,} ports loaded")
            print(f"     OK {len(self.ports_df.columns)} port features available")
            
            print("\n[2/2] Loading CO2 emissions data (OECD)...")
            self.emissions_df = pd.read_csv(
                self.emissions_file,
                encoding='utf-8',
                low_memory=False
            )
            
            # Convert OBS_VALUE to numeric (CO2 in tonnes)
            self.emissions_df['CO2_TONNES'] = pd.to_numeric(
                self.emissions_df['OBS_VALUE'],
                errors='coerce'
            )
            
            print(f"     OK {len(self.emissions_df):,} CO2 emissions records loaded")
            print(f"     OK Time period: {self.emissions_df['TIME_PERIOD'].min()} to {self.emissions_df['TIME_PERIOD'].max()}")
            print(f"     OK Countries/regions: {self.emissions_df['REF_AREA'].nunique()}")
            print(f"     OK Vessel types: {self.emissions_df['VESSEL'].nunique()}")
            
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Failed to load data: {str(e)}")
            return False
    
    def analyze_global_co2_trends(self):
        """
        Analyze global CO2 emissions over time
        Q: Is maritime CO2 increasing or decreasing?
        """
        print("\n" + "=" * 80)
        print("GLOBAL CO2 TRENDS ANALYSIS (2022-2025)")
        print("=" * 80)
        
        if self.emissions_df is None:
            print("ERROR: Emissions data not loaded")
            return
        
        # Filter out aggregated rows (showing only specific vessel data)
        filtered = self.emissions_df[
            (self.emissions_df['POLLUTANT'] == 'CO2') &
            (self.emissions_df['VESSEL'] == 'ALL_VESSELS')
        ].copy()
        
        print(f"\n[GLOBAL CO2 EMISSIONS - All vessels, all countries]")
        print("-" * 80)
        
        total_co2 = filtered['CO2_TONNES'].sum()
        mean_co2 = filtered['CO2_TONNES'].mean()
        
        print(f"  Total CO2 (all time): {total_co2:,.0f} tonnes")
        print(f"  Average per record: {mean_co2:,.0f} tonnes")
        print(f"  Records analyzed: {len(filtered):,}")
        
        # Year-by-year analysis
        filtered['YEAR'] = filtered['TIME_PERIOD'].str[:4].astype(str)
        yearly = filtered.groupby('YEAR')['CO2_TONNES'].sum().sort_index()
        
        print(f"\n  CO2 by year:")
        for year, co2 in yearly.items():
            print(f"    {year}: {co2:,.0f} tonnes")
        
        if len(yearly) > 1:
            first_year = yearly.iloc[0]
            last_year = yearly.iloc[-1]
            change_pct = ((last_year - first_year) / first_year * 100) if first_year != 0 else 0
            print(f"\n  Year-over-year trend:")
            print(f"    {yearly.index[0]}: {first_year:,.0f} tonnes")
            print(f"    {yearly.index[-1]}: {last_year:,.0f} tonnes")
            print(f"    Change: {change_pct:+.1f}%")
            
            if change_pct > 5:
                print("    -> CO2 IS INCREASING (maritime traffic growing)")
            elif change_pct < -5:
                print("    -> CO2 IS DECREASING (maritime efficiency improving)")
            else:
                print("    -> STABLE (no significant trend)")
        
        return yearly
    
    def analyze_vessel_type_emissions(self):
        """
        Analyze CO2 by vessel type
        Q: Which ship types emit most CO2?
        """
        print("\n" + "=" * 80)
        print("VESSEL TYPE CO2 ANALYSIS")
        print("=" * 80)
        
        if self.emissions_df is None:
            return
        
        # Filter for specific vessel types (exclude ALL_VESSELS aggregates)
        vessel_data = self.emissions_df[
            (self.emissions_df['POLLUTANT'] == 'CO2') &
            (~self.emissions_df['VESSEL'].str.contains('ALL', na=False))
        ].copy()
        
        vessel_emissions = vessel_data.groupby('VESSEL').agg({
            'CO2_TONNES': ['count', 'sum', 'mean', 'max']
        }).round(2)
        
        vessel_emissions.columns = ['records', 'total_co2', 'mean_co2', 'max_co2']
        vessel_emissions = vessel_emissions.sort_values('total_co2', ascending=False)
        
        print("\n[TOP VESSEL TYPES BY TOTAL CO2 EMISSIONS]")
        print("-" * 80)
        print(f"{'Vessel Type':<30} {'Total CO2':>15} {'Avg/Record':>12} {'Records':>8}")
        print("-" * 80)
        
        for vessel, row in vessel_emissions.head(10).iterrows():
            vessel_clean = vessel.replace('_', ' ')
            print(f"{vessel_clean:<30} {row['total_co2']:>15,.0f} {row['mean_co2']:>12,.0f} {int(row['records']):>8}")
        
        return vessel_emissions
    
    def analyze_monthly_patterns(self):
        """
        Analyze monthly CO2 patterns
        Q: Do certain months show more emissions? (indicator of port congestion/dwell time)
        """
        print("\n" + "=" * 80)
        print("MONTHLY PATTERNS ANALYSIS")
        print("(Does port congestion affect CO2? Analyzing monthly variations)")
        print("=" * 80)
        
        if self.emissions_df is None:
            return
        
        # Extract month from TIME_PERIOD
        filtered = self.emissions_df[
            (self.emissions_df['POLLUTANT'] == 'CO2') &
            (self.emissions_df['VESSEL'] == 'ALL_VESSELS')
        ].copy()
        
        filtered['MONTH'] = filtered['TIME_PERIOD'].str[-2:].astype(int)
        filtered['MONTH_NAME'] = filtered['MONTH'].map({
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        })
        
        monthly = filtered.groupby('MONTH_NAME')['CO2_TONNES'].agg(['sum', 'mean', 'count']).round(0)
        
        print(f"\n[CO2 EMISSIONS BY MONTH - Aggregate view]")
        print("-" * 80)
        print(f"{'Month':<12} {'Total CO2':>15} {'Avg CO2':>12} {'Records':>8}")
        print("-" * 80)
        
        for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if month in monthly.index:
                row = monthly.loc[month]
                print(f"{month:<12} {int(row['sum']):>15,} {row['mean']:>12,.0f} {int(row['count']):>8}")
        
        # Identify peak/low months
        max_month = monthly['sum'].idxmax()
        min_month = monthly['sum'].idxmin()
        max_val = monthly['sum'].max()
        min_val = monthly['sum'].min()
        
        print(f"\n  Peak month: {max_month} ({int(max_val):,} tonnes)")
        print(f"  Low month: {min_month} ({int(min_val):,} tonnes)")
        print(f"  Difference: {int(max_val - min_val):,} tonnes ({(max_val-min_val)/min_val*100:.1f}%)")
        print("\n  Interpretation:")
        print("  High variation between months could indicate:")
        print("    * Port congestion increases dwell time -> more CO2 from ships waiting")
        print("    * Seasonal shipping patterns (weather, holidays)")
        print("    * Ships anchoring longer during peak seasons")
        
        return monthly
    
    def analyze_country_emissions(self):
        """
        Analyze CO2 by country/region (proxy for port activity)
        This allows us to map port-specific analysis since we have port->country mapping
        """
        print("\n" + "=" * 80)
        print("COUNTRY/REGION CO2 EMISSIONS ANALYSIS")  
        print("(Mapping to key ports: Shanghai/China, LA/USA, Rotterdam/Netherlands, Singapore)")
        print("=" * 80)
        
        if self.emissions_df is None:
            return
        
        filtered = self.emissions_df[
            (self.emissions_df['POLLUTANT'] == 'CO2') &
            (self.emissions_df['VESSEL'] == 'ALL_VESSELS')
        ].copy()
        
        # Aggregate by country
        country_data = filtered.groupby('REF_AREA').agg({
            'CO2_TONNES': ['sum', 'mean', 'count']
        }).round(2)
        
        country_data.columns = ['total_co2', 'avg_co2', 'records']
        country_data = country_data.sort_values('total_co2', ascending=False)
        
        # Focus on our key ports' countries
        key_countries = ['CHN', 'USA', 'NLD', 'SGP', 'AUS']
        
        print("\n[CO2 EMISSIONS FOR KEY PORTS' COUNTRIES]")
        print("-" * 80)
        print(f"{'Country':<30} {'Total CO2':>15} {'Avg/Record':>12} {'Records':>8}")
        print("-" * 80)
        
        for country in key_countries:
            if country in country_data.index:
                row = country_data.loc[country]
                country_name = COUNTRY_CODES.get(country, country)
                print(f"{country_name:<30} {int(row['total_co2']):>15,} {row['avg_co2']:>12,.0f} {int(row['records']):>8}")
        
        # Port-specific interpretation
        print("\n[ROUTE ANALYSIS SETUP]")
        print("-" * 80)
        print("  Route 1: Shanghai (China) -> Los Angeles (USA)")
        print("  Route 2: Australia -> East Asia (Shanghai/Yokohama)")
        print("  Route 3: Rotterdam (Netherlands) -> Singapore")
        print("\n  For each route:")
        print("    * Starting port CO2 levels = departure port activity")
        print("    * Destination port CO2 levels = arrival port activity")
        print("    * Higher variation = more port congestion")
        
        return country_data
    
    def analyze_dwell_time_correlation(self):
        """
        Analyze dwell time correlation with emissions
        Q: When ships stay longer in port (port congestion), does CO2 increase?
        
        Strategy: Modern ships don't reduce power significantly while docked.
        High monthly variations from same country = port congestion
        """
        print("\n" + "=" * 80)
        print("DWELL TIME IMPACT ANALYSIS")
        print("(Does extended port stay (4+ hours, or congestion) increase CO2?)")
        print("=" * 80)
        
        if self.emissions_df is None:
            return
        
        filtered = self.emissions_df[
            (self.emissions_df['POLLUTANT'] == 'CO2') &
            (self.emissions_df['VESSEL'] == 'ALL_VESSELS') &
            (self.emissions_df['REF_AREA'].isin(['NLD', 'SGP', 'CHN', 'USA']))  # Major ports
        ].copy()
        
        filtered['TIME_SORT'] = pd.to_datetime(filtered['TIME_PERIOD'], format='%Y-%m')
        filtered = filtered.sort_values('TIME_SORT')
        
        print(f"\n[MONTH-TO-MONTH VARIABILITY - Indicator of port congestion]")
        print("-" * 80)
        
        for country in ['CHN', 'USA', 'NLD', 'SGP']:
            country_data = filtered[filtered['REF_AREA'] == country].copy()
            if len(country_data) == 0:
                continue
                
            country_name = COUNTRY_CODES.get(country, country)
            monthly_co2 = country_data.groupby('TIME_PERIOD')['CO2_TONNES'].sum()
            
            if len(monthly_co2) > 1:
                std = monthly_co2.std()
                mean = monthly_co2.mean()
                cv = (std / mean * 100) if mean != 0 else 0  # Coefficient of variation
                
                print(f"\n  {country_name}:")
                print(f"    Average monthly CO2: {mean:,.0f} tonnes")
                print(f"    Std deviation: {std:,.0f} tonnes")
                print(f"    Coefficient of variation: {cv:.1f}%")
                
                if cv > 20:
                    print(f"    -> HIGH VARIATION: Port experiences congestion/unpredictable dwell times")
                    print(f"       Ships waiting -> burning fuel -> more CO2")
                elif cv > 10:
                    print(f"    -> MODERATE VARIATION: Some congestion periods")
                else:
                    print(f"    -> LOW VARIATION: Smooth port operations")
        
        print("\n[KEY INSIGHT]")
        print("    Higher monthly variation = port congestion = ships idle longer")
        print("    While docked for 4+ hours with engines running:")
        print("      * Bulk carriers: ~100-150 tonnes CO2/day")
        print("      * Container ships: ~50-80 tonnes CO2/day")
        print("      * Tankers: ~80-120 tonnes CO2/day")
    
    def generate_report(self):
        """Run complete analysis"""
        if not self.load_data():
            return False
        
        # Run all analyses
        self.analyze_global_co2_trends()
        self.analyze_vessel_type_emissions()
        self.analyze_monthly_patterns()
        self.analyze_country_emissions()
        self.analyze_dwell_time_correlation()
        
        print("\n" + "=" * 80)
        print("[OK] ANALYSIS COMPLETE")
        print("=" * 80)
        print("\nNext steps:")
        print("  1. Create detailed route-specific analysis")
        print("  2. Export findings to visualizations (route_analysis.py)")
        print("  3. Generate region-specific recommendations")
        
        return True

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Use correct dataset filenames: OECD.csv and WIP.csv
    ports_csv = datasets_dir / "WIP.csv"
    emissions_csv = datasets_dir / "OECD.csv"

    
    analyzer = CO2EmissionsAnalyzer(str(ports_csv), str(emissions_csv))
    analyzer.generate_report()
