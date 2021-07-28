function getTimestamp() {
    const pad = (n, s = 2) => (`${new Array(s).fill(0)}${n}`).slice(-s);
    const d = new Date();

    return `${pad(d.getFullYear(), 4)}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

document.addEventListener("prodigymount", () => {
    
    var slider = document.getElementById("score_slider");
    var output = document.getElementById("score_display");
    output.innerHTML = "Draw"; // assume draw at 0 for starting point

    slider.addEventListener("input", event => {
        window.prodigy.update({ score: event.target.value })
        // Update the current slider value (each time you drag the slider handle)
        if (event.target.value == 0) {
            output.innerHTML = "Draw";
        } else if (event.target.value > 0) {
            output.innerHTML = "Response B: " + Math.abs(event.target.value) + "%"
            window.prodigy.update({ winner: "B" });
        } else if (event.target.value < 0) {
            output.innerHTML = "Response A: " + Math.abs(event.target.value) + "%"
            window.prodigy.update({ winner: "A" });
        }
    })
    
    // listen for click on accept/reject buttons to update timestamp
    // solution provided at https://support.prodi.gy/t/feature-request-timestamps-for-data-entry/4222/5
    // fails by getting stuck in a loop
    document.querySelectorAll(".prodigy-buttons").forEach(item => {
        item.addEventListener("click", event => {
            var ts = getTimestamp()
            window.prodigy.update({ time_updated: ts });
        })
    })

    // reset the slider to default value
    document.addEventListener("prodigyanswer", event => {
        slider.value = slider.defaultValue;
        output.innerHTML = "Draw"; // assume draw at 0 for starting point
    })
})