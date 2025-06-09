package POO.desafio2;

public class Testte {

    public static void main(String[] args) {

        Produto p1 = new Produto("a", 20);
        Produto p2 = new Produto("c", 30);
        Produto p3 = new Produto("b", 50);

        Venda compra = new Venda();

        compra.adicionarItem(p1, 3);
        compra.adicionarItem(p2,2);
        compra.adicionarItem(p3, 10);

        compra.calcularValorTotal();

    }

}
