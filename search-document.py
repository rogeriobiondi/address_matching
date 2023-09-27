from opensearchpy import OpenSearch
from prettytable import PrettyTable

client = OpenSearch(
    hosts = [{ 'host': 'localhost', 'port': 9200 }],
    http_auth = ('admin', 'admin'),
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)


while True:
  print("CEP ou Logradouro: ", end="")
  q = input()
  # Search for the document.
  query = {
    'size': 5,    
    'query': {
      'multi_match': {
        'query': q,
        'fields': ['cep', 'logradouro', 'cidade', 'uf']   
      }
    }
  }
  response = client.search(
      body = query,
      index = 'address-index'
  )
  print('\nSearch results:')
  tab = PrettyTable()
  tab.field_names = ["Score", "CEP", "UF", "Cidade", "Tipo", "Logradouro"]
  hits = response['hits']['hits']
  for hit in hits:
      tab.add_row([hit['_score'],
                   hit['_source']['cep'], 
                   hit['_source']['uf'], 
                   hit['_source']['cidade'], 
                   hit['_source']['tipo'], 
                   hit['_source']['logradouro']])
  print(tab)