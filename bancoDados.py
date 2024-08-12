# # salvo em memoria
# import sqlite3
# from faker import Faker
# import random
#
# # Inicializa o Faker para gerar dados fictícios em português brasileiro
# fake = Faker('pt_BR')
#
# # Cria uma conexão com um banco de dados em memória
# conn = sqlite3.connect(':memory:')
#
# # Cria um cursor para executar comandos SQL
# cursor = conn.cursor()
#
# # Cria a tabela 'persons' com um campo adicional 'cpf'
# cursor.execute('''
# CREATE TABLE persons (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT UNIQUE NOT NULL,
#     email TEXT UNIQUE NOT NULL,
#     age INTEGER,
#     address TEXT UNIQUE NOT NULL,
#     cpf TEXT UNIQUE NOT NULL
# )
# ''')
#
# # Define a quantidade de registros a serem inseridos
# num_records = 10
#
# # Insere registros aleatórios na tabela, incluindo o CPF
# for _ in range(num_records):
#     name = fake.name()
#     email = fake.email()
#     age = random.randint(18, 80)
#     address = fake.address()
#     cpf = fake.cpf()
#
#     cursor.execute('''
#     INSERT INTO persons (name, email, age, address, cpf)
#     VALUES (?, ?, ?, ?, ?)
#     ''', (name, email, age, address, cpf))
#
# # Seleciona e imprime os dados inseridos
# cursor.execute('SELECT * FROM persons')
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
#
# # Fecha a conexão (o banco de dados em memória é destruído)
# conn.close()

# criar arquivo
import sqlite3
from faker import Faker
import random

# Inicializa o Faker para gerar dados fictícios em português brasileiro
fake = Faker('pt_BR')

# Nome do arquivo do banco de dados
db_filename = 'pessoas.db'

# Cria uma conexão com o banco de dados em um arquivo
conn = sqlite3.connect(db_filename)

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Cria a tabela 'persons' com um campo adicional 'cpf'
cursor.execute('''
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    city TEXT,
    state TEXT,
    country TEXT,
    cpf TEXT UNIQUE NOT NULL
)
''')

# Define a quantidade de registros a serem inseridos
num_records = 100

# Insere registros aleatórios na tabela, incluindo o CPF
for _ in range(num_records):
    name = fake.name()
    email = fake.email()
    age = random.randint(18, 80)
    city = fake.city()
    state = fake.state()
    country = fake.country()
    cpf = fake.cpf()

    cursor.execute('''
    INSERT INTO persons (name, email, age, city, state, country, cpf)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, age, city, state, country, cpf))

# Confirma as alterações
conn.commit()

# Seleciona e imprime os dados inseridos
cursor.execute('SELECT * FROM persons')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Fecha a conexão com o banco de dados
conn.close()

print(f"Dados foram salvos no arquivo '{db_filename}'.")
