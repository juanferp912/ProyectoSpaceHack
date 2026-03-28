// ============================================================
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
var corridorData = {
  "type": "FeatureCollection",
  "metadata": {
    "title": "SpaceHack 2026 \u2014 Green Shipping Corridors",
    "source": "OECD Maritime CO2 Emissions (experimental data)",
    "corridors": [
      "Shanghai_LA",
      "Rotterdam_Singapore",
      "Australia_East_Asia"
    ],
    "period": "2022-2025 (monthly)",
    "note": "CO2 values are country-level totals used as corridor proxies"
  },
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            121.5,
            31.22
          ],
          [
            145.0,
            40.0
          ],
          [
            180.0,
            38.0
          ],
          [
            -155.0,
            25.0
          ],
          [
            -118.25,
            33.75
          ]
        ]
      },
      "properties": {
        "corridor_key": "Shanghai_LA",
        "corridor_name": "Shanghai \u2192 Los Angeles",
        "corridor_label": "Trans-Pacific Green Corridor",
        "start_port": "Shanghai",
        "start_country": "CHN",
        "end_port": "Los Angeles",
        "end_country": "USA",
        "distance_nm": 5400,
        "typical_days": 14,
        "dominant_cargo": "Consumer goods, electronics, vehicles",
        "vessel_types": "Container, Bulk Carrier, Vehicle Carrier",
        "co2_total_tonnes": 2318435637.0,
        "co2_avg_monthly": 57960891.0,
        "co2_reduction_potential_pct": 35.0,
        "co2_after_lng_wind_tonnes": 1506983164.0,
        "congestion_level": "LOW",
        "color": "#E63946",
        "g2z_stage": "Early Realization",
        "g2z_stage_numeric": 4,
        "g2z_phase1_complete": true,
        "g2z_signatories_count": 8,
        "g2z_composite_score": 100,
        "g2z_score_label": "Leading",
        "g2z_co2_target_2030_pct": 30,
        "g2z_clydebank": true,
        "g2z_fuel_deployed_2023_t": 47000,
        "g2z_key_milestone": "Phase 1 milestones declared complete Oct 2024; 47,000t green methanol bunkered at Shanghai 2023",
        "annual_voyages_est": 2800,
        "co2_per_voyage_t": 383244.0,
        "co2_per_nm_kg": 70971.1,
        "co2_yoy_2024_pct": 9.5,
        "co2_annual_2024_Gt": 1.073,
        "gap_to_imo_2030_t": 321924905.0,
        "co2_saved_green_ammonia_t": 987236374.0,
        "dwell_4h_impact_t": 15,
        "cii_dominant_vessel": "Container Ship",
        "cii_actual_2023": 7.2,
        "cii_ref_2023": 6.1,
        "cii_grade_2023": "D",
        "cii_gap_to_2030_pct": 46.0
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            4.48,
            51.9
          ],
          [
            12.0,
            37.0
          ],
          [
            32.0,
            30.0
          ],
          [
            43.0,
            12.5
          ],
          [
            58.0,
            22.0
          ],
          [
            72.0,
            20.0
          ],
          [
            103.85,
            1.28
          ]
        ]
      },
      "properties": {
        "corridor_key": "Rotterdam_Singapore",
        "corridor_name": "Rotterdam \u2192 Singapore",
        "corridor_label": "Europe-Asia Green Corridor (Suez)",
        "start_port": "Rotterdam",
        "start_country": "NLD",
        "end_port": "Singapore",
        "end_country": "SGP",
        "distance_nm": 7000,
        "typical_days": 28,
        "dominant_cargo": "Chemicals, petroleum products, general cargo",
        "vessel_types": "Container, Bulk Carrier, Oil Tanker, Chemical Tanker",
        "co2_total_tonnes": 1013934435.0,
        "co2_avg_monthly": 25348361.0,
        "co2_reduction_potential_pct": 35.0,
        "co2_after_lng_wind_tonnes": 659057383.0,
        "congestion_level": "LOW",
        "color": "#457B9D",
        "g2z_stage": "Advanced Feasibility",
        "g2z_stage_numeric": 3,
        "g2z_phase1_complete": false,
        "g2z_signatories_count": 3,
        "g2z_composite_score": 100,
        "g2z_score_label": "Leading",
        "g2z_co2_target_2030_pct": 25,
        "g2z_clydebank": true,
        "g2z_fuel_deployed_2023_t": 0,
        "g2z_key_milestone": "28 partners confirmed March 2025; digital data exchange trial between PoR and MPA live since 2024",
        "annual_voyages_est": 3400,
        "co2_per_voyage_t": 123851.0,
        "co2_per_nm_kg": 17692.98,
        "co2_yoy_2024_pct": 7.2,
        "co2_annual_2024_Gt": 0.421,
        "gap_to_imo_2030_t": 126327910.0,
        "co2_saved_green_ammonia_t": 387405591.0,
        "dwell_4h_impact_t": 15,
        "cii_dominant_vessel": "Container Ship",
        "cii_actual_2023": 7.2,
        "cii_ref_2023": 6.1,
        "cii_grade_2023": "D",
        "cii_gap_to_2030_pct": 46.0
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            151.21,
            -33.87
          ],
          [
            153.0,
            -20.0
          ],
          [
            143.0,
            -5.0
          ],
          [
            130.0,
            15.0
          ],
          [
            121.5,
            31.22
          ]
        ]
      },
      "properties": {
        "corridor_key": "Australia_East_Asia",
        "corridor_name": "Australia \u2192 East Asia",
        "corridor_label": "Australia-East Asia Green Corridor",
        "start_port": "Sydney / Brisbane",
        "start_country": "AUS",
        "end_port": "Shanghai / Yokohama",
        "end_country": "CHN",
        "distance_nm": 4200,
        "typical_days": 11,
        "dominant_cargo": "Iron ore, coal, LNG, grain",
        "vessel_types": "Bulk Carrier, LNG Tanker, Oil Tanker, Container",
        "co2_total_tonnes": 1672217268.0,
        "co2_avg_monthly": 41805432.0,
        "co2_reduction_potential_pct": 35.0,
        "co2_after_lng_wind_tonnes": 1086941224.0,
        "congestion_level": "LOW",
        "color": "#2A9D8F",
        "g2z_stage": "Feasibility",
        "g2z_stage_numeric": 2,
        "g2z_phase1_complete": false,
        "g2z_signatories_count": 6,
        "g2z_composite_score": 65,
        "g2z_score_label": "On Track",
        "g2z_co2_target_2030_pct": 5,
        "g2z_clydebank": false,
        "g2z_fuel_deployed_2023_t": 0,
        "g2z_key_milestone": "Feasibility study published May 2023 (ETC); 360 vessels needed by 2050; clean ammonia identified as primary pathway",
        "annual_voyages_est": 5600,
        "co2_per_voyage_t": 138740.0,
        "co2_per_nm_kg": 33033.39,
        "co2_yoy_2024_pct": 8.0,
        "co2_annual_2024_Gt": 0.777,
        "gap_to_imo_2030_t": 233083620.0,
        "co2_saved_green_ammonia_t": 714789767.0,
        "dwell_4h_impact_t": 15,
        "cii_dominant_vessel": "Bulk Carrier",
        "cii_actual_2023": 5.9,
        "cii_ref_2023": 4.2,
        "cii_grade_2023": "E",
        "cii_gap_to_2030_pct": 74.0
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          121.5,
          31.22
        ]
      },
      "properties": {
        "port_name": "Shanghai",
        "country": "CHN",
        "co2_total_tonnes": 1410885741.0,
        "co2_avg_monthly": 29393453.0,
        "congestion_level": "LOW",
        "congestion_cv_pct": 8.1,
        "color": "#E63946",
        "marker_size": 5
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -118.25,
          33.75
        ]
      },
      "properties": {
        "port_name": "Los Angeles",
        "country": "USA",
        "co2_total_tonnes": 907549895.0,
        "co2_avg_monthly": 18907289.0,
        "congestion_level": "LOW",
        "congestion_cv_pct": 6.5,
        "color": "#F77F00",
        "marker_size": 5
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          4.48,
          51.9
        ]
      },
      "properties": {
        "port_name": "Rotterdam",
        "country": "NLD",
        "co2_total_tonnes": 262246080.0,
        "co2_avg_monthly": 5463460.0,
        "congestion_level": "LOW",
        "congestion_cv_pct": 4.5,
        "color": "#06A77D",
        "marker_size": 5
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          103.85,
          1.28
        ]
      },
      "properties": {
        "port_name": "Singapore",
        "country": "SGP",
        "co2_total_tonnes": 751688354.0,
        "co2_avg_monthly": 15660174.0,
        "congestion_level": "LOW",
        "congestion_cv_pct": 6.7,
        "color": "#00B4D8",
        "marker_size": 5
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          151.21,
          -33.87
        ]
      },
      "properties": {
        "port_name": "Sydney",
        "country": "AUS",
        "co2_total_tonnes": 261331527.0,
        "co2_avg_monthly": 5444407.0,
        "congestion_level": "LOW",
        "congestion_cv_pct": 9.1,
        "color": "#8338EC",
        "marker_size": 5
      }
    }
  ]
};

var corridors = ee.FeatureCollection(corridorData.features
  .filter(function(f) { return f.geometry.type === 'LineString'; })
  .map(function(f) { return ee.Feature(f); })
);

var ports = ee.FeatureCollection(corridorData.features
  .filter(function(f) { return f.geometry.type === 'Point'; })
  .map(function(f) { return ee.Feature(f); })
);

// ---- BASEMAP ----
Map.setOptions('SATELLITE');
Map.setCenter(90, 15, 3);  // Indian Ocean centered view

// ---- CORRIDOR LINES ----
// Color each corridor by its assigned color property
var corridorStyle = {
  width: 3,
  fillColor: '00000000',
};

// Paint corridors with their corridor color
var corridorVis = corridors.style({
  styleProperty: 'color',
  width: 4,
  lineType: 'solid',
});

Map.addLayer(corridorVis, {}, 'Green Corridors', true);

// ---- PORT CIRCLES ----
// Scale circle size by congestion + CO2
var portVis = ports.style({
  styleProperty: 'color',
  width: 2,
  fillColor: 'FFFFFF80',
  pointSize: 8,
});

Map.addLayer(portVis, {}, 'Key Ports', true);

// ---- CO2 COUNTRY HEAT (approximate) ----
// Use a simple polygon overlay for corridor countries
var countryColors = {
  'CHN': 'E63946', 'USA': 'F77F00',
  'NLD': '06A77D', 'SGP': '00B4D8', 'AUS': '8338EC',
};

// ---- PANEL: CORRIDOR STATISTICS ----
var panel = ui.Panel({
  style: {
    position: 'bottom-left',
    padding: '10px',
    width: '480px',
    backgroundColor: 'rgba(255,255,255,0.92)',
  }
});

var title = ui.Label({
  value: 'SpaceHack 2026 — Green Shipping Corridors',
  style: { fontWeight: 'bold', fontSize: '14px', margin: '0 0 6px 0' }
});

var subtitle = ui.Label({
  value: 'CO2 emissions from OECD maritime data (2022-2025)',
  style: { fontSize: '11px', color: '#666', margin: '0 0 10px 0' }
});

panel.add(title);
panel.add(subtitle);

// Corridor legend entries
var legendItems = [
  { color: '#E63946', name: 'Shanghai -> Los Angeles', nm: '5,400 nm' },
  { color: '#457B9D', name: 'Rotterdam -> Singapore',  nm: '7,000 nm' },
  { color: '#2A9D8F', name: 'Australia -> East Asia',  nm: '4,200 nm' },
];

legendItems.forEach(function(item) {
  var row = ui.Panel({layout: ui.Panel.Layout.flow('horizontal'), style: {margin: '2px 0'}});
  var colorBox = ui.Label({
    value: '  ',
    style: {
      backgroundColor: item.color,
      padding: '4px 12px',
      margin: '2px 6px 2px 0',
      border: '1px solid #ccc',
    }
  });
  var label = ui.Label(item.name + '  (' + item.nm + ')', {fontSize: '11px'});
  row.add(colorBox);
  row.add(label);
  panel.add(row);
});

panel.add(ui.Label('', {margin: '6px 0'}));

// Stats table header
panel.add(ui.Label(
  'Green Transition Potential (LNG + Wind-Assist = -35% CO2):',
  { fontWeight: 'bold', fontSize: '11px', margin: '4px 0' }
));

var statsData = [
    ['<b>Shanghai → Los Angeles</b>', '0.00T t', '0.00T t (-35%)', '14 days', '5,400 nm'],
    ['<b>Rotterdam → Singapore</b>', '0.00T t', '0.00T t (-35%)', '28 days', '7,000 nm'],
    ['<b>Australia → East Asia</b>', '0.00T t', '0.00T t (-35%)', '11 days', '4,200 nm'],
];

statsData.forEach(function(row) {
  var rowPanel = ui.Panel({
    layout: ui.Panel.Layout.flow('horizontal'),
    style: {margin: '1px 0'}
  });
  row.forEach(function(cell) {
    rowPanel.add(ui.Label(cell, {
      fontSize: '10px',
      margin: '0 4px',
      width: '130px',
    }));
  });
  panel.add(rowPanel);
});

panel.add(ui.Label(
  'Note: CO2 values are country-level OECD totals (corridor proxies)',
  { fontSize: '9px', color: '#999', margin: '8px 0 0 0' }
));

Map.add(panel);

print('Green Corridors loaded:', corridors.size(), 'corridors,', ports.size(), 'ports');
