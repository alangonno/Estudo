package Lambdas;

import java.util.List;
import java.util.Arrays;
import java.util.function.Consumer;

public class Consumidor {
    public static void main(String[] args) {
        Consumer<Produto> imprimir = prod -> System.out.println(prod.nome);
        Produto prod1 = new Produto("Note", 30000, 0.2);
        imprimir.accept(prod1);
        Produto prod2 = new Produto("Nte", 3000, 0.2);
        Produto prod3 = new Produto("ote", 300, 0.2);
        Produto prod4 = new Produto("Not", 30, 0.2);

        List<Produto> produtos = Arrays.asList(prod1, prod4, prod2, prod3);
        produtos.forEach( prods -> imprimir.accept(prods));
        produtos.forEach(imprimir);


    }



}
