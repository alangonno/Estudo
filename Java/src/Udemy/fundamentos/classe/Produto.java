package fundamentos.classe;

public class Produto {
    String nome;
    double preco;
    static double desconto = 0.25;

    Produto(String nomeInicial, double precoInicial){
        nome = nomeInicial;
        preco = precoInicial;
    }

    Produto(){}


    double precoComDesconto() {
        return (1 - desconto) * preco;
    }
}
