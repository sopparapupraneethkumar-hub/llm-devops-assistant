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
function updateRecentBuilds() {

    fetch("/dashboard/recent-builds/")
        .then(response => response.json())
        .then(data => {

            let html = "";

            data.forEach(build => {

                let badge = "bg-primary";

                if (build.status === "SUCCESS")
                    badge = "bg-success";

                else if (build.status === "FAILED")
                    badge = "bg-danger";

                else if (build.status === "RUNNING")
                    badge = "bg-warning";

                html += `
<tr>

<td>

<a href="/builds/${build.id}/">

#${build.number}

</a>

</td>

<td>

<span class="badge ${badge}">

${build.status}

</span>

</td>

<td>

${build.duration} sec

</td>

<td>

${build.date}

</td>

</tr>
`;

            });

            document.getElementById(
                "recent-builds-table"
            ).innerHTML = html;

        });

}
function updateBuildStatus() {

    fetch("/dashboard/build-status/")
        .then(response => response.json())
        .then(data => {

            if (data.status === "NO_BUILD") {
                return;
            }

            document.getElementById("latest-build").innerText =
                "#" + data.build_number;

            document.getElementById("latest-status").innerText =
                data.status;

            document.getElementById("latest-duration").innerText =
                data.duration + " sec";

            const badge =
                document.getElementById("latest-status");

            badge.classList.remove(
                "bg-primary",
                "bg-success",
                "bg-danger",
                "bg-warning"
            );

            if (data.status === "SUCCESS") {

                badge.classList.add("bg-success");

            } else if (data.status === "FAILED") {

                badge.classList.add("bg-danger");

            } else if (data.status === "RUNNING") {

                badge.classList.add("bg-warning");

            } else {

                badge.classList.add("bg-primary");

            }

        })
        .catch(error => console.log(error));

}

updateBuildStatus();
updateRecentBuilds();

setInterval(function(){

    updateBuildStatus();
    updateRecentBuilds();

},5000);