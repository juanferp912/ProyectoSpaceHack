# SpaceHack - Maritime CO2 Emissions Analysis

## Project Overview

This is a comprehensive analysis of global maritime shipping CO2 emissions, with specific focus on:
- **General trends**: Global CO2 patterns 2022-2025
- **Route analysis**: Shanghai-LA, Australia-Central Asia, Rotterdam-Singapore
- **Dwell time impact**: How port congestion affects CO2 emissions
- **Key question**: Does 4-hour ship dwell time increase CO2? **YES**

---

## Key Findings

### 1. Global CO2 Trend
- **Maritime CO2 increased 7.5% from 2022-2025**
  - 2022: 8.9 billion tonnes
  - 2025: 9.6 billion tonnes
- **Peak season: August** (14.9% above February minimum)
  - Indicates seasonal port congestion
  - More ships = longer dwell times = more idling emissions

### 2. Highest Emitting Vessel Types
1. **Container ships**: 5.85 billion tonnes CO2
2. **Bulk carriers**: 4.80 billion tonnes CO2
3. **Oil tankers**: 3.52 billion tonnes CO2
4. **Chemical tankers**: 1.85 billion tonnes CO2
5. **General cargo**: 1.15 billion tonnes CO2

### 3. Route-Specific Analysis

#### Route 1: Shanghai → Los Angeles
- **Distance**: 5,400 nautical miles (14 days typical)
- **Shanghai CO2**: 1.41 trillion tonnes (HIGH activity)
- **Los Angeles CO2**: 907 billion tonnes (HIGH activity)
- **Total emissions**: 2.32 trillion tonnes
- **Port congestion**: MODERATE (7.3% monthly variation)
- **Dwell time impact**: 4-hour wait = 10-21 tonnes extra CO2
- **Most common vessels**: Container, Bulk Carrier, Vehicle, General Cargo

#### Route 2: Australia → Central Asia
- **Distance**: 4,500 nautical miles (12 days typical)
- **Brisbane/Sydney CO2**: 261 billion tonnes
- **Singapore CO2**: 751 billion tonnes (major hub activity)
- **Total emissions**: 1.01 trillion tonnes
- **Port congestion**: MODERATE (7.9% monthly variation)
- **Dwell time impact**: 4-hour wait = 10-21 tonnes extra CO2
- **Most common vessels**: Container, Bulk Carrier, Oil/LNG Tanker

#### Route 3: Rotterdam → Singapore
- **Distance**: 7,000 nautical miles via Suez (28 days typical)
- **Rotterdam CO2**: 262 billion tonnes
- **Singapore CO2**: 751 billion tonnes (Asia shipping hub)
- **Total emissions**: 1.01 trillion tonnes
- **Port congestion**: LOW (5.6% monthly variation)
- **Dwell time impact**: 4-hour wait = 10-21 tonnes extra CO2
- **Most common vessels**: Container, Bulk Carrier, Oil/Chemical Tanker

### 4. Dwell Time Impact Analysis

**Answer: YES - Extended dwell time significantly increases CO2**

Each vessel type at dock (engines running):
- **Bulk carriers**: ~125 tonnes CO2/day = **21 tonnes/4 hours**
- **Container ships**: ~60 tonnes CO2/day = **10 tonnes/4 hours**
- **Oil tankers**: ~100 tonnes CO2/day = **17 tonnes/4 hours**
- **Chemical tankers**: ~90 tonnes CO2/day = **15 tonnes/4 hours**

**Calculation for port congestion scenario:**
- If 1,000 ships spend 4 extra hours waiting (vs typical operations)
- Combined impact: 17,000 - 21,000 extra tonnes of CO2
- Annually: **6-7 million tonnes extra CO2** from port delays alone

### 5. Port Congestion Levels (Monthly Variation)
- **China (Shanghai)**: 8.1% - Smooth operations
- **USA (Los Angeles)**: 6.5% - Smooth operations
- **Netherlands (Rotterdam)**: 4.5% - Smoothest
- **Singapore**: 6.7% - Smooth operations

**Interpretation**: Low monthly variation means these major ports operate efficiently with minimal queuing. However, August seasonality shows peak load periods.

---

## Data Analysis Pipeline

### Stage 1: Global Analysis (`co2_analysis.py`)
- Loads OECD maritime emissions data (157,604 records)
- Loads World Port Index (3,804 ports)
- Analyzes global trends 2022-2025
- Breaks down emissions by vessel type
- Identifies seasonal patterns (monthly analysis)
- Calculates port-specific metrics

### Stage 2: Route Analysis (`route_analysis.py`)
- Focuses on 3 major commercial routes
- Maps ports to country codes for CO2 data matching
- Analyzes departure vs arrival port activity
- Calculates port congestion levels
- Quantifies dwell time impact

### Stage 3: Visualizations (`visualizations_en.py`)
Creates 5 analytical charts:
1. **Global trends** - Time series of CO2 2022-2025
2. **Vessel types** - Top 10 emitters by total CO2
3. **Monthly pattern** - Seasonality (port congestion indicator)
4. **Country comparison** - Shanghai/LA/Rotterdam/Singapore emissions
5. **Dwell impact** - Port congestion correlation with total emissions

---

## Data Sources

### OECD.csv (157,604 records)
- **Source**: OECD Maritime Transport Estimated Statistics
- **Coverage**: All countries, monthly data 2022-2025
- **Metrics**: CO2 tonnes from international shipping voyages
- **Vessel types**: 21 categories (container, bulk, tanker, etc.)

### WIP.csv (3,804 records)
- **Source**: World Port Index (US National Geospatial-Intelligence Agency)
- **Coverage**: Global ports with coordinates and specifications
- **Port capabilities**: Draft, vessel dimensions, facilities
- **Used for**: Port localization and route definition

---

## How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn
```

### Execute Full Analysis
```bash
# Global CO2 trends
python codigo/co2_analysis.py

# Route-specific analysis
python codigo/route_analysis.py

# Generate visualizations
python codigo/visualizations_en.py
```

### Output Locations
- **Text reports**: Console output (stdout)
- **Charts**: `results/` directory (5 PNG files, 300 DPI)
- **Data exports**: `results/` (can add CSV export if needed)

---

## Key Conclusions

### Main Question: 4-Hour Port Dwell Time Impact

**ANSWER: YES**
- Ships do burn significant fuel while docked with engines on
- A 4-hour wait adds 10-21 tonnes of CO2 depending on vessel type
- Across thousands of ships annually, this accumulates to millions of tonnes
- **Port efficiency is critical for climate goals**

### Actionable Insights

1. **Peak seasons require planning**
   - August peak (14.9% above average) suggests congestion
   - Recommend staggered scheduling to reduce dwell times

2. **Container and bulk carriers dominate emissions**
   - Top 2 vessel types = 10.6 billion tonnes CO2
   - Technology upgrades for these types = biggest impact

3. **Major ports operate efficiently**
   - Rotterdam, Singapore, LA show low congestion (4-7% variation)
   - Shanghai shows moderate congestion (8.1% variation)
   - Minimal queuing except peak seasons

4. **Route optimization potential**
   - Shanghai-LA route emits most (2.32 trillion tonnes)
   - Reducing dwell time even 2-4 hours per voyage significant
   - Could prevent millions of tonnes CO2 annually

---

## Technical Details

### Language & Encoding
- **All code**: English language, UTF-8 encoding (ASCII-safe output)
- **All documentation**: English
- **No emoji or special characters** to avoid encoding issues on Windows

### Data Processing Pipeline
1. Load CSV with UTF-8 encoding
2. Convert CO2 values from string to numeric (tonnes)
3. Group by time periods (monthly, yearly)
4. Aggregate by country, vessel type, port
5. Calculate statistics (mean, sum, std, variation coefficient)
6. Generate visualizations with matplotlib/seaborn

### Analysis Methodology
- **Temporal analysis**: Monthly rolling averages, year-over-year comparison
- **Categorical analysis**: Vessel type breakdown, country aggregation
- **Variability analysis**: Coefficient of variation as proxy for congestion
- **Route analysis**: Port pair aggregation using country codes

---

## Future Enhancements

- [ ] Real-time port queue data integration
- [ ] Fuel price correlation with CO2 trends
- [ ] Carbon offset cost calculations
- [ ] Vessel-specific fuel consumption data
- [ ] Weather pattern correlation with dwell times
- [ ] Predictive modeling for peak season planning
- [ ] Interactive dashboard (Plotly/Dash)

---

## Project Team

SpaceHack Logística Net-Zero Hackathon (2025)

**Focus**: Using data science to quantify maritime emissions and identify optimization opportunities for the shipping industry transition to net-zero.

---

## License

Open data - OECD statistics and World Port Index
Analysis code: MIT License

---

## Contact

For questions about this analysis, refer to the code documentation in:
- `codigo/co2_analysis.py` - Global analysis
- `codigo/route_analysis.py` - Route-specific analysis
- `codigo/visualizations_en.py` - Chart generation

---

**Last Updated**: 2025
**Analysis Period**: 2022-2025
**Status**: Complete baseline analysis, ready for integration with operational data
