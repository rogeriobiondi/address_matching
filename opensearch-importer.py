import psycopg2
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

host = "localhost"
database = "correios"
user = "postgres"
password = "postgres"
CHUNK_SIZE = 10000

client = OpenSearch(
    hosts = [{ 'host': 'localhost', 'port': 9200 }],
    http_auth = ('admin', 'admin'),
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

conn = psycopg2.connect(host=host, database=database, user=user, password=password)
cursor = conn.cursor()

query = """
    SELECT logradouro.log_nu as id,
	   logradouro.cep as cep,
	   logradouro.ufe_sg as uf,
	   localidade.loc_no as cidade,
	   bairro.bai_no as bairro,
	   logradouro.tlo_tx as tipo,
	   logradouro.log_no as logradouro,
	   replace(faixas.sec_nu_ini, ',', '') as num_inicial,
	   replace(faixas.sec_nu_fim, ',', '') as num_final,	   
	   faixas.sec_in_lado as lado
    FROM log_logradouro logradouro
	JOIN log_localidade localidade
		ON localidade.loc_nu = logradouro.loc_nu  
	JOIN log_bairro bairro
		ON bairro.bai_nu = logradouro.bai_nu_ini
	FULL OUTER JOIN log_num_sec faixas
		ON faixas.log_nu = logradouro.log_nu
"""

cursor.execute(query)

records = cursor.fetchall()

bulk_data = []
cont = 0
total = 0

for row in records:
    id = row[0]
    document = {
        'cep': row[1],
        'uf': row[2],
        'cidade': row[3],
        'bairro': row[4],
        'tipo': row[5],
        'logradouro': row[6],
        'num_inicial': row[7],
        'num_final': row[8],
        'lado': row[9]
    }
    bulk_data.append({ "_index": "address-index", "_id": id, "_source": document })
    cont = cont + 1
    if cont >= CHUNK_SIZE:
        bulk(client, bulk_data)
        total = total + cont
        print(f"Logradouros indexados {total}...")
        bulk_data = []
        cont = 0
# Insere o bloco final de linhas
bulk(client, bulk_data)
total = total + cont
print(f"Total Rows Inserted {total}...")