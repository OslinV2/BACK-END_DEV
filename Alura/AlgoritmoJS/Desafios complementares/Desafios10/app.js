// 01
// function palindromo() {
//     palavra = prompt('Digite uma frase ou palavra, (pode até mesmo ser seu nome): ');
//     minusculo = palavra.toLowerCase();
//     palavrainvertida = minusculo.split('').reverse().join('');
//     if (palavra === palavrainvertida) {
//         alert(`A palavra ${palavra} é palíndromo`);
//     } else {
//         alert(`A palavra ${palavra} não é palíndromo`)
//     };
// };
// palindromo()

// 02
function numeros(n1, n2,n3) {
    let numeros = [n1, n2, n3];
    numeros.sort((a, b) => a - b);
    console.log(numeros);

}
numeros(90, 22, 44);