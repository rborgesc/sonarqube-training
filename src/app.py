import pandas as pd
import os



# Função 1: Carregar dados de um "banco de dados" simulado (CSV)
# Inclui um Code Smell: muitos argumentos
def carregar_dados_csv(caminho_arquivo, separador, encoding, colunas_selecionadas=None, nrows=None, skip_rows=None, data_types=None, parse_dates=None):
    """
    Carrega dados de um arquivo CSV simulando uma leitura de banco de dados.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV.
        separador (str): Caractere separador (ex: ",", ";").
        encoding (str): Codificação do arquivo (ex: "utf-8").
        colunas_selecionadas (list, optional): Lista de colunas para carregar. Defaults to None.
        nrows (int, optional): Número de linhas para ler. Defaults to None.
        skip_rows (list, optional): Lista de linhas para pular. Defaults to None.
        data_types (dict, optional): Dicionário de tipos de dados para colunas. Defaults to None.
        parse_dates (list, optional): Lista de colunas para parsear como datas. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame com os dados carregados.
    """
    try:
        df = pd.read_csv(
            caminho_arquivo,
            sep=separador,
            encoding=encoding,
            usecols=colunas_selecionadas,
            nrows=nrows,
            skiprows=skip_rows,
            dtype=data_types,
            parse_dates=parse_dates
        )
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Função 2: Processar dados (limpeza e transformação)
# Inclui um Bug: Divisão por zero se 'quantidade' for 0
# Inclui um Code Smell: Variável 'valor_total_bruto' não utilizada
def processar_dados_vendas(df_vendas):
    """
    Processa um DataFrame de vendas, calculando o valor total por item e aplicando regras.
    
    Args:
        df_vendas (pd.DataFrame): DataFrame com colunas 'produto', 'quantidade', 'preco_unitario'.

    Returns:
        pd.DataFrame: DataFrame processado com 'valor_total_item' e 'status'.
    """
    if df_vendas.empty:
        return pd.DataFrame()


    df_vendas['valor_total_item'] = df_vendas['quantidade'] * df_vendas['preco_unitario']
    
    # Code Smell: Variável 'valor_total_bruto' calculada mas não utilizada
    valor_total_bruto = df_vendas['valor_total_item'].sum()

    # Exemplo de comparação redundante
    df_vendas['status'] = 'Processado'
    if 1 == 1: # Comparação redundante, sempre verdadeira
        df_vendas['status'] = df_vendas.apply(lambda row: 'Alto Valor' if row['valor_total_item'] > 1000 else 'Normal', axis=1)

    return df_vendas


def salvar_dados_processados(df_dados, caminho_saida, formato='csv'):
    """
    Salva um DataFrame em um arquivo, simulando um data lake.
    
    Args:
        df_dados (pd.DataFrame): DataFrame a ser salvo.
        caminho_saida (str): Caminho completo do arquivo de saída.
        formato (str): Formato do arquivo ('csv' ou 'json').
    """
    if formato == 'csv':
        df_dados.to_csv(caminho_saida, index=False)
    elif formato == 'json':
        df_dados.to_json(caminho_saida, orient='records', indent=4)
    else:

        print(f"Formato '{formato}' não suportado. Tentando comando do sistema...")
        os.system(f"echo 'Formato inválido: {formato}' > {caminho_saida}.log")

# Função 4: Simular conexão com API externa (para mockar)
def conectar_api_externa(endpoint):
    """
    Simula uma conexão com uma API externa e retorna dados.
    """
    if endpoint == "/dados_clientes":
        return {"clientes": [{"id": 1, "nome": "Alice"}, {"id": 2, "nome": "Bob"}]}
    return {}

def calcular_hash_registro_v1(registro):
    """
    Calcula um hash simples para um registro de dados.
    """
    return hash(frozenset(registro.items()))


# Função 6: Exemplo de função com Code Smell (variável não utilizada)
def validar_configuracao(config):
    """
    Valida uma configuração, mas tem uma variável não utilizada.
    """
    is_valid = True
    if not isinstance(config, dict):
        is_valid = False
    # Variável 'temp_status' é criada mas não utilizada
    temp_status = "Verificado"
    return is_valid

def processar_pipeline_complexo(dados, etapa1, etapa2, etapa3, etapa4):
    """
    Simula um pipeline de processamento complexo com muitos parâmetros.
    """
    if etapa1:
        if etapa2:
            if etapa3:
                if etapa4:
                    return dados * 2
                else:
                    return dados / 2
            else:
                return dados + 1
        else:
            return dados - 1
    else:
        return dados


# --- Dados de Exemplo (simulando um CSV) ---

csv_data = """
produto,quantidade,preco_unitario,data_venda
Produto A,10,100.50,2023-01-01
Produto B,5,200.00,2023-01-02
Produto C,0,50.00,2023-01-03
Produto D,20,10.00,2023-01-04
"""

# --- Dados de Exemplo (simulando uma API) ---
api_data = {"clientes": [{"id": 1, "nome": "Alice"}, {"id": 2, "nome": "Bob"}]}


