// 01
function ola_mundo() {
    console.log('Olá, mundo!')
}
ola_mundo()

// 02
function parametro_nome(nome) {
    console.log(`Olá, ${nome}`)
}
parametro_nome('carlens')

// 03
function dobro(numero) {
    console.log(`O dobro de ${numero} é ${numero * 2}`)
}
dobro(22)

// 04
// function media(n1, n2, n3, media)  {
//     n1 = parseFloat(prompt('Digite um valor: '))
//     n2 = parseFloat(prompt('Digite outro valor: '))
//     n3 = parseFloat(prompt('Digite um ultimo valor: '))
//     media = ((n1 + n2 + n3) / 3).toFixed(1);
//     console.log(`A média dos valores ${n1}, ${n2} e ${n3} é ${media}`);
//     // console.log(`A média dos valores: ${n1}, ${n2} e ${n3} é ${((n1 + n2 + n3) / 3).toFixed(3)}`)
// }
// media()

// 05
// function numero_maior(n1, n2) {
//     n1 = prompt('Digite um valor: ')
//     n2 = prompt('Digite outro valor: ')
//     if (n1 > n2) {
//         console.log(`Entre os valores: ${n1} e ${n2} o maior é ${n1}`)
//     } else {
//         console.log(`Entre os valores: ${n1} e ${n2} o maior é ${n2}`)
//     }
// }
// numero_maior()

// 06
function multiplicado_por_si_mesmo(num) {
    num = parseFloat(prompt('Digite um numero: '))
    console.log(`O numero ${num} multiplicado por si mesmo é ${num * num}`)
}
multiplicado_por_si_mesmo()

