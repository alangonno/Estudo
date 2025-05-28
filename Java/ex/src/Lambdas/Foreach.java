package Lambdas;

import fundamentos.For;
import fundamentos.array.ForEach;

import java.util.Arrays;
import java.util.List;

public class Foreach {
    public static void main(String[] args) {

        List<String> aprovados = Arrays.asList("Ana", "Bia", "Lia", "Gui");

        System.out.println("Forma tradicional");
        for(String nome:aprovados) {
            System.out.println(nome);
        }

        System.out.println("\nLambda 01");
        aprovados.forEach((nome) -> System.out.println(nome));

        System.out.println("\nMethod Reference");
        aprovados.forEach(System.out::println);

        System.out.println("\nLambda2");
        aprovados.forEach(nome -> Imprimir(nome));
    }

    static void Imprimir(String nome) {
        System.out.println("Oi meu nome é " + nome);
    }
}
