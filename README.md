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

Example Usage 
Setup:1

if __name__ == "__main__":
    
    json_data = """
{
  "home_name": "Smart Hub Alpha",
  "devices": [
    { "id": 1, "name": "Living Room Light", "type": "light", "power_usage": 10, "online": true },
    { "id": 2, "name": "Kitchen AC", "type": "appliance", "power_usage": 1200, "online": true },
    { "id": 3, "name": "Garage Door", "type": "security", "power_usage": 5, "online": false }
  ],
  "settings": {
    "eco_mode": true,
    "firmware": "v2.1.0"
  }
}
"""


    searchable_json = parse_json(json_data)

Queries:

    print("--- STARTING TESTS ---")

    # Test 1: Simple Key Access
    print(f"Test 1 (Key): {searchable_json.search('home_name')}")  #output:Test 1 (Key): Smart Hub Alpha

    # Test 2: Nested Index and Key
    print(f"Test 2 (Nested): {searchable_json.search ('devices[1].name')}")  #output:Test 2 (Nested): Kitchen AC

    # Test 3: Boolean Filter
    print(f"Test 3 (Filter): {searchable_json.search('devices[?online==true]')}")  #output:Test 3 (Filter): [{'id': 1, 'name': 'Living Room Light', 'type': 'light', 'power_usage': 10, 'online': True}, {'id': 2, 'name': 'Kitchen AC', 'type': 'appliance', 'power_usage': 1200, 'online': True}]

    # Test 4: Math Filter + Property Selection
    print(f"Test 4 (Multi): {searchable_json.search('devices[?power_usage>50].name')}")  #output:Test 4 (Multi): ['Kitchen AC']

    # Test 5: Invalid Path
    print(f"Test 5 (Invalid): {searchable_json.search('settings.owner')}")  #output:Test 5 (Invalid): None

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Example Usage 
Setup:2

if __name__ == "__main__":

    json_data = """
    {
    "store": "Main Street Books",
    "inventory": [
        { "type": "book", "title": "The Great Gatsby", "price": 12.50, "in_stock": true },
        { "type": "book", "title": "Moby Dick", "price": 15.00, "in_stock": false },
        { "type": "magazine", "title": "Tech Today", "price": 5.99, "in_stock": true }
    ],
    "location": {
        "city": "New York",
        "postcode": "10001"
    }
    }
    """

    searchable_json = parse_json(json_data)


Queries:

    print("--- STARTING TESTS ---")

    # Test 1: Simple Key Access
    print(f"Test 1 (Key): {searchable_json.search('store')}") #output:Test 1 (Key): Main Street Books

    # Test 2: Nested Index and Key
    print(f"Test 2 (Nested): {searchable_json.search('inventory[0].title')}") #output:Test 2 (Nested): The Great Gatsby

    # Test 3: Boolean Filter
    print(f"Test 3 (Filter): {searchable_json.search('inventory[?in_stock==true]')}") #output:Test 3 (Filter): [{'type': 'book', 'title': 'The Great Gatsby', 'price': 12.5, 'in_stock': True}, {'type': 'magazine', 'title': 'Tech Today', 'price': 5.99, 'in_stock': True}]

    # Test 4: Math Filter + Property Selection
    print(f"Test 4 (Multi): {searchable_json.search('inventory[?price<15.0].title')}") #output:Test 4 (Multi): ['The Great Gatsby', 'Tech Today']

    # Test 5: Invalid Path
    print(f"Test 5 (Invalid): {searchable_json.search('location.country')}") #output: Test 5 (Invalid): None

