import prodigy
from prodigy.components.loaders import JSONL
from prodigy import set_hashes
from datetime import datetime
from prodigy.components.db import connect

import random

# Author: Tannon Kew

"""

Script for custom recipe `preference_slider` that displays
pairwise model output comparisons for a single source text.
Evaluators must drag the slider indicating their degree of
preference given a specific question.

Expects a JSONL file with each line consisting of multiple
model outputs for a single source text.

{
    "src_texts": "blah blah blah", 
    "ref_texts": "blah blah blah", 
    "/srv/scratch6/kew/bart/hospo_respo/en/500k/baseline/inference/bs5.txt": "blah blah blah"
    "/srv/scratch6/kew/bart/hospo_respo/en/500k/filt_freq_distro/inference/bs5.txt": "blah blah blah", 
    "/srv/scratch6/kew/bart/hospo_respo/en/500k/filt_gen_sent/inference/bs5.txt": "blah blah blah", 
    "/srv/scratch6/kew/bart/hospo_respo/en/500k/filt_tgt_ppl/inference/bs5.txt": "blah blah blah",
    "test_set_line_id": line_number
}

"""

# set seed for reproducibility
# random.seed(42)

with open('custom.css', 'r', encoding='utf8') as f:
    css = f.read()

with open('custom.html', 'r', encoding='utf8') as f:
    pref_slider = f.read()

with open('script.js', 'r', encoding='utf8') as f:
    javascript = f.read()

def clean_text_for_display(text):
    text_parts = text.split('---SEP---')
    if len(text_parts) > 1:
        title, body = text_parts
    else:
        title = ''
        body = text_parts
    # body = '\n'.join(sent_tokenize(body))
    return title.strip(), body.strip()

@prodigy.recipe(
    "preference_slider",
    dataset=("The dataset to use", "positional",  None, str),
    source=("The source data as a JSONL file", "positional", None, str),
)
def choice(dataset: str, source: str):
    """
    Rating pairwise model outputs with a preference slider
    """

    def add_options(stream, k=2):
        """Helper function to add options to every task in a stream."""
        for i, task in enumerate(stream):

            new_task = {
                'src_text': '',
                'id': '',
                'ref_text': '',
                'hyp_a_text': '',
                'hyp_a_id': '',
                'hyp_b_text': '',
                'hyp_b_id': '',
                'score': 0,
                'time_loaded': None,
                'time_updated': None,
                'winner': None
            }
            
            new_task['time_loaded'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_task['src_text'] = task.pop('src_texts')
            new_task['src_text_title'], new_task['src_text_body'] = clean_text_for_display(new_task['src_text'])
            new_task['id'] = task.pop('test_set_line_id')
            new_task['ref_text'] = task.pop('ref_texts') # remove from item to avoid considering for annotation
            random.seed(i) # set random seed as index of item in stream for reproducibility
            random_pair = random.sample(list(task.keys()), k=min(k, len(list(task.keys()))))
            new_task['hyp_a_id'], new_task['hyp_b_id'] = random_pair
            new_task['hyp_a_text'] = task[new_task['hyp_a_id']]
            new_task['hyp_b_text'] = task[new_task['hyp_b_id']]
            
            yield new_task

    stream = JSONL(source)
    stream = add_options(stream, 2)
    stream = (set_hashes(task, input_keys=("src_text",), task_keys=("hyp_a_text", "hyp_b_text")) for task in stream)
    
    question = "Which response is most relevant to the review?"

    return {
        "view_id": "blocks",
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        "config": {
            "blocks": [
                {"view_id": "html", "html_template": "<div class=src><p><strong>Review:</strong></p><p><strong>{{src_text_title}}</strong> {{src_text_body}}</p></div>"},
                {"view_id": "html", "html_template": "<h1 class=taskQuestion>{}</h1>".format(question)},
                {"view_id": "html", "html_template": "<div class=hyp1><p><strong>Response A:</strong></p><p>{{hyp_a_text}}</p></div><div class=hyp2><p><strong>Response B:</strong></p><p>{{hyp_b_text}}</p></div>"},
                {"view_id": "html", "html_template": pref_slider},
                ],
            "global_css": css,
            "javascript": javascript
            },
        }
