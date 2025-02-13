let Total_geral;
limpar();

function adicionar() {
    // recuperar valores nome do produto, quantidade e valor
    let produto = document.getElementById('produto').value;
    let nome_produto = produto.split('-')[0];
    let valor_produto = parseFloat(produto.split('R$')[1]);
    let quantidade = parseInt(document.getElementById('quantidade').value); 
    if (isNaN(valor_produto) || isNaN(quantidade)) {
        alert('Erro: Digite valores válidos para produto e quantidade.');
        document.getElementById('quantidade').value = ''; // Limpa o campo de quantidade
        return;
    }
    // Calcular o preço, o nosso subtotal
    let preco = quantidade * valor_produto;
    carrinho = document.getElementById('lista-produtos');
    // Adicionar no carrinho
    carrinho.innerHTML = carrinho.innerHTML + `<section class="carrinho__produtos__produto">
        <span class="texto-azul">${quantidade}x</span> ${nome_produto} <span class="texto-azul">R$${preco}</span>
        </section>`;
    // Atualizar o valor total
    Total_geral = Total_geral + preco;
    valor_total = document.getElementById('valor-total');
    valor_total.textContent = `R$${Total_geral}`
    document.getElementById('quantidade').value = '';
}

function limpar() {
    Total_geral = 0;
    document.getElementById('lista-produtos').innerHTML = '';
    document.getElementById('valor-total').innerHTML = 'R$0';
}
limpar();

