import mysql.connector

# Conexão com o MySQL
db = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha"
)

cursor = db.cursor()

# Criar um banco de dados
cursor.execute("CREATE DATABASE IF NOT EXISTS churrasco_do_tonhao")

# Selecionar o banco de dados
cursor.execute("USE churrasco_do_tonhao")

# Criar uma tabela para reservas
cursor.execute("""
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    lugares INT NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'pedente'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emails (
       id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        email VARCHAR(20) NOT NULL,
        senha VARCHAR(20) NOT NULL
)
""")

print("Banco de dados e tabela criados com sucesso!")

# Fechar a conexão
cursor.close()
db.close()