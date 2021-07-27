import prodigy
from prodigy.components.loaders import JSONL

custom_css = """
/* make the annotation window wider for side-by-side display */
.prodigy-container {
    max-width: 200em;
    white-space: normal;
}

/* reduce the font size for all annotation elements */
.prodigy-content * { font-size: 14px; }

/* set the two model outputs for comparison side-by-side */
.prodigy-content:nth-child(3) { 
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 100px;
}

/* style settings for custom slider */
.slidecontainer {
    margin: auto;
    width: 80%; /* Width of the outside container */
}

.slider {
    -webkit-appearance: none; /* Override default look */
    width: 100%; /* Set a specific slider handle width */
    height: 25px; /* Slider handle height */
    background: #d3d3d3; /* slider background */
    outline: none; /* Remove outline */
    opacity: 0.7; /* Set transparency (for mouse-over effects on hover) */
    -webkit-transition: .2s; /* 0.2 seconds transition on hover */
    transition: opacity .2s;
    cursor: pointer; /* Cursor on hover */
}

.slider:hover {
    opacity: 1; /* Fully shown on mouse-over */
}
"""

slider_html = """
<div class="slidecontainer">
    <input type="range" list="tickmarks" min="-100"
    max="100" class="slider" id="score_slider" step=1>
    <p>Value: <span id="slider_value"></span></p>
    
    <datalist id="tickmarks">
        <option value="-100" label="100%"></option>
        <option value="-90"></option>
        <option value="-80"></option>
        <option value="-70"></option>
        <option value="-60"></option>
        <option value="-50" label="50%"></option>
        <option value="-40"></option>
        <option value="-30"></option>
        <option value="-20"></option>
        <option value="-10"></option>
        <option value="0" label="0%"></option>
        <option value="10"></option>
        <option value="20"></option>
        <option value="30"></option>
        <option value="40"></option>
        <option value="50" label="50%"></option>
        <option value="60"></option>
        <option value="70"></option>
        <option value="80"></option>
        <option value="90"></option>
        <option value="100" label="100%"></option>
    </datalist>
</div>
"""

custom_javascript1 = """
document.addEventListener("prodigyanswer", event => {
    var slider = document.getElementById("score_slider");
    // save the value to the annotation task
    user_score = parseFloat(slider.value);
    event.detail.task.score = user_score;
    console.log('User score =', user_score);
    // reset the slider to default value
    slider.value = slider.defaultValue;
})
"""

custom_javascript2 = """
document.addEventListener("prodigyanswer", event => {
    var slider = document.getElementById("score_slider");
    // save the value to the annotation task
    user_score = parseFloat(slider.value);
    window.prodigy.update({ score: user_score });
    console.log('User score =', user_score);
    // reset the slider to default value
    slider.value = slider.defaultValue;
})
"""

custom_javascript3 = """
document.addEventListener('prodigymount', () => {
    
    var slider = document.getElementById("score_slider");
    var output = document.getElementById("slider_value");
    output.innerHTML = slider.value; // Display the default slider value
    
    slider.addEventListener('input', event => {
        window.prodigy.update({ score: event.target.value })
        // Update the current slider value (each time you drag the slider handle)
        output.innerHTML = event.target.value;    
    })

    document.addEventListener("prodigyanswer", event => {
        // reset the slider to default value
        slider.value = slider.defaultValue;
        output.innerHTML = slider.value; // Display the default slider value
    })

})

"""

@prodigy.recipe(
    "preference_slider",
    dataset=("The dataset to use", "positional",  None, str),
    source=("The source data as a JSONL file", "positional", None, str),
)
def choice(dataset: str, source: str):
    """
    Rating pairwise model outputs with a preference slider
    """

    # stream in lines from JSONL file yielding a
    # dictionary for each example in the data.
    stream = JSONL(source)

    return {
        "view_id": "blocks",
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        "config": {
            "blocks": [
                {"view_id": "html", "html_template": "<p>{{src_text}}</p>"},
                {"view_id": "html", "html_template": "<div>{{options.a.text}}</div><div>{{options.b.text}}</div>"},
                {"view_id": "html", "html_template": slider_html},
                ],
            "global_css": custom_css,
            "javascript": custom_javascript3
            },
        }

