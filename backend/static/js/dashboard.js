document.addEventListener("DOMContentLoaded", function () {

    loadDashboard();

    setInterval(loadDashboard, 5000);

    const runBuildForm = document.querySelector(
        'form[action*="/run/"], form[action*="run-build"]'
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

                const summary = (data.latest_build.summary || "").trim();

                const isError = /429|RESOURCE_EXHAUSTED|GEMINI ERROR|Exception Type|ClientError|quota/i.test(summary);

                if (isError) {

                    aiSummary.innerHTML = `
                        <div class="text-center py-2 px-1">
                            <i class="bi bi-hourglass-split fs-2 text-warning d-block mb-2"></i>
                            <h6 class="fw-bold mb-1">AI Analysis Temporarily Unavailable</h6>
                            <p class="text-muted small mb-2">
                                The Gemini API quota has been exceeded. Build results are unaffected — only this summary is delayed.
                            </p>
                            <a href="https://ai.google.dev/gemini-api/docs/rate-limits" target="_blank" rel="noopener" class="small">
                                View quota &amp; billing details
                            </a>
                        </div>
                    `;

                } else if (summary) {

                    const escaped = summary
                        .replace(/&/g, "&amp;")
                        .replace(/</g, "&lt;")
                        .replace(/>/g, "&gt;")
                        .replace(/\n{2,}/g, "\n")
                        .trim();

                    aiSummary.innerHTML = `<p class="mb-0">${escaped.replace(/\n/g, "<br>")}</p>`;

                } else {

                    aiSummary.innerHTML = `
                        <div class="text-center py-2 px-1 text-muted">
                            <i class="bi bi-robot fs-2 d-block mb-2"></i>
                            <p class="small mb-0">AI Summary not available yet.</p>
                        </div>
                    `;

                }

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