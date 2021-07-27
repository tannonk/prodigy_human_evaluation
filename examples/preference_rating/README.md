Basic evaluation schema for collecting user preference ratings for certain criteria.
Idea is to perform pairwise comparisons between models and then ranking with TrueSkill.


### Example Call:

```
prodigy preference_slider pref_test data/hospo_respo_data/hospo_respo_sample.jsonl -F recipe.py
```

```
prodigy preference_slider pref_test_mbart_simpl data/ats_data/de_A1.human_eval.jsonl -F recipe.py
```


### Evaluation Schema Preview:

![Example Screenshot](imgs/preference_rating_screen_1.png)
