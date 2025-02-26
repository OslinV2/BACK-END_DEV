# unidade = input('Digite a unidade (K/L): ')
# peso = float(input('Digite seu peso: '))
# if unidade == 'K':
#     peso = peso * 2.205
#     unidade = 'Lbs.'
#     print(f'O seu peso {round(peso, 1)} {unidade}')
# elif unidade == 'L':
#     peso = peso / 2.205
#     unidade = 'Kgs.'
#     print(f'O seu peso {round(peso, 1)} {unidade}')
# else:
#     print(f'{unidade} não é uma unidade valida.')
    

unidade = input('Digite a unidade (K/L): ').strip().upper()
try:
    peso = float(input('Digite seu peso: '))
    if unidade == 'K':
        peso = round(peso * 2.205, 1)
        unidade = 'Lbs.'
        print(f'O seu peso é {peso} {unidade}')
    elif unidade == 'L':
        peso = round(peso / 2.205, 1)
        unidade = 'Kgs.'
        print(f'O seu peso é {peso} {unidade}')
    else:
        print(f'"{unidade}" não é uma unidade válida. Por favor, use "K" para quilogramas ou "L" para libras.')
except ValueError:
    print("Por favor, insira um valor numérico válido para o peso.")
