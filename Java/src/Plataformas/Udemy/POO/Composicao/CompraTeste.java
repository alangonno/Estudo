package POO.Composicao;

public class CompraTeste {

    public static void main(String[] args) {
        Compra c1 = new Compra();
        c1.cliente = "Alan";
        c1.itens.add(new Item("caneta", 20, 7.4));
        c1.itens.add(new Item("cacete", 10, 3.4));
        c1.itens.add(new Item("coco", 5, 2.4));

        System.out.println(c1.itens.size());
        System.out.println(c1.valorTotal() );
    }
}
