import random
import re

import prodigy

print(prodigy.__version__)

from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens

eval_html = """<form>
    <strong>FLUENCY</strong>
    <input type="range" id="fluency_range" style="width: 500px;" min="0" max="100" step="0.1" list="ticks">
    <datalist id="ticks">
        <option>0</option>
        <option>25</option>
        <option>50</option>
        <option>75</option>
        <option>100</option>
    </datalist>
</form>"""

javascript = """document.addEventListener('prodigyanswer', event => {

    var fluency = document.getElementById('fluency_range').value;
    
    if (fluency == null) {
        // if not checked, save as 0
        event.detail.task.anno.fluency = parseFloat(0);
    }
    else {
        // otherwise, save the value and reset the button
        event.detail.task.anno.fluency = parseFloat(fluency);
        document.getElementById('fluency_range').value = 0.0;
    }
    
})"""

@prodigy.recipe('custom-edit')
def correct_rrgen(dataset, file_path):

    blocks = [
        {"view_id": "html", "html_template": """<p style="text-align:left;font-family:verdana;font-size:80%;"><strong>{{src}}</strong></p>"""},
        {"view_id": "html", "html_template": """<p style="text-align:left;font-family:verdana;font-size:100%;">{{text}}</p>"""},
        {"view_id": "html", "html_template": eval_html},
    ]
    counts = {"edited": 0, "unchanged": 0}

    def get_stream_helper(stream):
        while True:
            for task in stream:
                yield task

    def get_stream():
        stream = JSONL(file_path)
        tasks = []
        for eg in stream:
            # print(eg.keys())
            eg["edit_text"] = eg['text']
            tasks.append(eg)            
        return tasks

    def update(answers):
        for eg in answers:
            if eg["edit_text"] != eg["text"]:
                counts["edited"] += 1
            else:
                counts["unchanged"] += 1

    def on_exit(ctrl):
        print("\nResults")
        print(counts["edited"], "edited")
        print(counts["unchanged"], "unchanged")

    stream = get_stream()
    stream = get_stream_helper(stream)

    return {
        "dataset": dataset,
        "stream": stream, # NOTE: converting from generator to list allows a progress bar for annotator
        "update": update,
        "on_exit": on_exit,
        "view_id": "blocks",
        "config": {
            "blocks": blocks,
            "javascript": javascript,
            },
        }
