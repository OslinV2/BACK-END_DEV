// 01
// function IMC(altura, peso) {
//     altura = parseFloat(prompt('Digite a sua altura em metros (ex: 1.78): '));
//     peso = parseFloat(prompt('Digite o seu peso em quilogramas (ex: 70): '));
//     let imc = peso / (altura ** 2);
//     console.log (`O calculo do seu índice de massa corporal (IMC) de acordo com seus ${altura}m e ${peso}kg é ${imc}!`);
// }
// IMC();

// 02
// function valor_fatorial(numero) {
//     numero = parseFloat(prompt('Digite um valor positivo: '))
    
    // Caso de numero negativo
//     if (isNaN(numero) || numero < 0) {
//         console.log("Por favor, insira um número positivo válido.");
//         return;
//     }
    // aso de numero = 0
//     if (numero == 0) {
//         console.log( `O fatorial do número 0 é 1`);
//         return 1;
//     }
    // Formula do fatoria
//     let fatorial = 1n;
//     for (let i = 1n; i <= BigInt(numero); i++) {
//         fatorial *= i;
//     }
//     console.log(`O fatorial do numero ${numero} é ${fatorial.toString()}.`)
//     return fatorial;
// }
// Chamada da função
// valor_fatorial();

// 03
// function conversorRealParaDolar(dolar) {
//     valorEmReais = parseFloat(prompt('Digite o valor em R$: '))
//     CotacaoDolar = valor / 4.80
//     console.log(`${valorEmReais} reais equivale a ${CotacaoDolar.toFixed(2)} doláres EUA.`)
// }

// conversor();

// Formato de variavel reutilizavel
// function converterDolarParaReal(dolar) {
//     const cotacaoDolar = 4.80;
//     return dolar * cotacaoDolar;
// }

// const valorEmDolar = 100;
// const valorEmReais = converterDolarParaReal(valorEmDolar);
// console.log(`${valorEmDolar} dólares é equivalente a R$${valorEmReais}`);


// 04
// function calculo_de_area_e_perimetro(altura, largura) {
    // Interação
//     altura = parseFloat(prompt('Digite a altura da sala: '))
//     largura = parseFloat(prompt('Digite a largura da sala: '))

    // Identificação de valores nulos
//     if (isNaN(altura) || isNaN(largura) || altura <= 0 || largura <= 0) {
//         console.log("Por favor, insira valores válidos para a altura e a largura.");
//         return;
//     }
    // Formula do calculo
//     const area = altura * largura
//     const perimetro = 2 * (altura + largura)
//     console.log(`De acordo com ${altura.toFixed(2)} de altura e ${largura.toFixed(2)} de largura, a sala tem uma ${area.toFixed(2)} de área e ${perimetro.toFixed(2)} de perímetro.`)
// }
// calculo_de_area_e_perimetro();

// 05
// function area_e_perimetro(raio) {
//     const PI = 3.14;
//     let area = PI * Math.pow(raio, 2);
//     let perimetro = 2 * PI * raio;

//     console.log(`De acordo com o raio de ${raio} metros, a área dessa sala circular é ${area} m².`);
//     console.log(`De acordo com o raio de ${raio} metros, o perímetro da sala é ${perimetro.toFixed(2)} metros.`);
// }

// let raio = 5;
// area_e_perimetro(raio);

function tabuada (numero) {
    for (let i = 1; i <= 10; i++) {
        console.log(`${numero} X ${i} = ${numero * i}`)
    }
}
let numero = 8;
tabuada(numero)