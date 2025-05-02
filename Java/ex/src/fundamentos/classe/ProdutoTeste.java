package fundamentos.classe;

public class ProdutoTeste {
    public static void main(String[] args) {
        Produto p1 = new Produto();
        p1.nome = "celular";
        p1.preco = 2000.20;
        p1.desconto = 0.15;

        Produto p2 = new Produto();
        p2.nome = "Note";
        p2.preco = 4050.34;
        p2.desconto = 0.20;
    }
}
