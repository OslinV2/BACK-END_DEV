alert('Bem-vindo ao jogo do número secreto!!');
numero_maximo = parseInt(Math.random() * 1000)
let numero_secreto = parseInt(Math.random() * numero_maximo + 1);
console.log(numero_secreto);
let chute;
let tentativas = 1;
while (chute != numero_secreto) {
    chute = prompt(`Escolha um valor entre 1 a ${numero_maximo} (Tenta a sorte): `);

    if (chute == numero_secreto) {
        break
    } else {
        if (chute > numero_secreto) {
            alert(`Tenta um pouco mais baixo, 'Vai com tudo'`);
        } else {
            alert(`Um pouco mais alto, 'Vc consege'`);
        }
        // alert(`Errouuu!!. O número secreto era ${numero}, mas você escolheu ${chute}`);
    } 
    // tentativas = tentativas + 1;
    tentativas++
}
let tentativa = tentativas > 1 ? 'tentativas' : 'tentativa'
alert(`Descobriu o numero: ${numero_secreto}, depois de ${tentativas} ${tentativa}`);

// if (tentativas > 1 ) {
//     alert(`Acerto. Depois de ${tentativas}tentativa, é o numero: ${numero}`);
// } else {
//     alert(`Acerto. Depois de ${tentativas}tentativas, é o numero: ${numero}`);
// }
