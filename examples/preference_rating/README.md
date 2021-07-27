Basic evaluation schema for collecting user preference ratings for certain criteria.
Idea is to perform pairwise comparisons between models and then ranking with TrueSkill.


### Example Call:
```
prodigy preference_slider pref_test_mbart_simpl data/ats_data/de_A1.human_eval.jsonl -F recipe.py
```
