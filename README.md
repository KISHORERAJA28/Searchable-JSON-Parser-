Searchable JSON Parser

A custom-built JSON parser and query engine developed in Python. This project demonstrates how to tokenize and parse JSON strings manually using regular expressions and provides a powerful search interface for deep data navigation and conditional filtering.

Features:
* Manual JSON Parsing: Decodes JSON strings into Python dictionaries and lists without using the built-in `json` module.
* Deep Path Navigation: Access nested data using dot notation (e.g., `user.profile.name`).
* Conditional Filtering: Filter arrays of objects using comparison operators (e.g., `[?age>=18]`).
* Collection Mapping: Automatically extract keys from every object within a list.

Usage:
To use the parser, import the `parse_json` function and call the `.search()` method on the resulting object.

```python
from parser import parse_json

json_data = '''
{
  "store": {
    "books": [
      {"title": "Python Basics", "price": 20},
      {"title": "Advanced Regex", "price": 45}
    ]
  }
}
'''

data = parse_json(json_data)

# 1. Access nested data
print(data.search("store.books[0].title")) # Output: "Python Basics"

# 2. Filter list by condition
expensive_books = data.search("store.books[?price>30]") 
print(expensive_books) # Output: [{"title": "Advanced Regex", "price": 45.0}]
