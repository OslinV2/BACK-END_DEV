// 01
dia = prompt('Qual é o dia de hoje? ')
if (dia == 'Sábado'|| dia == 'Domingo') {
    alert("Bom Final de semana!!")
} 
    else if (dia == 'Segunda') {
    alert('Vc tá iniciando a semana com tudo!!')
} 
else {
    alert("Boa Semana, pra vc!!!")
}

// 02
valor = prompt('Digite um valor: ')
if (valor == 0) {
    alert(`O número ${valor} é nulo!!`)
} else if (valor >= 0) {
    alert(`O número ${valor} é Positivo.`)
}
else {
    alert(`O valor ${valor} é negativo.`)
}

// 03
pontuacao = prompt('Qual foi a sua pontuação no jogo?')
if (pontuacao >= 100) {
    alert(`${pontuacao} pontos, parabéns!.`)
} else {
    alert('Tente novamente na proxima vez!.')
}

// 04
Conta = prompt('Digite o usuario da conta: ')
saldo = 150.0;
msg = `${Conta}, O seu saldo disponivel é de ${saldo}R$`
alert(msg)

// 05
nome = prompt('Digite su nome completo: ')
alert(`Bem vindo!! ${nome}`)
