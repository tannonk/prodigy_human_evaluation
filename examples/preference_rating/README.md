Basic evaluation schema for collecting user preference ratings for certain criteria.
Idea is to perform pairwise comparisons between models and then ranking with TrueSkill.

## Tips and tricks

Useful config settings: https://prodi.gy/docs/install#config

Relevant Support Topics:
- https://support.prodi.gy/t/saving-user-ratings-to-a-task-from-html-inputs/4468

## To Luanch

```
prodigy preference_slider pref_test data/hospo_respo_data/hospo_respo_sample.jsonl -F recipe.py
```

```
prodigy preference_slider pref_test_mbart_simpl data/ats_data/de_A1.human_eval.jsonl -F recipe.py
```

### Annotation Setup (14.09.21)

4 annotators; 2 annotation splits; max 200 items per annotator
- anno_A - x00.json
- anno_B - x00.json
- anno_C - x01.json
- anno_D - x01.json

```
# Test Session
export PRODIGY_PORT=50554 && prodigy preference_slider pref_test data/hospo_respo_data/hospo_respo_sample.jsonl -F recipe.py

# anno_A
export PRODIGY_PORT=50555 && prodigy preference_slider anno_Ax00 data/hospo_respo_data/210914/x00.jsonl -F recipe.py
# anno_B
export PRODIGY_PORT=50556 && prodigy preference_slider anno_Bx00 data/hospo_respo_data/210914/x00.jsonl -F recipe.py
# anno_C
export PRODIGY_PORT=50557 && prodigy preference_slider anno_Cx01 data/hospo_respo_data/210914/x01.jsonl -F recipe.py
# anno_D
export PRODIGY_PORT=50558 && prodigy preference_slider anno_Dx01 data/hospo_respo_data/210914/x01.jsonl -F recipe.py
```

---

## Evaluation Schema Preview

![Example Screenshot](imgs/preference_rating_screen_1.png)

## Known issues

- ticks on HTML range input do not appear
