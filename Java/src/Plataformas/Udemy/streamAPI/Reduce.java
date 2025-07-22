package streamAPI;

import java.util.Arrays;
import java.util.List;
import java.util.function.BinaryOperator;

public class Reduce {

    public static void main(String[] args) {
        List<Integer> lista = Arrays.asList(3, 5, 1, 7, 8, 6);

        BinaryOperator<Integer> soma = (acum, n) -> acum + n;

        int total = lista.stream().reduce(soma).get();
        System.out.println(total);


        Integer total2 = lista.parallelStream().reduce(100, soma);
        System.out.println(total2);

        lista.stream().
                filter(n -> n >= 5).
                reduce(soma).
                ifPresent(System.out::println);
    }

}
