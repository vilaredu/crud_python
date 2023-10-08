import mysql.connector
from contextlib import contextmanager

# Função para conectar ao banco de dados
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="seu_user",
        password="sua_senha",
        database="seu_banco_de_dados",
    )

# Contexto para gerenciar a conexão com o banco de dados
@contextmanager
def conexao_banco():
    conexao = conectar_db()
    cursor = conexao.cursor()
    try:
        yield cursor
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        print(f"Erro no banco de dados: {e}")
    finally:
        cursor.close()
        conexao.close()

# Função para registrar uma pessoa
def registrarPessoa(id, nome, sobre_nome):
    with conexao_banco() as cursor:
        comando = 'INSERT INTO pessoas (id, nome, sobre_nome) VALUES (%s, %s, %s)'
        valores = (id, nome, sobre_nome)
        cursor.execute(comando, valores)

# Função para procurar uma pessoa pelo nome
def procurarPessoa(nome):
    with conexao_banco() as cursor:
        comando = 'SELECT * FROM pessoas WHERE nome = %s'
        valores = (nome,)
        cursor.execute(comando, valores)
        resultado = cursor.fetchall()
        return resultado

# Função para atualizar os dados de uma pessoa
def atualizarPessoa(id, nome, sobre_nome):
    with conexao_banco() as cursor:
        comando = 'UPDATE pessoas SET nome = %s, sobre_nome = %s WHERE id = %s'
        valores = (nome, sobre_nome, id)
        cursor.execute(comando, valores)

        if cursor.rowcount > 0:
            mensagem = f'Pessoa com o ID {id} atualizada com sucesso'
        else:
            mensagem = f'Nenhuma pessoa encontrada com o ID {id}. Nenhuma atualização realizada'

        return mensagem

# Função para deletar uma pessoa
def deletarPessoa(id):
    with conexao_banco() as cursor:
        comando = 'DELETE FROM pessoas WHERE id = %s'
        valores = (id,)
        cursor.execute(comando,valores)

        if cursor.rowcount > 0:
            mensagem = f'Pessoa com o ID{id} foi DELETADA'
        else:
            mensagem = f'Nenhuma pessoa encontrada com o ID{id}'

        return mensagem
