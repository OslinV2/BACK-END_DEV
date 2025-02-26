unidade = input('Digite a unidade desejada (C/Celsius ou F/Fahrenheit): ').strip().upper()
temp = float(input('Digite a temperatura: '))
if unidade == 'C':
    temp = round((9 * temp) / 5 + 32, 2)
    print(f'A temperatura em Fahrenheit é {temp}°F')
elif unidade == 'F':
    temp = round((temp - 32) * 5 / 9, 2)
    print(f'A temperatura em Celsius é {temp}°C')
else:
    print(f'{unidade} não é uma unidade válida Por favor, insira C ou F')