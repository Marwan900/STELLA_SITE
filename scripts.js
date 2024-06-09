document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch and display sensor data
    function fetchSensorData() {
        fetch('/ldr')
            .then(response => response.text())
            .then(data => {
                const dataDisplay = document.getElementById("data-display");
                if (data.includes("zone d'ombre")) {
                    dataDisplay.classList.add("in-shadow");
                } else {
                    dataDisplay.classList.remove("in-shadow");
                }
                dataDisplay.innerHTML = `
                    <p>${data}</p>
                `;
            })
            .catch(error => console.error('Error fetching sensor data:', error));
    }

    // Function to fetch and display temperature data
    function fetchTemperatureData() {
        fetch('/temperature')
            .then(response => response.text())
            .then(data => {
                const tempDisplay = document.getElementById("temp-display");
                tempDisplay.innerHTML = `
                    <p>${data}</p>
                `;
            })
            .catch(error => console.error('Error fetching temperature data:', error));
    }

    fetchSensorData();
    fetchTemperatureData();

    // Refresh data every 10 seconds
    setInterval(fetchSensorData, 10000);
    setInterval(fetchTemperatureData, 10000);
});
