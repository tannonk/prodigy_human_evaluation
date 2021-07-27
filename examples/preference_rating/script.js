document.addEventListener('prodigymount', () => {
    
    var slider = document.getElementById("score_slider");
    var output = document.getElementById("score_display");
    output.innerHTML = slider.value;
    
    slider.addEventListener('input', event => {
        window.prodigy.update({ score: event.target.value })
        // Update the current slider value (each time you drag the slider handle)
        output.innerHTML = Math.abs(event.target.value);
    })

    // reset the slider to default value
    document.addEventListener("prodigyanswer", event => {
        slider.value = slider.defaultValue;
        output.innerHTML = slider.value;
    })

})