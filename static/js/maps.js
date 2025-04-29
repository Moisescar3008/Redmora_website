// Declaración global del mapa y la capa de calor
let map;
let heatMapLayer;
let defaultHeatLayer;

// Inicializar el mapa cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
});

function initializeMap() {
    // Crear el mapa con opciones básicas
    map = L.map("map", {
        center: [21.284259, -99.417428],
        crs: L.CRS.EPSG3857,
        zoom: 5,
        zoomControl: true,
        preferCanvas: false,
    });

    // Añadir la capa base de OpenStreetMap
    L.tileLayer(
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19,
            minZoom: 0
        }
    ).addTo(map);

    // Configurar la capa de calor por defecto
    defaultHeatLayer = L.heatLayer(
        [
            [24.0277, -104.6532, 1],
            [23.7369, -99.1411, 1],
        ],
        {
            blur: 15,
            gradient: {
                "0.0": "blue",
                "0.6": "cyan",
                "0.7": "lime",
                "0.8": "yellow",
                "1.0": "red"
            },
            maxZoom: 18,
            minOpacity: 0.6,
            radius: 26
        }
    ).addTo(map);
}

function scrapeData() {
    // Ocultar botón de descarga y mostrar loader
    document.getElementById('downloadBtn').classList.add('hidden');
    document.getElementById('scrapeLoader').style.display = 'block';

    // Limpiar capas existentes
    if (defaultHeatLayer) {
        map.removeLayer(defaultHeatLayer);
    }
    if (heatMapLayer) {
        map.removeLayer(heatMapLayer);
    }

    // Obtener valores de los campos
    const data = {
        nqueries: document.getElementById('news').value,
        query: document.getElementById('keywords').value,
        qoption: document.getElementById('secondaries').value,
        qexception: document.getElementById('restrictions').value,
        qrangedate: document.getElementById('year').value,
        qsite: document.getElementById('domain').value
    };

    // Realizar la petición al servidor
    fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('scrapeLoader').style.display = 'none';
        document.getElementById('visualizeBtn').classList.remove('hidden');
        autoFillTable();
    })
    .catch(error => {
        console.error('Error en el scraping:', error);
        document.getElementById('scrapeLoader').style.display = 'none';
        alert('Error al realizar el scraping. Por favor, intente nuevamente.');
    });
}

function visualizeData() {
    document.getElementById('visualizeLoader').style.display = 'block';

    fetch('/visualize', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor: ' + response.status);
        }
        return response.json();
    })
    .then(responseData => {
        if (!responseData.Data || !Array.isArray(responseData.Data) || responseData.Data.length === 0) {
            throw new Error('Datos no válidos para el mapa de calor');
        }

        // Limpiar capa de calor existente si existe
        if (heatMapLayer) {
            map.removeLayer(heatMapLayer);
        }

        // Crear nueva capa de calor
        heatMapLayer = L.heatLayer(responseData.Data, {
            blur: 15,
            gradient: {
                "0.0": "blue",
                "0.6": "cyan",
                "0.7": "lime",
                "0.8": "yellow",
                "1.0": "red"
            },
            maxZoom: 18,
            minOpacity: 0.5,
            radius: 25
        });

        // Añadir la nueva capa al mapa
        heatMapLayer.addTo(map);

        // Ajustar la vista del mapa a los datos
        const bounds = L.latLngBounds(responseData.Data.map(point => [point[0], point[1]]));
        map.fitBounds(bounds, { padding: [50, 50] });
    })
    .catch(error => {
        console.error('Error en la visualización:', error);
        alert('Error al visualizar los datos en el mapa. Por favor, intente nuevamente.');
    })
    .finally(() => {
        document.getElementById('downloadBtn').classList.remove('hidden');
        document.getElementById('visualizeLoader').style.display = 'none';
    });
}