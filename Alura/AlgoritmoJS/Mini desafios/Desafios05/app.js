// 01
// Baixar o arquivo e abrir
// 02
let conteudo_h1 = document.querySelector('h1');
conteudo_h1.innerHTML = 'Hora do Desafio!!'
// 03
function botao_clicado() {
    console.log('O botão foi clicado!!');
}
// 04
function mensagem_alert() {
    console.log('Eu amo JS!!');
}
// 05
function cidade() {
    cidade = prompt('Digite o nome de umam cidade: ');
    alert(`Quando eu estiver em ${cidade}, lembrarei de você!`);
}
// 06
function soma() {
    let n1 = Number(prompt('Digite um 1° valor: '));
    let n2 = Number(prompt('Digite um 2° valor: '));
    alert(`A soma entre ${n1} e ${n2} é ${n1 + n2}.`);
}