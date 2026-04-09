import unittest
from app import calcular_desconto, verificar_idade, saudacao

class TestApp(unittest.TestCase):

    def test_calcular_desconto_vip(self):
        # Teste para cliente VIP com compra abaixo de 1000
        self.assertEqual(calcular_desconto(500, "VIP"), 50.00)
        # Teste para cliente VIP com compra acima de 1000
        self.assertEqual(calcular_desconto(1200, "VIP"), 144.00) # 10% + 2% = 12% de 1200

    def test_calcular_desconto_regular(self):
        # Teste para cliente REGULAR com compra abaixo de 1000
        self.assertEqual(calcular_desconto(500, "REGULAR"), 25.00)
        # Teste para cliente REGULAR com compra acima de 1000
        self.assertEqual(calcular_desconto(1200, "REGULAR"), 84.00) # 5% + 2% = 7% de 1200

    def test_calcular_desconto_desconhecido(self):
        # Teste para cliente desconhecido com compra abaixo de 1000
        self.assertEqual(calcular_desconto(500, "OUTRO"), 0.00)
        # Teste para cliente desconhecido com compra acima de 1000
        self.assertEqual(calcular_desconto(1200, "OUTRO"), 24.00) # 0% + 2% = 2% de 1200

    def test_verificar_idade_permitido(self):
        self.assertEqual(verificar_idade(18), "Acesso permitido")
        self.assertEqual(verificar_idade(25), "Acesso permitido")

    def test_verificar_idade_negado(self):
        self.assertEqual(verificar_idade(17), "Acesso negado")
        self.assertEqual(verificar_idade(10), "Acesso negado")

    def test_saudacao_com_nome(self):
        self.assertEqual(saudacao("Ana"), "Olá, Ana!")

    def test_saudacao_sem_nome(self):
        self.assertEqual(saudacao(""), "Olá, visitante!")
        self.assertEqual(saudacao(None), "Olá, visitante!")
