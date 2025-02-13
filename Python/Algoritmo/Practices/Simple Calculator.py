operador = input('Digite um operador (+, -, *, /): ')
num1 = float(input('Digite o 1° valor: '))
num2 =  float(input('Digite o 2° valor: '))
if operador == '+':
    resultado = num1 + num2
    print(round(resultado, 2))
elif operador == '-':
    resultado = num1 - num2
    print(round(resultado, 2))
elif operador == '*':
    resultado = num1 * num2
    print(round(resultado, 2))
elif operador == '/':
    resultado = num1 / num2
    print(round(resultado, 2))
else:
    print(f'{operador} não é um operador valido!!')