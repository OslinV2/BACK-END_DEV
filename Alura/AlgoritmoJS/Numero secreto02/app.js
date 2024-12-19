// let titulo = document.querySelector('h1')
// titulo.innerHTML = 'Jogo do número secreto!'

// let paragrafo = document.querySelector('p')
// paragrafo.innerHTML = 'Escolha um numero entre 1 e 10'
let numero_secreto = gerar_numero();
let tentativas = 1;

function exibir_na_tela(tag, texto) {
    let campo = document.querySelector(tag);
    campo.innerHTML = texto;
}

function mensagem_inicial() {
    exibir_na_tela('h1', 'Jogo do número secreto!');
    exibir_na_tela('p', 'Escolha um numero entre 1 e 10');
}
mensagem_inicial();

function verificarChute() {
    let chute = document.querySelector('input').value;

    if (chute == numero_secreto) {
        exibir_na_tela('h1', 'Acertou!!');
        let palavra_tentativa = tentativas > 1 ? 'tentativas' : 'tentativa';
        let mensagem_tentativa = `Vc descobriu o numero secreto com ${tentativas} ${palavra_tentativa}`;
        exibir_na_tela('p', mensagem_tentativa);
        document.getElementById('reiniciar').removeAttribute('disabled')
    } else {
        if (chute > numero_secreto) {
            exibir_na_tela('p', 'O numero secreto é menor');
        } else {
            exibir_na_tela('p', 'O numero secreto é maior');
        }
        tentativas++;
        limparCampo();
    }
}
verificarChute();

function gerar_numero() {
    return parseInt(Math.random() * 10 + 1);
}
gerar_numero()

function limparCampo() {
    chute = document.querySelector('input');
    chute.value = '';
}

function reiniciar_jogo() {
    numero_secreto = gerar_numero();
    limparCampo();
    tentativas = 1
    mensagem_inicial();
    document.getElementById('reiniciar').setAttribute('disabled', true);
}