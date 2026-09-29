import psycopg2

conn = psycopg2.connect(
    host="aws-0-ca-central-1.pooler.supabase.com",
    database="postgres",
    user="postgres.enpxavacjbonztqcdzag",
    password="73196580Goku",
    port=5432,
    sslmode="require"
)

print("Conectou!")
conn.close()