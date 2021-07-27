import prodigy
from prodigy.components.loaders import JSONL
from prodigy.util import split_string
from typing import List
import random
import re
from nltk.tokenize import sent_tokenize

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
random.seed(42)

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
    return title, body

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
        while True:
            for task in stream:

                new_task = {
                    'src_text': '',
                    'id': '',
                    'ref_text': '',
                    'hyp_a_text': '',
                    'hyp_a_id': '',
                    'hyp_b_text': '',
                    'hyp_b_id': '',
                    'score': 0,
                }
                
                new_task['src_text'] = task.pop('src_texts')
                new_task['src_text_title'], new_task['src_text_body'] = clean_text_for_display(new_task['src_text'])
                new_task['id'] = task.pop('test_set_line_id')
                new_task['ref_text'] = task.pop('ref_texts') # remove from item to avoid considering for annotation       
                random_pair = random.sample(list(task.keys()), k=min(k, len(list(task.keys()))))
                new_task['hyp_a_id'], new_task['hyp_b_id'] = random_pair
                new_task['hyp_a_text'] = task[new_task['hyp_a_id']]
                new_task['hyp_b_text'] = task[new_task['hyp_b_id']]

                yield new_task

    # stream in lines from JSONL file yielding a
    # dictionary for each example in the data.
    stream = JSONL(source)

    # select the options (model outputs) to show for each example
    stream = add_options(stream, 2)

    question = "Which response is most related to the review below?"

    return {
        "view_id": "blocks",
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        "config": {
            "blocks": [
                {"view_id": "html", "html_template": f"<h1 class=taskQuestion>{question}</h1>"},
                {"view_id": "html", "html_template": "<div><strong>{{src_text_title}}</strong>{{src_text_body}}</div>"},
                {"view_id": "html", "html_template": "<div>{{hyp_a_text}}</div><div>{{hyp_b_text}}</div>"},
                {"view_id": "html", "html_template": pref_slider},
                ],
            "global_css": css,
            "javascript": javascript
            },
        }



# @prodigy.recipe(
#     "k_choice",
#     dataset=("The dataset to use", "positional",  None, str),
#     source=("The source data as a JSONL file", "positional", None, str),
#     k=("Number of options to choose from", "option", None, str),
# )
# def choice(dataset: str, source: str, k: int):
#     """
#     Annotate data with multiple-choice (k) options. 
#     The annotated examples will have an additional property `"accept": []` mapping to the ID(s) of the selected option(s).
#     """

#     def add_options(stream, k=2):
#         """Helper function to add options to every task in a stream."""
#         for task in stream:
#             # breakpoint()
#             new_task = {
#                 'text': '',
#                 'id': '',
#                 'options': [],
#             }
#             new_task['text'] = task.pop('src_texts')
#             new_task['id'] = task.pop('test_set_line_id')        
#             random_selection = random.sample(list(task.keys()), k=min(k, len(list(task.keys()))))
#             for item in random_selection:
#                 item = {'id': item, 'text': task[item]}
#                 new_task['options'].append(item)
#             yield new_task

#     # stream in lines from JSONL file yielding a
#     # dictionary for each example in the data.
#     stream = JSONL(source)

#     # select the options (model outputs) to show for each example
#     k = int(k) if k else 2
#     # print(k)
#     stream = add_options(stream, k)

#     return {
#         "view_id": "choice",  # Annotation interface to use
#         "dataset": dataset,  # Name of dataset to save annotations
#         "stream": stream,  # Incoming stream of examples
#         "config": {  # Additional config settings
#             # Allow multiple choice if flag is set
#             "choice_style": "multiple" if (k > 2) else "single",
#             # Automatically accept and "lock in" selected answers if binary
#             "choice_auto_accept": False if (k > 2) else True,
#         },
#     }
