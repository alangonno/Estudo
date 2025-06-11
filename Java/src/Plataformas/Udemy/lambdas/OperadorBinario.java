package lambdas;

import java.util.function.BiFunction;
import java.util.function.BinaryOperator;

public class OperadorBinario {
    public static void main(String[] args) {
        BinaryOperator<Double> media = (n1, n2) -> (n1 + n2) / 2;
        System.out.println(media.apply(6.2, 7.8));

        BiFunction<Double, Double, String> resultado = (n1, n2) ->
                (n1 + n2) / 2 >= 7 ? "AProvado" : "Reprovado";

        System.out.println(resultado.apply(9.2, 3.3));

    }
}
