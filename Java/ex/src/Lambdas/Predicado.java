package Lambdas;

import java.util.function.Predicate;

public class Predicado {
    public static void main(String[] args) {
        Predicate<Produto> isCaro = prod -> (prod.preco * (1 - prod.desconto)) >= 100;

        Produto prod1 = new Produto("Note", 3000, 0.2);
        System.out.println(isCaro.test(prod1));

    }
}
