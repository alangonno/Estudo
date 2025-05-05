package fundamentos.classe;

public class Produto {
    String nome;
    double preco;
    double desconto;

    double precoComDesconto() {
        return (1 - desconto) * preco;
    }
}
