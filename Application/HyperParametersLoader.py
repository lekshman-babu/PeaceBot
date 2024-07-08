import json
with open('Application/Parameters/HyperParameters.json','r') as file:
    hParams=json.load(file)
with open('Application/Parameters/Tokenizor.json','r') as file:
    tokenizor=json.load(file)