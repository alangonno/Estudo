package POO.Composicao.Desafio;

public class ClienteTeste {
    public static void main(String[] args) {
        Cliente cliente1 = new Cliente("alan");
        Compra compra1 = new Compra();
        Produto arroz = new Produto("arroz", 20.3);
        Produto feijao = new Produto("feijao", 30.3);
        Produto mandioca = new Produto("mandioca", 45.3);
        Produto carne = new Produto("carne", 10.3);

        compra1.adicionarItem(new Item(2, arroz));
        compra1.adicionarItem(new Item(8, feijao));
        compra1.adicionarItem(new Item(5, mandioca));
        cliente1.adicionarCompra(compra1);
        System.out.println(cliente1.listaCompra.get(0).obterValorTotal());
    }



}
