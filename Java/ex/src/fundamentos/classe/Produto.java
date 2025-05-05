package fundamentos.classe;

public class Produto {
    String nome;
    double preco;
    double desconto;

    Produto(String nomeInicial, double precoInicial, double descontoIncial){
        nome = nomeInicial;
        preco = precoInicial;
        desconto = descontoIncial;
    }

    Produto(){}


    double precoComDesconto() {
        return (1 - desconto) * preco;
    }
}
