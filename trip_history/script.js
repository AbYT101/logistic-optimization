document.addEventListener("DOMContentLoaded", () => {
    const map = L.map('map').setView([6.5244, 3.3792], 12); // Default view over Lagos

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    let tripData = [];

    document.getElementById('csvFileInput').addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            Papa.parse(file, {
                header: true,
                complete: (results) => {
                    tripData = results.data.map(row => ({
                        tripId: parseInt(row['Trip ID']),
                        origin: [parseFloat(row['Trip Origin Lat']), parseFloat(row['Trip Origin Lng'])],
                        destination: [parseFloat(row['Trip Destination Lat']), parseFloat(row['Trip Destination Lng'])]
                    }));
                    alert('CSV file loaded successfully');
                }
            });
        }
    });

    document.getElementById('clearPaths').addEventListener('click', () => {
            // Clear existing layers
            map.eachLayer((layer) => {
                if (!!layer.toGeoJSON) {
                    map.removeLayer(layer);
                }
            });
    })

    document.getElementById('showTripButton').addEventListener('click', () => {
        const tripId = parseInt(document.getElementById('tripIdInput').value);
        const trip = tripData.find(t => t.tripId === tripId);

        if (trip) {
            const { origin, destination } = trip;

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
            }).addTo(map);

            fetch(`https://router.project-osrm.org/route/v1/driving/${origin[1]},${origin[0]};${destination[1]},${destination[0]}?overview=full&geometries=geojson`)
                .then(response => response.json())
                .then(data => {
                    const coordinates = data.routes[0].geometry.coordinates;
                    const latLngs = coordinates.map(coord => [coord[1], coord[0]]);
                    
                    const polyline = L.polyline(latLngs, { color: 'blue' }).addTo(map);
                    map.fitBounds(polyline.getBounds());

                    // Add animation
                    const decorator = L.polylineDecorator(polyline, {
                        patterns: [
                            { offset: 0, repeat: 10, symbol: L.Symbol.arrowHead({ pixelSize: 10, polygon: false, pathOptions: { stroke: true, color: 'red' } }) }
                        ]
                    }).addTo(map);

                    let offset = 0;
                    function animate() {
                        decorator.setPatterns([
                            { offset: offset + '%', repeat: 10, symbol: L.Symbol.arrowHead({ pixelSize: 10, polygon: false, pathOptions: { stroke: true, color: 'red' } }) }
                        ]);
                        offset = (offset + 1) % 100;
                        requestAnimationFrame(animate);
                    }
                    animate();
                });
        } else {
            alert('Trip ID not found');
        }
    });
});
