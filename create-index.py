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

response = client.indices.create( 'address-index', {
    'settings': {
        'index': {
            'number_of_shards': 1
        },
        "analysis": {
            "normalizer": {
                "lado_normalizer": {
                    "type": "custom",
                    "filter": ["lowercase"]
                }
            },
            "analyzer": {
                "logradouro_analyzer": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "ascii_folding",
                        "portuguese_stop",
                        "portuguese_stemmer"
                    ]
                },
                "cidade_analyzer": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "ascii_folding",
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
                "analyzer": "logradouro_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "cidade": {
                "type": "text",
                "analyzer": "cidade_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "cep": {
                "type": "integer"                
            },
            "num_inicial": {
                "type": "integer"                
            },
            "num_final": {
                "type": "integer"                
            },
            "lado": {
                "type": "text",
                "analyzer": "cidade_analyzer",
                "fields": {
                    "normalize": {
                        "type": "keyword",
                        "normalizer": "lado_normalizer"
                    },
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
        }
    }
})

print('\nCreating index "address-index":')
print(response)
