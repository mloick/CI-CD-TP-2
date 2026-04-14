import re

def capitalize(text):
    if not isinstance(text, str):
        return ""
    if not text:
        return ""
    return text[0].upper() + text[1:].lower()

def calculate_average(numbers):
    if not isinstance(numbers, list) or not numbers:
        return 0.0
    valid_numbers = [n for n in numbers if isinstance(n, (int, float))]
    if not valid_numbers:
        return 0.0
    avg = sum(valid_numbers) / len(valid_numbers)
    return round(avg, 2)

def slugify(text):
    if not isinstance(text, str):
        return ""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def clamp(value, min_val, max_val):
    if not isinstance(value, (int, float)) or not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)):
        return 0
    return max(min_val, min(value, max_val))

def sort_students(students, sort_by="name", order="asc"):
    if not students or not isinstance(students, list):
        return []
    
    valid_sort_keys = ["name", "grade", "age"]
    if sort_by not in valid_sort_keys:
        sort_by = "name"
    
    reverse = order == "desc"
    
    try:
        sorted_students = sorted(students, key=lambda x: x.get(sort_by, 0) if isinstance(x.get(sort_by), (int, float)) else str(x.get(sort_by, "")), reverse=reverse)
        return sorted_students
    except Exception:
        return []
