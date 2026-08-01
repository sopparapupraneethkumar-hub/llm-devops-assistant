document.addEventListener("DOMContentLoaded", function () {

    loadDashboard();

    setInterval(loadDashboard, 5000);

    const runBuildForm = document.querySelector(
        'form[action*="run-build"]'
    );

    if (runBuildForm) {

        runBuildForm.addEventListener("submit", function () {

            const btn = runBuildForm.querySelector("button");

            btn.disabled = true;

            btn.innerHTML = `
                <span class="spinner-border spinner-border-sm"></span>
                Running...
            `;

        });

    }

});



function loadDashboard() {

    updateDashboard();

    updateRecentBuilds();

}



function updateDashboard() {

    fetch("/dashboard/build-status/")

        .then(response => response.json())

        .then(data => {

            if (!data.latest_build) {

                return;

            }

            document.getElementById("total-builds").innerText =
                data.kpis.total_builds;

            document.getElementById("success-builds").innerText =
                data.kpis.successful_builds;

            document.getElementById("failed-builds").innerText =
                data.kpis.failed_builds;

            document.getElementById("running-builds").innerText =
                data.kpis.running_builds;



            document.getElementById("latest-build").innerText =
                "#" + data.latest_build.build_number;

            document.getElementById("latest-duration").innerText =
                data.latest_build.duration + " sec";



            const badge = document.getElementById("latest-status");



            badge.className = "badge";



            if (data.latest_build.status === "SUCCESS") {

                badge.classList.add("bg-success");

            }

            else if (data.latest_build.status === "FAILED") {

                badge.classList.add("bg-danger");

            }

            else if (data.latest_build.status === "RUNNING") {

                badge.classList.add("bg-warning");

            }

            else {

                badge.classList.add("bg-secondary");

            }



            badge.innerText = data.latest_build.status;



            const aiSummary = document.getElementById(

                "latest-ai-summary"

            );



            if (aiSummary) {

                aiSummary.innerHTML =

                    data.latest_build.summary;

            }

        })

        .catch(error => console.log(error));

}





function updateRecentBuilds() {

    fetch("/dashboard/recent-builds/")

        .then(response => response.json())

        .then(data => {

            let html = "";



            data.forEach(build => {



                let badge = "bg-secondary";



                if (build.status === "SUCCESS")

                    badge = "bg-success";



                else if (build.status === "FAILED")

                    badge = "bg-danger";



                else if (build.status === "RUNNING")

                    badge = "bg-warning";



                html += `

<tr>

<td>

<strong>

#${build.number}

</strong>

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

<td>

<a

href="/builds/${build.id}/"

class="btn btn-outline-primary btn-sm">

Open

</a>

</td>

</tr>

`;

            });



            document.getElementById(

                "recent-builds-table"

            ).innerHTML = html;

        })

        .catch(error => console.log(error));

}