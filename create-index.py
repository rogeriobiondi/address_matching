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
                "custom_asciifolding": {
                    "tokenizer": "standard",
                    "filter": [ "lowercase", "my_ascii_folding" ]
                }
            },
            "filter": {
                "my_ascii_folding": {
                    "type": "asciifolding",
                    "preserve_original": True
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "logradouro": {
                "type": "text",
                "analyzer": "custom_asciifolding",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "cidade": {
                "type": "text",
                "analyzer": "custom_asciifolding",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "uf": {
                "type": "text",
                "analyzer": "custom_asciifolding",
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
