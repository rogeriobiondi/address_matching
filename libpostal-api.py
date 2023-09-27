from fastapi import FastAPI
from postal.parser import parse_address

app = FastAPI()

@app.get("/parse/")
def parse_me(address:str):
    libpostal_addr = parse_address(address)
    print(libpostal_addr)
    parsed_address = {}
    for comp in libpostal_addr:
        if not 'logradouro' in parsed_address and comp[1] == 'road':
            parsed_address['logradouro'] = comp[0]
        if comp[1] == 'house_number':
            parsed_address['numero'] = comp[0]
        if comp[1] == 'city':
            parsed_address['cidade'] = comp[0]
        if comp[1] == 'postcode':
            parsed_address['cep'] = comp[0]
        if comp[1] == 'state':
            parsed_address['uf'] = comp[0]
        print(comp)
    return parsed_address
