// ============================================================
// SpaceHack 2026 — Green Corridors + Sentinel-5P Air Quality
// ============================================================
// DATOS SATELITALES REALES: Sentinel-5P TROPOMI (ESA / Copernicus)
//
// Lógica de la visualización:
//   NO2  → trazador de contaminación en PUERTOS (industria + barcos en espera)
//   SO2  → trazador de BARCOS EN RUTA (combustible pesado HFO emite SO2)
//   CO   → combustión incompleta — tanto puertos como motores marinos
//
// Si los hotspots de NO2 están SOLO en puertos:   el problema es el dwell time
// Si el SO2 dibuja las RUTAS en el océano:         los barcos en tránsito son el problema
// Si AMBOS coinciden:                              el sistema completo requiere intervención
//
// HOW TO USE:
//   1. Go to https://code.earthengine.google.com/
//   2. Paste this entire script → Click Run
// ============================================================


// ============================================================
// 1. SENTINEL-5P DATOS (2023 — año completo, media anual)
// ============================================================

// NO2 troposférico — hotspots industriales y portuarios
// Fuente: COPERNICUS/S5P/OFFL/L3_NO2 | banda: tropospheric_NO2_column_number_density
// Unidad: mol/m² → multiplicamos x1e6 para micromol/m² (más legible)
var no2 = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
  .filterDate('2023-01-01', '2023-12-31')
  .select('tropospheric_NO2_column_number_density')
  .mean()
  .multiply(1e6);  // mol/m² -> umol/m²

// SO2 columna total — trazador de combustible marino (HFO emite ~3% peso en SO2)
// Fuente: COPERNICUS/S5P/OFFL/L3_SO2 | banda: SO2_column_number_density
var so2 = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_SO2')
  .filterDate('2023-01-01', '2023-12-31')
  .select('SO2_column_number_density')
  .mean()
  .multiply(1e6);

// CO columna — combustión incompleta (motores diesel marinos a baja velocidad en puerto)
// Fuente: COPERNICUS/S5P/OFFL/L3_CO | banda: CO_column_number_density
var co = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CO')
  .filterDate('2023-01-01', '2023-12-31')
  .select('CO_column_number_density')
  .mean()
  .multiply(1000);  // mol/m² -> mmol/m²


// ============================================================
// 2. PARÁMETROS DE VISUALIZACIÓN
// ============================================================

// NO2 — paleta: azul (limpio) → amarillo → rojo (contaminado)
// Rango: 0 a 200 umol/m² (puertos industriales llegan a 150-250)
var no2Vis = {
  min: 0, max: 200,
  palette: ['#0d0221', '#0a1045', '#1a3a7a', '#2d7dd2', '#97d4e8',
            '#fffbbd', '#f4a261', '#e76f51', '#e63946', '#9d0208']
};

// SO2 — paleta: negro (bajo) → violeta → amarillo (barcos en ruta)
// Rango oceánico: 0 a 5 umol/m² (shipping lanes visibles a 1-3)
var so2Vis = {
  min: -0.5, max: 5,
  palette: ['#000000', '#1a001a', '#3d0066', '#7b00d4', '#c0a0ff',
            '#e8d5ff', '#fff3b0', '#ffd166', '#f4a261', '#e63946']
};

// CO — paleta: oscuro → verde → amarillo
// Rango: 30 a 60 mmol/m² (background ~35, puertos ~55)
var coVis = {
  min: 30, max: 65,
  palette: ['#001219', '#005f73', '#0a9396', '#94d2bd',
            '#e9d8a6', '#ee9b00', '#ca6702', '#bb3e03', '#ae2012']
};


// ============================================================
// 3. DATOS DE CORREDORES (versión probada que funciona)
// ============================================================

var corridorData = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [[121.5,31.22],[145,40],[180,38],[-155,25],[-118.25,33.75]]
      },
      "properties": {
        "name": "Shanghai -> Los Angeles",
        "color": "E63946",
        "dist": "5,400 nm",
        "co2_gt": "1.07",
        "days": "14",
        "g2z": "Early Realization",
        "cii": "D",
        "target30": "30"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [[4.48,51.9],[12,37],[32,30],[43,12.5],[58,22],[72,20],[103.85,1.28]]
      },
      "properties": {
        "name": "Rotterdam -> Singapore",
        "color": "457B9D",
        "dist": "7,000 nm",
        "co2_gt": "0.42",
        "days": "28",
        "g2z": "Adv. Feasibility",
        "cii": "D",
        "target30": "25"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [[151.21,-33.87],[153,-20],[143,-5],[130,15],[121.5,31.22]]
      },
      "properties": {
        "name": "Australia -> East Asia",
        "color": "2A9D8F",
        "dist": "4,200 nm",
        "co2_gt": "0.77",
        "days": "11",
        "g2z": "Feasibility",
        "cii": "E",
        "target30": "5"
      }
    },
    // Puertos
    {"type":"Feature","geometry":{"type":"Point","coordinates":[121.5,31.22]},
     "properties":{"port":"Shanghai","country":"CHN","color":"E63946","radius":150000}},
    {"type":"Feature","geometry":{"type":"Point","coordinates":[-118.25,33.75]},
     "properties":{"port":"Los Angeles","country":"USA","color":"FF6B35","radius":100000}},
    {"type":"Feature","geometry":{"type":"Point","coordinates":[4.48,51.9]},
     "properties":{"port":"Rotterdam","country":"NLD","color":"06D6A0","radius":100000}},
    {"type":"Feature","geometry":{"type":"Point","coordinates":[103.85,1.28]},
     "properties":{"port":"Singapore","country":"SGP","color":"00B4D8","radius":100000}},
    {"type":"Feature","geometry":{"type":"Point","coordinates":[151.21,-33.87]},
     "properties":{"port":"Sydney","country":"AUS","color":"8338EC","radius":80000}}
  ]
};

// Separar corredores y puertos
var corridors = ee.FeatureCollection(
  corridorData.features
    .filter(function(f){ return f.geometry.type === 'LineString'; })
    .map(function(f){
      return ee.Feature(ee.Geometry.LineString(f.geometry.coordinates), f.properties);
    })
);

var ports = ee.FeatureCollection(
  corridorData.features
    .filter(function(f){ return f.geometry.type === 'Point'; })
    .map(function(f){
      return ee.Feature(ee.Geometry.Point(f.geometry.coordinates), f.properties);
    })
);

// Buffers de 100km alrededor de cada puerto (zona de influencia portuaria)
var portBuffers = ports.map(function(f) {
  return f.buffer(100000);  // 100 km
});


// ============================================================
// 4. COMPARACIÓN ESTADÍSTICA: PUERTO vs OCÉANO ABIERTO
// ============================================================

// Muestra NO2 en zonas portuarias vs puntos en océano abierto
var oceanPoints = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Point([160, 30]),  {zone: 'Pacific mid-route'}),
  ee.Feature(ee.Geometry.Point([65, 15]),   {zone: 'Indian Ocean corridor'}),
  ee.Feature(ee.Geometry.Point([135, 10]),  {zone: 'South China Sea'}),
  ee.Feature(ee.Geometry.Point([-140, 30]), {zone: 'North Pacific open'}),
]);

// Valor NO2 en cada buffer portuario (media reducida)
var portNO2 = no2.reduceRegions({
  collection: portBuffers,
  reducer: ee.Reducer.mean(),
  scale: 5500  // resolución S5P ~5.5km
});

// Valor NO2 en océano abierto
var oceanNO2 = no2.reduceRegions({
  collection: oceanPoints,
  reducer: ee.Reducer.mean(),
  scale: 5500
});

print('NO2 en zonas portuarias (umol/m2):', portNO2.select(['port','mean']));
print('NO2 en oceano abierto (umol/m2):', oceanNO2.select(['zone','mean']));


// ============================================================
// 5. MAPA BASE + CAPAS SATELLITE
// ============================================================

Map.setOptions('SATELLITE');
Map.setCenter(100, 15, 3);

// CAPA 1: NO2 anual 2023 — muestra hotspots portuarios
Map.addLayer(no2, no2Vis, 'NO2 2023 (umol/m2) — Hotspots Portuarios', true, 0.75);

// CAPA 2: SO2 anual 2023 — muestra rutas de barcos en océano
// NOTA: activa esta capa en el panel de capas (Layer Manager) para comparar
Map.addLayer(so2, so2Vis, 'SO2 2023 (umol/m2) — Rutas Maritimas HFO', false, 0.80);

// CAPA 3: CO anual 2023
Map.addLayer(co, coVis, 'CO 2023 (mmol/m2) — Combustion en Puertos', false, 0.70);

// CAPA 4: Buffers de puertos (zona de influencia ~100km)
Map.addLayer(
  portBuffers.style({color: 'FFFFFF', fillColor: 'FFFFFF22', width: 1}),
  {}, 'Zonas Portuarias (100km buffer)', true
);

// CAPA 5: Corredores verdes
var corridorStyled = corridors.map(function(f) {
  return f.set('style', {color: f.get('color'), width: 3});
});
Map.addLayer(
  corridorStyled.style({styleProperty: 'style'}),
  {}, 'Corredores Verdes (rutas)', true
);

// CAPA 6: Puertos
var portStyled = ports.map(function(f) {
  return f.set('style', {
    pointShape: 'circle', pointSize: 6,
    color: f.get('color'), fillColor: 'FFFFFF'
  });
});
Map.addLayer(portStyled.style({styleProperty: 'style'}), {}, 'Puertos Clave', true);


// ============================================================
// 6. LEYENDAS VISUALES
// ============================================================

function makeLegend(title, palette, minVal, maxVal, units) {
  var legend = ui.Panel({
    style: {padding: '6px 10px', margin: '0', backgroundColor: 'rgba(0,0,0,0.75)'}
  });
  legend.add(ui.Label(title, {
    fontWeight: 'bold', fontSize: '11px', color: 'white', margin: '0 0 4px 0'
  }));

  // Gradient bar using colored labels
  var bar = ui.Panel({layout: ui.Panel.Layout.flow('horizontal'), style: {margin: '2px 0'}});
  palette.forEach(function(hex) {
    bar.add(ui.Label('', {
      backgroundColor: '#' + hex.replace('#',''),
      padding: '4px', margin: '0', width: '18px'
    }));
  });
  legend.add(bar);

  var rangeRow = ui.Panel({layout: ui.Panel.Layout.flow('horizontal')});
  rangeRow.add(ui.Label(String(minVal), {color: 'white', fontSize: '9px'}));
  rangeRow.add(ui.Label('                  ', {fontSize: '9px'}));
  rangeRow.add(ui.Label(String(maxVal) + ' ' + units, {color: 'white', fontSize: '9px'}));
  legend.add(rangeRow);
  return legend;
}

var no2Legend = makeLegend(
  'NO2 — Contaminacion Portuaria',
  ['0d0221','1a3a7a','2d7dd2','97d4e8','fffbbd','f4a261','e63946','9d0208'],
  0, 200, 'umol/m2'
);

var so2Legend = makeLegend(
  'SO2 — Huella de Barcos en Ruta',
  ['000000','3d0066','7b00d4','c0a0ff','fff3b0','ffd166','f4a261','e63946'],
  0, 5, 'umol/m2'
);


// ============================================================
// 7. PANEL PRINCIPAL DE ANÁLISIS
// ============================================================

var mainPanel = ui.Panel({
  style: {
    position: 'bottom-left',
    padding: '12px',
    width: '420px',
    backgroundColor: 'rgba(13,18,30,0.92)'
  }
});

// Header
mainPanel.add(ui.Label('SpaceHack 2026 — Green Corridor Monitor', {
  fontWeight: 'bold', fontSize: '14px', color: '#A8DADC', margin: '0 0 2px 0'
}));
mainPanel.add(ui.Label('Sentinel-5P TROPOMI + OECD Maritime CO2 | 2023 Annual Mean', {
  fontSize: '10px', color: '#888', margin: '0 0 10px 0'
}));

// Separador
mainPanel.add(ui.Label('CAPAS DE CALIDAD DEL AIRE', {
  fontWeight: 'bold', fontSize: '10px', color: '#E9C46A', margin: '4px 0 4px 0'
}));

// Explicación de cada capa
var layerDesc = [
  ['NO2 (activa)', '#E63946',
   'Hotspots en PUERTOS — Shanghai, Rotterdam, Singapore visibles como manchas rojas.'],
  ['SO2 (inactiva)', '#C0A0FF',
   'Rutas de BARCOS en oceano — barcos quemando HFO dejan rastro de SO2 sobre el mar.'],
  ['CO (inactiva)', '#94D2BD',
   'Combustion en puertos — motores idle en muelle emiten CO a baja temperatura.'],
];

layerDesc.forEach(function(item) {
  var row = ui.Panel({layout: ui.Panel.Layout.flow('horizontal'), style: {margin: '2px 0'}});
  row.add(ui.Label('  ', {
    backgroundColor: item[1], padding: '3px 8px', margin: '2px 6px 2px 0'
  }));
  row.add(ui.Panel([
    ui.Label(item[0], {fontWeight: 'bold', fontSize: '10px', color: '#ddd', margin: '0'}),
    ui.Label(item[2], {fontSize: '9px', color: '#aaa', margin: '0'})
  ]));
  mainPanel.add(row);
});

// Separador
mainPanel.add(ui.Label('', {margin: '6px 0 2px 0'}));
mainPanel.add(ui.Label('CORREDORES — CO2 ANUAL 2024 & ESTADO G2Z', {
  fontWeight: 'bold', fontSize: '10px', color: '#E9C46A', margin: '4px 0'
}));

// Tabla de corredores
var corrRows = [
  ['Corredor', 'CO2 2024', 'Brecha 2030', 'G2Z', 'CII'],
  ['Shanghai-LA',    '1.07 Gt', '322 Mt', 'EarlyReal.', 'D'],
  ['Rotterdam-SGP',  '0.42 Gt', '126 Mt', 'Adv.Feas.',  'D'],
  ['Australia-EA',   '0.77 Gt', '233 Mt', 'Feasibility','E'],
];

corrRows.forEach(function(row, i) {
  var rowPanel = ui.Panel({
    layout: ui.Panel.Layout.flow('horizontal'),
    style: {
      margin: '1px 0',
      backgroundColor: i === 0 ? 'rgba(255,255,255,0.08)' : 'transparent'
    }
  });
  var widths = ['120px','65px','65px','80px','30px'];
  var colors = [
    ['#A8DADC','#A8DADC','#A8DADC','#A8DADC','#A8DADC'],
    ['#E63946','#ddd','#E63946','#52B788','#F4A261'],
    ['#457B9D','#ddd','#F4A261','#E9C46A','#F4A261'],
    ['#2A9D8F','#ddd','#E63946','#E63946','#E63946'],
  ];
  row.forEach(function(cell, j) {
    rowPanel.add(ui.Label(cell, {
      fontSize: '10px',
      width: widths[j],
      fontWeight: i === 0 ? 'bold' : 'normal',
      color: i === 0 ? colors[0][j] : colors[i][j],
      margin: '0 2px'
    }));
  });
  mainPanel.add(rowPanel);
});

// Separador
mainPanel.add(ui.Label('', {margin: '6px 0 2px 0'}));
mainPanel.add(ui.Label('INTERPRETACION DE LAS CAPAS', {
  fontWeight: 'bold', fontSize: '10px', color: '#E9C46A'
}));

mainPanel.add(ui.Label(
  'Si el NO2 forma MANCHAS sobre los puertos: el tiempo de espera (dwell time) '+
  'es el problema — motores idle contaminan la zona portuaria.',
  {fontSize: '9px', color: '#ccc', margin: '3px 0'}
));
mainPanel.add(ui.Label(
  'Si el SO2 dibuja LINEAS sobre el oceano: los barcos en transito quemando '+
  'HFO son la fuente principal — requiere transicion a combustibles verdes.',
  {fontSize: '9px', color: '#ccc', margin: '3px 0'}
));
mainPanel.add(ui.Label(
  'La realidad: AMBOS. Por eso el sistema monitorea porto + ruta.',
  {fontSize: '9px', color: '#52B788', fontWeight: 'bold', margin: '5px 0 0 0'}
));

// Fuente
mainPanel.add(ui.Label('', {margin: '4px 0'}));
mainPanel.add(ui.Label(
  'Datos: Sentinel-5P TROPOMI (ESA/Copernicus) + OECD Maritime CO2 + ' +
  'THETIS-MRV 2023 (EMSA) + Getting to Zero Coalition 2025',
  {fontSize: '8px', color: '#666', fontStyle: 'italic'}
));

Map.add(mainPanel);

// Agregar leyenda NO2 en esquina superior derecha
var legendPanel = ui.Panel({
  style: {position: 'top-right', padding: '4px'}
});
legendPanel.add(no2Legend);
legendPanel.add(ui.Label('(Activar capa SO2 en Layers para ver rutas)', {
  fontSize: '9px', color: '#888', margin: '4px 0 0 0'
}));
Map.add(legendPanel);


// ============================================================
// 8. PRINT ESTADÍSTICAS EN CONSOLA
// ============================================================

print('=== SpaceHack 2026 — Sentinel-5P Analysis ===');
print('Sentinel-5P NO2 2023 cargado (COPERNICUS/S5P/OFFL/L3_NO2)');
print('Sentinel-5P SO2 2023 cargado (COPERNICUS/S5P/OFFL/L3_SO2)');
print('Sentinel-5P CO  2023 cargado (COPERNICUS/S5P/OFFL/L3_CO)');
print('');
print('Corredores cargados:', corridors.size());
print('Puertos cargados:', ports.size());
print('');
print('Para ver comparacion NO2 puerto vs oceano abierto,');
print('expande los resultados de portNO2 y oceanNO2 abajo:');
print('');
print('NO2 promedio por zona portuaria (umol/m2):', portNO2.select(['port','mean']));
print('NO2 promedio oceano abierto (umol/m2):', oceanNO2.select(['zone','mean']));
print('');
print('Interpretacion:');
print('  Ratio puerto/oceano > 3x = dwell time es causa principal');
print('  SO2 visible en rutas oceanicas = combustible HFO en transito es causa principal');
