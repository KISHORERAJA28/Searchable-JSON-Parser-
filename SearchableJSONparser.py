import re

def parse_json(json_string: str) -> 'JSONSearchable':
    patterns = [
        ('STRING',  r'"(?:\\.|[^\\"])*"'),
        ('NUMBER',  r'-?\d+(?:\.\d+)?'),
        ('LITERAL', r'true|false|null'),
        ('CHAR',    r'[\[\]{}:,]'),
        ('WS',      r'\s+'),
    ]

    master_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
    tokens = []
    
    for match in re.finditer(master_regex, json_string):
        kind = match.lastgroup
        value = match.group(kind)
        if kind == 'WS': continue
        tokens.append((kind, value))

    def parse_value(index):
        kind, val = tokens[index]
        
        if kind == 'STRING':
            return val[1:-1].replace('\\"', '"').replace('\\\\', '\\'), index + 1
        
        elif kind == 'NUMBER':
            num = float(val)
            return (int(num) if num.is_integer() else num), index + 1
        
        elif kind == 'LITERAL':
            mapping = {"true": True, "false": False, "null": None}
            return mapping[val], index + 1
        
        elif val == '{':
            obj = {}
            index += 1
            while tokens[index][1] != '}':
                key, index = parse_value(index)
                index += 1
                value, index = parse_value(index)
                obj[key] = value
                if tokens[index][1] == ',': index += 1
            return obj, index + 1
            
        elif val == '[':
            arr = []
            index += 1
            while tokens[index][1] != ']':
                value, index = parse_value(index)
                arr.append(value)
                if tokens[index][1] == ',': index += 1
            return arr, index + 1

    parsed_data, _ = parse_value(0)
    return JSONSearchable(parsed_data)

class JSONSearchable:
    def __init__(self, data):
        self._data = data

    def search(self, path: str):
        if not path: return self._data
        
        segments = re.findall(r'[^.\[\]]+|\[\?[^\]]+\]|\[\d+\]', path)
        current = self._data

        for seg in segments:
            if current is None: return None
            
            if seg.startswith('[') and not seg.startswith('[?'):
                idx = int(seg[1:-1])
                current = current[idx] if idx < len(current) else None
                
            elif seg.startswith('[?'):
                condition = seg[2:-1]
                m = re.match(r'(\w+)(==|!=|>|<|>=|<=)(.+)', condition)
                if not m: return None
                key, op, val_str = m.groups()
                
                if val_str == 'true': val = True
                elif val_str == 'false': val = False
                elif val_str.startswith('"'): val = val_str[1:-1]
                else: val = float(val_str)

                filtered = []
                for item in current:
                    item_val = item.get(key)
                    ops = {
                        "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
                        ">": lambda a, b: a > b,   "<": lambda a, b: a < b,
                        ">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b
                    }
                    if ops[op](item_val, val):
                        filtered.append(item)
                current = filtered

            elif isinstance(current, list):
                current = [item.get(seg) for item in current if isinstance(item, dict)]
                current = [v for v in current if v is not None]

            else:
                current = current.get(seg) if isinstance(current, dict) else None
                
        return current
