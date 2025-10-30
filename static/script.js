// Initialize map
var map = L.map('map').setView([28.6139, 77.2090], 12); // Center at Delhi

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Load garbage detections
function loadDetections() {
  fetch('/api/garbage')
    .then(res => res.json())
    .then(data => {
      document.getElementById('totalDetections').innerText = data.length;

      data.forEach(point => {
        const markerColor = point.status === 'critical' ? 'red' :
                            point.status === 'pending' ? 'orange' : 'green';

        const icon = L.icon({
          iconUrl: `https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=trash|${markerColor}`,
          iconSize: [30, 50],
          iconAnchor: [15, 50],
        });

        const marker = L.marker([point.lat, point.lon], { icon }).addTo(map);
        marker.bindPopup(`
          <b>Garbage Detected</b><br>
          <strong>${point.address}</strong><br>
          ${point.timestamp}<br>
          Status: <span style="color:${markerColor}; font-weight:bold;">${point.status}</span><br>
          <img src="${point.image_url}" width="160px">
        `);
      });
    })
    .catch(err => console.error('Error loading detections:', err));
}

// Load optimized route
function loadRoute() {
  fetch('/api/route')
    .then(res => res.json())
    .then(route => {
      L.polyline(route.path, { color: 'blue', weight: 4 }).addTo(map);
    })
    .catch(err => console.error('Error loading route:', err));
}

// Send alert to MCD
function sendAlert() {
  fetch('/api/alert', { method: 'POST' })
    .then(res => res.json())
    .then(result => {
      alert(result.message || 'Alert sent to MCD officials!');
    })
    .catch(err => console.error('Error sending alert:', err));
}

// Button event listeners
document.getElementById("detectBtn").addEventListener("click", loadDetections);
document.getElementById("routeBtn").addEventListener("click", loadRoute);
document.getElementById("alertBtn").addEventListener("click", sendAlert);
