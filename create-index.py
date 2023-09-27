from opensearchpy import OpenSearch

client = OpenSearch(
    hosts = [{ 'host': 'localhost', 'port': 9200 }],
    http_auth = ('admin', 'admin'),
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

# Create an index
response = client.indices.create( 'address-index', {
  'settings': {
        'index': {
            'number_of_shards': 1
        },
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "tokenizer": "standard",
                    "filter": [ 
                        "lowercase", 
                        "ascii_folding",
                        "portuguese_stop",
                        "portuguese_stemmer"
                    ]
                }
            },
            "filter": {
                "ascii_folding": {
                    "type": "asciifolding",
                    "preserve_original": True
                },
                "portuguese_stop": {
                    "type": "stop",
                    "stopwords": "_portuguese_"
                },
                "portuguese_stemmer": {
                    "type": "stemmer",
                    "language": "light_portuguese"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "logradouro": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "cidade": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "uf": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "cep": {
                "type": "integer"                
            }

        }
    }
})

print('\nCreating index "address-index":')
print(response)
