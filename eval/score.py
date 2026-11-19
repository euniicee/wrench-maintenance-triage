import json

# Load both files
with open("eval/test_set.json") as file:
    test_set = json.load(file)
    
with open("eval/predictions.json") as file:
    predictions = json.load(file)
    
total_found = 0
total_missed = 0
total_extra = 0

pred_by_id = {}
for entry in predictions:
    pred_by_id[entry["id"]] = entry
   
for entry in test_set:
    pred = pred_by_id.get(entry["id"])
    if pred is None:
        print(f'{entry["id"]}: no prediction')
        continue
    
    # a set of issue IDs from each side
    true_issues = {t["issue"] for t in entry["tickets"]}
    pred_issues = {t["issue"] for t in pred["tickets"]}

    found = true_issues & pred_issues 
    missed = true_issues - pred_issues
    extra = pred_issues - true_issues

    total_missed += len(missed)
    total_found += len(found)
    total_extra += len(extra)
    
    if missed or extra:
        print(f'{entry["id"]}: missed {missed} extra {extra}')

print(f"Found: {total_found}  Missed: {total_missed}  Extra: {total_extra}")

