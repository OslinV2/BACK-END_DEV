// Forma principal
let alugados = 0
function alterarStatus(id) {
    let game = document.getElementById(`game-${id}`);
    let item_imagem = game.querySelector('.dashboard__item__img');
    let item_button = game.querySelector('.dashboard__item__button');
    let nomeJogo = game.querySelector('.dashboard__item__name');

    if (item_imagem.classList.contains('dashboard__item__img--rented')) {
        let confirmacao = confirm(`Tem certeza que deseja devolver o jogo "${nomeJogo.textContent}"?`);
        if (confirmacao == true) {
            item_imagem.classList.remove('dashboard__item__img--rented');
            item_button.classList.remove('dashboard__item__button--return');
            item_button.textContent = 'Alugar';
        }
    } else { 
        item_imagem.classList.add('dashboard__item__img--rented');
        item_button.classList.add('dashboard__item__button--return');
        item_button.textContent = 'Devolver';
        alugados++
    };
    console.log(alugados)
    jogosAlugados();
};

function jogosAlugados() {
    contador = document.getElementById('contador-alugados')
    contador.textContent = `No total foram ${alugados} jogos alugados.`
};



// Forma alternativa
// function alterarStatus(id) {
//     let game = document.getElementById(`game-${id}`);
//     let item_imagem = game.querySelector('.dashboard__item__img');
//     let item_button = game.querySelector('.dashboard__item__button');
//     let situacao_button = game.querySelector('a');

//     if (situacao_button.textContent.trim() === 'Alugar') {
//         item_button.classList.add('dashboard__item__button--return');
//         item_imagem.classList.add('dashboard__item__img--rented');
//         situacao_button.textContent = 'Devolver';
//     } else {
//         item_button.classList.remove('dashboard__item__button--return');
//         item_imagem.classList.remove('dashboard__item__img--rented');
//         situacao_button.textContent = 'Alugar';
//     }
// };