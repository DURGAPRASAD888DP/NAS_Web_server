document.addEventListener("DOMContentLoaded", () => {
    fetch('/monitor')
        .then(response => response.json())
        .then(data => {
            const monitoringData = `
                <p>CPU Usage: ${data.cpu_usage}%</p>
                <p>Disk Usage: ${data.disk_usage}%</p>
                <p>Memory Usage: ${data.memory_usage}%</p>
            `;
            document.getElementById("monitoring-data").innerHTML = monitoringData;
        })
        .catch(err => console.error(err));
});
