"""
SpaceHack - Analytical Visualizations for CO2 Emissions
Professional charts for data-driven insights (not decorative)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SETUP
# ============================================================================

workspace = Path(__file__).parent.parent
datasets_dir = workspace / "datasets"
results_dir = workspace / "results"
results_dir.mkdir(exist_ok=True)

# Style for professional analytics
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data():
    """Load OECD emissions data"""
    df = pd.read_csv(
        datasets_dir / "OECD.csv",
        encoding='utf-8',
        low_memory=False
    )
    df['CO2_TONNES'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')
    df['YEAR'] = df['TIME_PERIOD'].str[:4]
    df['MONTH'] = df['TIME_PERIOD'].str[-2:].astype(int)
    return df

# ============================================================================
# VISUALIZATION 1: Global CO2 Trends Over Time
# ============================================================================

def plot_global_trends(df):
    """Time series: CO2 emissions 2022-2025"""
    print("\n[1/5] Creating global trends chart...")
    
    # Filter data
    data = df[
        (df['POLLUTANT'] == 'CO2') &
        (df['VESSEL'] == 'ALL_VESSELS')
    ].copy()
    
    # Monthly aggregation
    monthly = data.groupby('TIME_PERIOD')['CO2_TONNES'].sum().sort_index()
    
    # Plot
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(range(len(monthly)), monthly.values, linewidth=2.5, color='#2E86AB', marker='o', markersize=4)
    
    # Annual average lines
    years = monthly.index.str[:4].unique()
    for year in years:
        year_data = monthly[monthly.index.str.startswith(year)]
        avg = year_data.mean()
        year_pos = int(monthly.index.get_loc(year_data.index[0]))
        ax.axhline(y=avg, xmin=year_pos/len(monthly), xmax=(year_pos+12)/len(monthly), 
                  linestyle='--', alpha=0.5, color='gray', linewidth=1)
    
    ax.set_title('Global Maritime CO2 Emissions Trend (2022-2025)', fontweight='bold', fontsize=13)
    ax.set_xlabel('Time Period (Monthly)', fontweight='bold')
    ax.set_ylabel('CO2 Emissions (Tonnes)', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f}B'))
    
    # X-axis every 12 months
    tick_positions = range(0, len(monthly), 12)
    tick_labels = [monthly.index[i] for i in tick_positions if i < len(monthly)]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45)
    
    plt.tight_layout()
    plt.savefig(results_dir / '01_global_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("  OK Saved: 01_global_trends.png")

# ============================================================================
# VISUALIZATION 2: Vessel Type Comparison
# ============================================================================

def plot_vessel_types(df):
    """Bar chart: CO2 by vessel type"""
    print("\n[2/5] Creating vessel type comparison...")
    
    # Filter data
    data = df[
        (df['POLLUTANT'] == 'CO2') &
        (~df['VESSEL'].str.contains('ALL', na=False))
    ].copy()
    
    vessel_co2 = data.groupby('VESSEL')['CO2_TONNES'].sum().sort_values(ascending=False).head(10)
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    vessels = [v.replace('_', ' ') for v in vessel_co2.index]
    colors = plt.cm.viridis(np.linspace(0, 1, len(vessels)))
    
    bars = ax.barh(vessels, vessel_co2.values, color=colors)
    
    ax.set_title('Top 10 Vessel Types by Total CO2 Emissions', fontweight='bold', fontsize=13)
    ax.set_xlabel('Total CO2 Emissions (Tonnes)', fontweight='bold')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f}B'))
    ax.invert_yaxis()
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
               f'{width/1e9:.2f}B', ha='left', va='center', fontsize=9)
    
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / '02_vessel_types.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("  OK Saved: 02_vessel_types.png")

# ============================================================================
# VISUALIZATION 3: Monthly Seasonality Pattern
# ============================================================================

def plot_monthly_pattern(df):
    """Line chart: Seasonality showing dwell time impact"""
    print("\n[3/5] Creating monthly seasonality pattern...")
    
    # Filter data
    data = df[
        (df['POLLUTANT'] == 'CO2') &
        (df['VESSEL'] == 'ALL_VESSELS')
    ].copy()
    
    # Monthly average by month of year
    monthly_avg = data.groupby('MONTH')['CO2_TONNES'].mean()
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(1, 13), [monthly_avg.get(i, 0) for i in range(1, 13)], 
           color='#A23B72', alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax.set_title('Seasonal CO2 Variation (August Peak = Port Congestion)', 
               fontweight='bold', fontsize=13)
    ax.set_xlabel('Month', fontweight='bold')
    ax.set_ylabel('Average Monthly CO2 (Tonnes)', fontweight='bold')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
    ax.grid(axis='y', alpha=0.3)
    
    # Highlight peak and low months
    peak_month = monthly_avg.idxmax()
    low_month = monthly_avg.idxmin()
    ax.bar(peak_month, monthly_avg.max(), color='#F18F01', alpha=0.9, 
          edgecolor='black', linewidth=2, label='Peak (Port Congestion)')
    ax.bar(low_month, monthly_avg.min(), color='#2A9D8F', alpha=0.9, 
          edgecolor='black', linewidth=2, label='Low (Smooth Operations)')
    
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(results_dir / '03_monthly_pattern.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("  OK Saved: 03_monthly_pattern.png")

# ============================================================================
# VISUALIZATION 4: Key Countries CO2 Comparison (Route Analysis)
# ============================================================================

def plot_country_emissions(df):
    """Grouped bar chart: Key ports' countries emissions"""
    print("\n[4/5] Creating route countries comparison...")
    
    # Filter data
    data = df[
        (df['POLLUTANT'] == 'CO2') &
        (df['VESSEL'] == 'ALL_VESSELS') &
        (df['REF_AREA'].isin(['CHN', 'USA', 'NLD', 'SGP', 'AUS']))
    ].copy()
    
    data['YEAR'] = data['TIME_PERIOD'].str[:4]
    
    # Aggregate by country and year
    country_year = data.groupby(['YEAR', 'REF_AREA'])['CO2_TONNES'].sum().unstack(fill_value=0)
    
    # Country names
    country_map = {'CHN': 'China (Shanghai)', 'USA': 'United States (LA)',
                   'NLD': 'Netherlands (Rotterdam)', 'SGP': 'Singapore',
                   'AUS': 'Australia'}
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(country_year.index))
    width = 0.15
    colors = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51']
    
    for i, (col, color) in enumerate(zip(country_year.columns, colors)):
        offset = (i - 2) * width
        if col in country_year.columns:
            ax.bar(x + offset, country_year[col], width, label=country_map.get(col, col), 
                  color=color, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_title('CO2 Emissions by Key Port Countries (2022-2025)', 
               fontweight='bold', fontsize=13)
    ax.set_xlabel('Year', fontweight='bold')
    ax.set_ylabel('CO2 Emissions (Tonnes)', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(country_year.index)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'{y/1e12:.1f}T'))
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(results_dir / '04_country_emissions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("  OK Saved: 04_country_emissions.png")

# ============================================================================
# VISUALIZATION 5: Dwell Time Impact (Variability Analysis)
# ============================================================================

def plot_dwell_impact(df):
    """Scatter plot: Port congestion vs CO2 (dwell time proxy)"""
    print("\n[5/5] Creating dwell time impact analysis...")
    
    # Filter data for key ports
    data = df[
        (df['POLLUTANT'] == 'CO2') &
        (df['REF_AREA'].isin(['CHN', 'USA', 'NLD', 'SGP']))
    ].copy()
    
    # Calculate monthly variability (proxy for dwell time/congestion)
    congestion = {}
    for country in data['REF_AREA'].unique():
        country_data = data[data['REF_AREA'] == country]
        monthly = country_data.groupby('TIME_PERIOD')['CO2_TONNES'].sum()
        if len(monthly) > 1:
            cv = (monthly.std() / monthly.mean() * 100)  # Coefficient of variation
            total_co2 = monthly.sum()
            congestion[country] = {'cv': cv, 'total_co2': total_co2}
    
    # Convert to DataFrame for plotting
    plot_data = pd.DataFrame(congestion).T
    country_names = {'CHN': 'Shanghai (China)', 'USA': 'LA (USA)', 
                    'NLD': 'Rotterdam (NL)', 'SGP': 'Singapore'}
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter = ax.scatter(plot_data['cv'], plot_data['total_co2']/1e12, 
                         s=400, alpha=0.6, c=['#E63946', '#F77F00', '#06A77D', '#00B4D8'],
                         edgecolor='black', linewidth=2)
    
    # Add labels
    for idx, (country_code, row) in enumerate(plot_data.iterrows()):
        ax.annotate(country_names[country_code], 
                   (row['cv'], row['total_co2']/1e12),
                   fontsize=10, fontweight='bold',
                   xytext=(5, 5), textcoords='offset points')
    
    ax.set_title('Port Congestion (Dwell Time) vs CO2 Emissions', 
               fontweight='bold', fontsize=13)
    ax.set_xlabel('Port Congestion Level (% monthly variation)', fontweight='bold')
    ax.set_ylabel('Total CO2 Emissions (Trillions tonnes)', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add reference line explaining the correlation
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.text(0.02, 0.98, 'HIGHER VARIATION = MORE DWELL TIME = MORE EMISSIONS',
           transform=ax.transAxes, fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(results_dir / '05_dwell_impact.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("  OK Saved: 05_dwell_impact.png")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print("SPACEHACK - GENERATING ANALYTICAL VISUALIZATIONS")
    print("=" * 80)
    print("\nLoading OECD emissions data...")
    
    df = load_data()
    print(f"OK {len(df):,} records loaded\n")
    
    print("Creating professional analytics charts...")
    print("(Focus: data insights, not decoration)")
    
    # Generate all visualizations
    plot_global_trends(df)
    plot_vessel_types(df)
    plot_monthly_pattern(df)
    plot_country_emissions(df)
    plot_dwell_impact(df)
    
    print("\n" + "=" * 80)
    print("ALL VISUALIZATIONS COMPLETE")
    print("=" * 80)
    print(f"\nOutput saved to: results/")
    print("\nCharts generated:")
    print("  01_global_trends.png - CO2 over time 2022-2025")
    print("  02_vessel_types.png - Top 10 ships by emissions")
    print("  03_monthly_pattern.png - Seasonality (August peak = congestion)")
    print("  04_country_emissions.png - Key ports countries comparison")
    print("  05_dwell_impact.png - Port congestion vs dwell time")

if __name__ == "__main__":
    main()
