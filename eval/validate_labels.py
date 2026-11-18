import json


# Load files
with open("data/taxonomy.json", "r") as file:
    taxonomy = json.load(file)
with open("eval/test_set.json", "r") as file:
    test_set = json.load(file)  

# 2. Collect valid IDs
valid_categories = set()
for category in taxonomy["categories"]:
    valid_categories.add(category["id"])
    
valid_issues = set()
for category in taxonomy["categories"]:
    for issue in category["issues"]:
        valid_issues.add(issue["id"])

valid_types = set()
for type in taxonomy["types"]:
    valid_types.add(type["id"])

valid_urgencies = set()
for urgency in taxonomy["urgency_levels"]:
    valid_urgencies.add(urgency["id"])
    
valid_routes = set()
for route in taxonomy["routes"]:
    valid_routes.add(route["id"])
    
# 3. Check every message
errors = 0
for entry in test_set:
    if entry["needs_review"] is None:
        print(f'{entry["id"]}: needs_review is null')
        errors += 1
    for ticket in entry["tickets"]:
        if ticket["category"] not in valid_categories:
            print(f'{entry["id"]}: unknown category "{ticket["category"]}"')
            errors += 1   
    for ticket in entry["tickets"]:
        if ticket["issue"] not in valid_issues:
            print(f'{entry["id"]}: unknown issue "{ticket["issue"]}"')
            errors += 1
        for type in taxonomy["types"]:
            valid_types.add(type["id"])
        for urgency in taxonomy["urgency_levels"]:
            valid_urgencies.add(urgency["id"])
        for route in taxonomy["routes"]:
            valid_routes.add(route["id"])
print(f"Done. {errors} problem(s) found.")