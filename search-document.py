import requests
import json
import readline
import cmd

from opensearchpy import OpenSearch
from prettytable import PrettyTable

LIBPOSTAL_SERVICE_URL = "http://localhost:8000/parse?address="
commands = []

client = OpenSearch(
    hosts = [{ 'host': 'localhost', 'port': 9200 }],
    http_auth = ('admin', 'admin'),
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

def parse_address(address: str) -> dict:
  url = LIBPOSTAL_SERVICE_URL + address 
  payload = {}
  headers = {}
  response = requests.request("GET", url, headers=headers, data=payload)
  return(json.loads(response.text))


class CommandParser(cmd.Cmd):
    
    prompt = "endereço > "
    
    def do_listall(self, line):
        print(commands)
    
    def default(self, line):
        commands.append(line)
        endereco = line
        end = parse_address(endereco)
        
        q = {
          "size": 5,
          "query": {
            "dis_max": {
                "queries": [],
                "tie_breaker": 0.7
            }      
          }
        }

        if 'uf' in end:
          q['query']['dis_max']['queries'].append({
            "multi_match": {
              "query": end["uf"],
              "fields": [ "uf" ],
              "minimum_should_match": "100%"
            }
          })
        
        if 'cidade' in end:
          q['query']['dis_max']['queries'].append({
            "multi_match": {
              "query": end["cidade"],
              "fields": [ "cidade" ],
              "minimum_should_match": "80%"
            }
          })
        
        if 'logradouro' in end:
          q['query']['dis_max']['queries'].append({
            "multi_match": {
              "query": end["logradouro"],
              "type": "most_fields",
              "fields": [ "tipo", "logradouro" ],
              "fuzziness": 3.0
            } 
          })
        
        if 'numero' in end:
          if int(end['numero']) % 2 == 0:
            lado = "p"
          else:
            lado = "i"
          q['query']['dis_max']['queries'].append({
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "num_inicial": {
                                        "lte": int(end['numero'])
                                    }
                                }
                            },
                            {
                                "range": {
                                    "num_final": {
                                        "gte": int(end['numero'])
                                    }
                                }
                            },
                            {
                               "match": { "lado.normalize": lado } 
                            }
                        ]
                    }
                })

        # Sem campos de busca selecionados
        if len(q['query']['dis_max']['queries']) == 0:
          print("Endereço incompleto")
          return
        
        response = client.search(
            body = q,
            index = 'address-index'
        )
        print('\nSearch results:')
        tab = PrettyTable()
        tab.field_names = ["Score", "CEP", "UF", "Cidade", "Bairro", "Tipo", "Logradouro", "Ini", "Fim", "Lado"]
        hits = response['hits']['hits']
        for hit in hits:
            tab.add_row([hit['_score'],
                        hit['_source']['cep'], 
                        hit['_source']['uf'], 
                        hit['_source']['cidade'], 
                        hit['_source']['bairro'],
                        hit['_source']['tipo'], 
                        hit['_source']['logradouro'],
                        hit['_source']['num_inicial'],
                        hit['_source']['num_final'],
                        hit['_source']['lado'],
            ])
        print(tab, '\n')

CommandParser().cmdloop()