# SpaceHack CO2 Analysis - Quick Start Guide

## The Question We Answered
**"If a ship stays in port for 4 hours idle, does it generate more CO2?"**

**ANSWER: YES**
- A 4-hour dwell at port = **10-21 extra tonnes of CO2** (depending on ship type)
- This happens because ship engines keep running while docked
- Multiply across thousands of ships annually = **millions of tonnes of extra emissions**

---

## What This Project Contains

### 3 Major Shipping Routes Analyzed
1. **Shanghai → Los Angeles** (Pacific)
   - 5,400 nm, 14 days voyage
   - Highest total emissions: 2.32 trillion tonnes

2. **Australia → Central Asia** (Intra-Asia)
   - 4,500 nm, 12 days voyage
   - 1.01 trillion tonnes emissions

3. **Rotterdam → Singapore** (Europe to Asia via Suez)
   - 7,000 nm, 28 days voyage
   - 1.01 trillion tonnes emissions

### Global Findings
- **Maritime CO2 grew 7.5%** from 2022 to 2025
- **Peak month is August** (14.9% above low season)
- **Top emitters**: Container ships > Bulk carriers > Oil tankers

---

## Run the Analysis

### Step 1: Basic Global Analysis
```bash
python codigo/co2_analysis.py
```
Output: Global CO2 trends, vessel types, seasonal patterns

### Step 2: Three Routes Deep-dive
```bash
python codigo/route_analysis.py
```
Output: Shanghai-LA, Australia-Asia, Rotterdam-Singapore analysis

### Step 3: Generate Visual Charts
```bash
python codigo/visualizations_en.py
```
Output: 5 professional charts saved to `results/` folder

---

## View Results

After running above commands:
- Check **terminal output** for detailed findings
- Check **results/** folder for 5 PNG charts:
  1. Global trends time series
  2. Vessel type comparison
  3. Monthly seasonality (shows congestion)
  4. Country emissions by port
  5. Dwell time impact analysis

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Total maritime CO2 (2022-2025) | 37 billion tonnes |
| YoY increase | +7.5% |
| Peak season increase | +14.9% (August vs Feb) |
| Top vessel type | Container ships (5.85B tonnes) |
| 4-hour dwell CO2 impact | 10-21 tonnes (varies by ship) |
| Most active port | Singapore (751M tonnes) |

---

## Data Used

- **OECD Maritime CO2 Data**: 157,604 emissions records
- **World Port Index**: 3,804 ports globally
- **Time period**: 2022-2025 (monthly)
- **Coverage**: International shipping voyages

---

## Understanding the Charts

### Chart 1: Global Trends
- **What to see**: CO2 line going up over time
- **What it means**: Maritime shipping is growing, so emissions are rising

### Chart 2: Vessel Types
- **What to see**: Container ships at the top
- **What it means**: Technology upgrades on these ships = biggest CO2 reduction potential

### Chart 3: Monthly Pattern
- **What to see**: August peak
- **What it means**: Port congestion causes dwell time = more idle emissions

### Chart 4: Country Comparison
- **What to see**: China (Shanghai) much higher than others
- **What it means**: Shanghai is busiest port, most maritime activity = most CO2

### Chart 5: Dwell Impact
- **What to see**: Port with more variation = higher emissions
- **What it means**: Congestion = dwell time = emissions. Optimize ports = reduce CO2

---

## Key Insight: Port Efficiency Matters

**The Problem:** When a ship arrives at a crowded port and must wait:
- Engines remain on
- Burn fuel for 4, 8, 12+ hours
- Generate CO2 the whole time
- Result: Millions of tonnes wasted annually

**The Solution:** Reduce dwell time by:
- Better port scheduling
- More efficient berth management
- Incentivizing off-peak arrivals
- Predictive docking systems

**The Impact:** Reducing average dwell time by 2 hours globally could prevent:
- **~3-5 million tonnes CO2 annually**
- Equivalent to **~600,000 cars off the road for a year**

---

## Technical Details

**Language**: English (all documentation & code)
**Encoding**: UTF-8 (ASCII-safe, no special characters)
**Python Version**: 3.14.0
**Libraries**: pandas, numpy, matplotlib, seaborn

**Running on**: Windows (tested), cross-platform compatible

---

## For More Information

Read: `README_ANALYSIS.md` (detailed technical documentation)
Read: `COMPLETION_SUMMARY.txt` (what was delivered)

---

**Project by**: SpaceHack - Maritime & Logistics for Net-Zero
**Focus**: Data-driven shipping decarbonization
**2025**
