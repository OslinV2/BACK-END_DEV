function sortear() {
    let quantidade = parseInt(document.getElementById('quantidade').value);
    let de = parseInt(document.getElementById('de').value);
    let ate = parseInt(document.getElementById('ate').value);
    
    let sorteados = [];
    let numero;
    for (let i = 0; i < quantidade; i++) {
        numero = numeroaleatorio(de, ate)

        while (sorteados.includes(numero)) {
            numero = numeroaleatorio(de, ate)
        }; 
        sorteados.push(numero);
    }

    let resultado = document.getElementById('resultado');
    resultado.innerHTML = `<label class="texto__paragrafo">Números sorteados: ${sorteados} </label>`
    
    if (de >= ate) {
        resultado.innerHTML = `<label class="texto__paragrafo">Números sorteados: Valor indefinido, tente novamente.</label>`
        alert('Campo "Do número" deve ser inferior ao campo "Até o número". Verifique!');
    } 
    
    if (quantidade > (ate - de + 1)) {
        alert('Campo "Quantidade" deve ser menor ou igual ao intervalo informado no campo "Do número" até o campo "Até o número". Verifique!');
        return;
    }
    reiniciar();
}
function numeroaleatorio(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}

function alterarStatus() {
    let botao = document.getElementById('btn-reiniciar');
    if (botao.classList.contains('container_botao-desabilitado')) {
        botao.classList.remove('container_botao-desabilitado');
        botao.classList.add('container_botao');
    } else {
        botao.classList.remove('container_botao');
        botao.classList.add('container_botao-desabilitado');
    }
};

function reiniciar() {
    document.getElementById('quantidade').value = '';
    document.getElementById('ate').value = '';
    document.getElementById('de').value = '';
    document.getElementById('resultado').innerHTML = '<label class="texto__paragrafo">Números sorteados:  nenhum até agora</label>'
    alterarStatus();
};


// function reiniciar() {
    // Selecionar todos os campos de entrada com base na classe 'container__input'
//     let campos = document.querySelectorAll('.container__input');
    
    // Iterar sobre todos os campos e limpar o valor
//     campos.forEach(campo => {
//         campo.value = ''; // Limpar o valor do campo
//     });
// }


// function exibir_numeros(tag, campo) {
//     let campo = document.querySelector(tag)
//     campo.innerHTML = texto;
// }

// exibir_numeros('label', `Números sorteados: ${sorteados}`);