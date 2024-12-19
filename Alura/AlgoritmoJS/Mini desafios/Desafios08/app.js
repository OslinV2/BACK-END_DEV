// 01
// function IMC(altura, peso) {
//     altura = parseFloat(prompt('Digite a sua altura em metros (ex: 1.78): '));
//     peso = parseFloat(prompt('Digite o seu peso em quilogramas (ex: 70): '));
//     let imc = peso / (altura ** 2);
//     console.log (`O calculo do seu índice de massa corporal (IMC) de acordo com seus ${altura}m e ${peso}kg é ${imc}!`);
// }
// IMC();

// 02
function valor_fatorial(numero) {
    numero = parseFloat(prompt('Digite um valor positivo: '))

    let fatorial = 1;

    for (let i = 1; i <= numero; i++) {
        fatorial *= i;
    }
    console.log(`O valor fatorial de numero ${numero} é ${fatorial}`);
}
valor_fatorial();