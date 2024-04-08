#   elif salario_bruto >= 3856.95 and salario_bruto <= 7507.29:
#         return salario_bruto * 0.14
#     else:

# Função para calcular o desconto INSS
def calcular_inss(salario_bruto):
    if salario_bruto <= 1.320:
        return salario_bruto * 0.075
    elif salario_bruto >= 1320.01 and salario_bruto <= 2571.29:
        return salario_bruto * 0.09
    elif salario_bruto >= 2571.30 and salario_bruto <= 3856.94:
        return salario_bruto * 0.12
    else: 
        return salario_bruto * 0.14

# Função para calcular o desconto INSS
def calcular_irrf(salario_liquido):
    if salario_liquido <= 2112:
        return 0
    elif salario_liquido >= 2112.01 and salario_liquido <= 2826.65:
        return (salario_liquido * 0.075) - 158.40
    elif salario_liquido >= 2826.66 and salario_liquido <= 3751.05:
        return (salario_liquido * 0.15) - 370.40
    elif salario_liquido >= 3751.06 and salario_liquido <= 4664.68:
        return (salario_liquido * 0.225) - 651.73
    else:
        return (salario_liquido * 0.275) - 884.96

# Função para calcular hora extra
def calcular_hora_extra(salario_bruto, horas_extras_trabalhadas):
    valor_por_hora = salario_bruto / 220 # 220 é valor da carga horária mensal
    valor_adicional = valor_por_hora * 0.5 #0.5 por causa que é 50% do valor da hora extra
    return horas_extras_trabalhadas * (valor_por_hora + valor_adicional)
    
    
# salario_bruto = float(input("Digite o salário bruto: R$ "))
# horas_extras_trabalhadas = float(input("Digite as horas extras trabalhadas no mês: "))

# desconto_inss = calcular_inss(salario_bruto)

# salario_liquido = salario_bruto - desconto_inss

# desconto_irrf = calcular_irrf(salario_liquido)

# aproveito_horas_adicionais = calcular_hora_extra(salario_bruto, horas_extras_trabalhadas)

# salario_final = salario_liquido + aproveito_horas_adicionais - desconto_irrf

# print ("\n### Folha de Salário ###")
# print (f"Salário Bruto: R${salario_bruto:.2f}")
# print (f"Horas Extras: {aproveito_horas_adicionais}")
# print (f"Descontos INSS: R${desconto_inss:.2f}")
# print (f"Descontos IRRF: R${desconto_irrf:.2f}")
# print ("---------------------------------------")
# print (f"Salário Final: R${salario_final:.2f}")