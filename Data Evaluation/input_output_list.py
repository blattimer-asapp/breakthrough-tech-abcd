'''
notes:
- abcd_v1.1.json.gz is dataset to unzip
- need to turn dataset into a list of lists s.t. [[input, output],...]
- input: original, output: scenario
'''
import gzip
import json

file_path = '/Users/arantxapacheco/asapp_project/abcd_draft/data/abcd_v1.1.json.gz'

def read_json(json_data):
    print(json.dumps(json_data, indent=4))

# unzip file
with gzip.open(file_path, 'rt') as file:
    data = json.load(file)

# input -> original ; output -> scenario
input_output = []
# only use training data
training_convos = data.get('train')

for convo in training_convos:
    inpt = convo.get('original')
    outpt = convo.get('scenario')
    input_output.append([inpt, outpt])

# print out the first element
print(json.dumps(input_output[0], indent=4))
