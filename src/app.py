def calcular_desconto(valor_compra, tipo_cliente):
    """
    Calcula o valor do desconto com base no valor da compra e tipo de cliente.
    Clientes 'VIP' têm 10% de desconto, clientes 'REGULAR' têm 5%.
    Compras acima de 1000 reais recebem um desconto adicional de 2%.
    """
    desconto_base = 0
    desconto_adicional = 0

    if tipo_cliente == "VIP":
        desconto_base = 0.10
    elif tipo_cliente == "REGULAR":
        desconto_base = 0.05
    else:
        # Cliente desconhecido não recebe desconto base
        desconto_base = 0

    if valor_compra > 1000:
        desconto_adicional = 0.02

    desconto_total = valor_compra * (desconto_base + desconto_adicional)
    return round(desconto_total, 2)

def verificar_idade(idade):
    """
    Verifica se a idade é suficiente para acesso.
    Idade mínima para acesso é 18 anos.
    """
    if idade >= 18:
        return "Acesso permitido"
    else:
        return "Acesso negado"


# def saudacao(nome):
#     """
#     Retorna uma saudação personalizada.
#     """
#     if nome:
#         return f"Olá, {nome}!"
#     else:
#         return "Olá, visitante!"
    

def calcular_preco_final(preco, desconto_percentual):
    # Bug: Se desconto_percentual for 0, ele ainda subtrai 0.0
    # Code Smell: Variável 'valor_desconto' não utilizada
    if desconto_percentual > 0:
        valor_desconto = preco * (desconto_percentual / 100)
        preco_com_desconto = preco - (preco * (desconto_percentual / 100))
        return preco_com_desconto
    else:
        return preco
    
def saudacao(nome):
    mensagem = "Olá, " + nome + "!"
    return mensagem # Code Smell: Variável 'mensagem' é redundante
