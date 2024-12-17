// let titulo = document.querySelector('h1')
// titulo.innerHTML = 'Jogo do número secreto!'

// let paragrafo = document.querySelector('p')
// paragrafo.innerHTML = 'Escolha um numero entre 1 e 10'
let numero_secreto = gerar_numero();

function interacao_do_txt_HTML(tag, texto) {
    let campo = document.querySelector(tag);
    campo.innerHTML = texto;
}
interacao_do_txt_HTML('h1', 'Jogo do número secreto!');
interacao_do_txt_HTML('p', 'Escolha um numero entre 1 e 10');

function verificarChute() {
    let chute = document.querySelector('input').value;
    console.log(chute == numero_secreto);
}

function gerar_numero() {
    return parseInt(Math.random() * 10 + 1);
}