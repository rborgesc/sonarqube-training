import unittest
from unittest.mock import patch, mock_open
import pandas as pd
import os

# Importa as funções do nosso módulo app.py
from src.app import (
    carregar_dados_csv,
    processar_dados_vendas,
    salvar_dados_processados,
    conectar_api_externa,
    calcular_hash_registro_v1,
    calcular_hash_registro_v2,
    validar_configuracao,
    processar_pipeline_complexo,
    csv_data, # Importa os dados CSV simulados
    api_data # Importa os dados da API simulados
)

class TestDataEngineering(unittest.TestCase):

    # --- Testes para carregar_dados_csv (Função 1) ---
    # Usamos @patch para simular a abertura de um arquivo, sem precisar de um arquivo real.
    @patch("builtins.open", new_callable=mock_open, read_data=csv_data)
    @patch("pandas.read_csv")
    def test_carregar_dados_csv_sucesso(self, mock_read_csv, mock_file_open):
        # Cenário: Carregamento de CSV com sucesso
        # Arrange (Preparar): Define o que a função mockada deve retornar
        mock_read_csv.return_value = pd.DataFrame({
            'produto': ['Produto A', 'Produto B'],
            'quantidade': [10, 5],
            'preco_unitario': [100.50, 200.00],
            'data_venda': ['2023-01-01', '2023-01-02']
        })
        
        # Act (Agir): Chama a função que estamos testando
        df = carregar_dados_csv("dados.csv", ",", "utf-8")
        
        # Assert (Verificar): Confirma se o resultado é o esperado
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        # Verifica se o pandas.read_csv foi chamado com os argumentos corretos
        mock_read_csv.assert_called_once_with(
            "dados.csv",
            sep=",",
            encoding="utf-8",
            usecols=None,
            nrows=None,
            skiprows=None,
            dtype=None,
            parse_dates=None
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("pandas.read_csv", side_effect=FileNotFoundError)
    def test_carregar_dados_csv_arquivo_nao_encontrado(self, mock_read_csv, mock_file_open):
        # Cenário: Arquivo CSV não encontrado
        # Act (Agir): Chama a função que estamos testando
        df = carregar_dados_csv("nao_existe.csv", ",", "utf-8")
        
        # Assert (Verificar): Confirma que um DataFrame vazio é retornado
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    @patch("builtins.open", new_callable=mock_open)
    @patch("pandas.read_csv", side_effect=Exception("Erro de parsing"))
    def test_carregar_dados_csv_erro_generico(self, mock_read_csv, mock_file_open):
        # Cenário: Erro genérico durante o carregamento do CSV
        # Act (Agir): Chama a função que estamos testando
        df = carregar_dados_csv("dados.csv", ",", "utf-8")
        
        # Assert (Verificar): Confirma que um DataFrame vazio é retornado
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    # --- Testes para processar_dados_vendas (Função 2) ---
    def test_processar_dados_vendas_vazio(self):
        # Cenário: DataFrame de entrada vazio
        # Arrange: Cria um DataFrame vazio
        df_vendas = pd.DataFrame()
        # Act: Chama a função
        df_processado = processar_dados_vendas(df_vendas)
        # Assert: Verifica se o resultado também é vazio
        self.assertTrue(df_processado.empty)

    def test_processar_dados_vendas_sucesso(self):
        # Cenário: Processamento normal de dados de vendas
        # Arrange: Cria um DataFrame de exemplo
        df_vendas = pd.DataFrame({
            'produto': ['A', 'B'],
            'quantidade': [10, 5],
            'preco_unitario': [100.0, 200.0]
        })
        # Act: Chama a função
        df_processado = processar_dados_vendas(df_vendas)
        # Assert: Verifica se as colunas foram adicionadas e os valores estão corretos
        self.assertIn('valor_total_item', df_processado.columns)
        self.assertIn('status', df_processado.columns)
        self.assertEqual(df_processado.loc[0, 'valor_total_item'], 1000.0)
        self.assertEqual(df_processado.loc[1, 'valor_total_item'], 1000.0)
        self.assertEqual(df_processado.loc[0, 'status'], 'Normal')


    def test_processar_dados_vendas_bug_divisao_por_zero(self):
        # Cenário: Testar o bug de divisão por zero (quantidade = 0)
        # Arrange: Cria um DataFrame com quantidade zero
        df_vendas = pd.DataFrame({
            'produto': ['C'],
            'quantidade': [0],
            'preco_unitario': [50.0]
        })
        # Act & Assert: Espera que a função não levante um erro (o bug está no app.py)
        # O SonarQube vai identificar o risco de divisão por zero, mesmo que o teste passe aqui.
        df_processado = processar_dados_vendas(df_vendas)
        self.assertIsInstance(df_processado, pd.DataFrame)
        # O valor_total_item para quantidade 0 deve ser 0
        self.assertEqual(df_processado.loc[0, 'valor_total_item'], 0.0)

    # --- Testes para salvar_dados_processados (Função 3) ---
    @patch("pandas.DataFrame.to_csv")
    def test_salvar_dados_processados_csv(self, mock_to_csv):
        # Cenário: Salvar em formato CSV
        # Arrange: Cria um DataFrame de exemplo
        df_dados = pd.DataFrame({'col1': [1, 2]})
        # Act: Chama a função
        salvar_dados_processados(df_dados, "saida.csv", "csv")
        # Assert: Verifica se o método to_csv foi chamado
        mock_to_csv.assert_called_once_with("saida.csv", index=False)

    @patch("pandas.DataFrame.to_json")
    def test_salvar_dados_processados_json(self, mock_to_json):
        # Cenário: Salvar em formato JSON
        # Arrange: Cria um DataFrame de exemplo
        df_dados = pd.DataFrame({'col1': [1, 2]})
        # Act: Chama a função
        salvar_dados_processados(df_dados, "saida.json", "json")
        # Assert: Verifica se o método to_json foi chamado
        mock_to_json.assert_called_once_with("saida.json", orient='records', indent=4)

    @patch("os.system")
    def test_salvar_dados_processados_vulnerabilidade(self, mock_os_system):
        # Cenário: Testar o caminho da vulnerabilidade (formato não suportado)
        # Arrange: Cria um DataFrame de exemplo
        df_dados = pd.DataFrame({'col1': [1, 2]})
        # Act: Chama a função com um formato inválido
        salvar_dados_processados(df_dados, "saida.log", "formato_invalido")
        # Assert: Verifica se os.system foi chamado (indicando que a vulnerabilidade foi exercitada)
        mock_os_system.assert_called_once()
        # O SonarQube ainda vai detectar a vulnerabilidade no código original.

    # --- Testes para conectar_api_externa (Função 4) ---
    def test_conectar_api_externa_clientes(self):
        # Cenário: Conectar a um endpoint de clientes
        # Act: Chama a função
        resultado = conectar_api_externa("/dados_clientes")
        # Assert: Verifica se os dados esperados são retornados
        self.assertEqual(resultado, api_data)

    def test_conectar_api_externa_outro_endpoint(self):
        # Cenário: Conectar a um endpoint desconhecido
        # Act: Chama a função
        resultado = conectar_api_externa("/outro_endpoint")
        # Assert: Verifica se um dicionário vazio é retornado
        self.assertEqual(resultado, {})

    # --- Testes para calcular_hash_registro (Função 5) ---
    def test_calcular_hash_registro_duplicacao(self):
        # Cenário: Testar as duas funções de hash para verificar duplicação
        # Arrange: Cria um registro de exemplo
        registro = {"id": 1, "nome": "Teste"}
        # Act: Calcula o hash com ambas as funções
        hash1 = calcular_hash_registro_v1(registro)
        hash2 = calcular_hash_registro_v2(registro)
        # Assert: Verifica se os hashes são iguais (indicando a mesma lógica)
        self.assertEqual(hash1, hash2)

    # --- Testes para validar_configuracao (Função 6) ---
    def test_validar_configuracao_valida(self):
        # Cenário: Configuração válida
        # Act & Assert
        self.assertTrue(validar_configuracao({"key": "value"}))

    def test_validar_configuracao_invalida(self):
        # Cenário: Configuração inválida (não é um dicionário)
        # Act & Assert
        self.assertFalse(validar_configuracao("string_invalida"))

    # --- Testes para processar_pipeline_complexo (Função 7) ---
    def test_processar_pipeline_complexo_caminho1(self):
        # Cenário: Testar um caminho específico do pipeline complexo
        # Act & Assert
        self.assertEqual(processar_pipeline_complexo(10, True, True, True, True), 20)

    def test_processar_pipeline_complexo_caminho2(self):
        # Cenário: Testar outro caminho do pipeline complexo
        # Act & Assert
        self.assertEqual(processar_pipeline_complexo(10, True, True, True, False), 5.0)

    def test_processar_pipeline_complexo_caminho3(self):
        # Cenário: Testar um terceiro caminho do pipeline complexo
        # Act & Assert
        self.assertEqual(processar_pipeline_complexo(10, True, True, False, True), 11)

    def test_processar_pipeline_complexo_caminho4(self):
        # Cenário: Testar um quarto caminho do pipeline complexo
        # Act & Assert
        self.assertEqual(processar_pipeline_complexo(10, True, False, True, True), 9)

    def test_processar_pipeline_complexo_caminho5(self):
        # Cenário: Testar o caminho final do pipeline complexo
        # Act & Assert
        self.assertEqual(processar_pipeline_complexo(10, False, True, True, True), 10)


if __name__ == '__main__':
    unittest.main()
