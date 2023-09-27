import csv
from pathlib import Path
import psycopg2

host = "localhost"
database = "correios"
user = "postgres"
password = "postgres"
CHUNK_SIZE = 5000

# Create database connections
conn = psycopg2.connect(host=host, database=database, user=user, password=password)
cursor = conn.cursor()

# Disable all foreign keys and truncate all tables
cursor.execute("""
DO $$ 
DECLARE 
   table_name text;
BEGIN 
   FOR table_name IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
   LOOP
      EXECUTE 'ALTER TABLE ' || table_name || ' DISABLE TRIGGER ALL;';
      EXECUTE 'TRUNCATE TABLE ' || table_name || ' RESTART IDENTITY CASCADE;';
   END LOOP;
END $$;               
""")
conn.commit()

# determine table name from file name
def _get_table_name(file: str) -> str:
    if file.startswith("LOG_LOGRADOURO"):
        return "log_logradouro"
    elif file.startswith("ECT_PAIS"):
        return "ect_pais"
    elif file.startswith("LOG_"):
        return file[:-4].lower()

    print(f"Unknown file: {file}")
    return None

def _get_placeholders(row: list) -> str:
    return ",".join(["%s"] * len(row))


data_files = sorted(Path("./data/correios").glob("*.TXT"))
for file in data_files:
    with Path(file).open(encoding="ISO-8859-1") as f:
        placeholders = ""
        batch = []
        table_name = _get_table_name(file.name)
        print(f"Importing File: {file}")
        reader = csv.reader(f, delimiter="@")
        for row in reader:
            # replace empty strings with None
            row = [None if item == '' else item for item in row]

            if not placeholders:
                placeholders = _get_placeholders(row)
            batch.append(tuple(row))
            
            if len(batch) >= CHUNK_SIZE:
                sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                cursor.executemany(sql, batch)
                conn.commit()
                print(".", end="", flush=True)
                batch = []

        if batch:
            sql = f"INSERT INTO {_get_table_name(file.name)} VALUES ({placeholders})"
            cursor.executemany(sql, batch)
            conn.commit()
            print("F")


# Re-enable foreign keys check
cursor.execute("""
DO $$ 
DECLARE 
   table_name text;
BEGIN 
   FOR table_name IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
   LOOP
      EXECUTE 'ALTER TABLE ' || table_name || ' ENABLE TRIGGER ALL;';
   END LOOP;
END $$;               
""")
conn.commit()