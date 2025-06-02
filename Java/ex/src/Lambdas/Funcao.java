package Lambdas;

import java.util.function.Function;

public class Funcao {

    public static void main(String[] args) {
        Function<Integer, String> parOuImpar = num -> num % 2 == 0 ? "Par" : "Impar";

        System.out.println(parOuImpar.apply(2));
        System.out.println(parOuImpar.apply(3));

        Function<String, String> resultado = valor -> "resultado é " + valor;

        String resultadoFinal = parOuImpar.andThen(resultado).apply(2);

        System.out.println(resultadoFinal
        );
    }
}
