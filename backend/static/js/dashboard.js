console.log("dashboard.js loaded");
document.addEventListener("DOMContentLoaded", function () {

    const labels = JSON.parse(
        document.getElementById("trend-labels").textContent
    );

    const data = JSON.parse(
        document.getElementById("trend-data").textContent
    );

    const successfulBuilds = JSON.parse(
        document.getElementById("successful-builds").textContent
    );

    const failedBuilds = JSON.parse(
        document.getElementById("failed-builds").textContent
    );

    const trendCanvas = document.getElementById("buildTrendChart");

    if (trendCanvas) {

        new Chart(trendCanvas.getContext("2d"), {

            type: "line",

            data: {

                labels: labels,

                datasets: [{

                    label: "Builds",

                    data: data,

                    borderColor: "#0d6efd",

                    backgroundColor: "rgba(13,110,253,0.2)",

                    borderWidth: 3,

                    fill: true,

                    tension: 0.4,

                    pointRadius: 5

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                scales: {

                    y: {

                        beginAtZero: true

                    }

                }

            }

        });

    }

    const statusCanvas = document.getElementById("buildStatusChart");

    if (statusCanvas) {

        new Chart(statusCanvas.getContext("2d"), {

            type: "pie",

            data: {

                labels: [

                    "Successful",

                    "Failed"

                ],

                datasets: [{

                    data: [

                        successfulBuilds,

                        failedBuilds

                    ],

                    backgroundColor: [

                        "#198754",

                        "#dc3545"

                    ],

                    borderWidth: 2

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }

        });

    }

});