async function fetchData() {
    try {
        const response = await fetch('/data');
        const data = await response.json();
        
        // Mise à jour des éléments HTML avec les nouvelles données
        document.getElementById('temp-display').textContent = data.TempC + '°C';
        document.getElementById('brightness-low-display').textContent = 'Bas: ' + data.LDR;
        // Add other data updates here as needed
    } catch (error) {
        console.error('Erreur lors de la récupération des données', error);
    }
}

// Rafraîchir les données toutes les secondes
setInterval(fetchData, 1000);

document.addEventListener('DOMContentLoaded', fetchData);
