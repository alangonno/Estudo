package Lambdas;

import java.util.function.Predicate;

public class PredicadoComposicao {

    public static void main(String[] args) {
        Predicate<Integer> isPar = num -> num % 2 == 0;
        Predicate<Integer> isTresDigi = num -> num >= 100 && 999 >= num;

        System.out.println(isPar.and(isTresDigi).test(888));
    }
}
