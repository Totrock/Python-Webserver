import json

json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
parsed_json = json.loads(json_string)
print(parsed_json['first_name'])


with open('data.txt', 'w') as outfile:
    json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])

print (json.dumps("\"foo\bar"))
