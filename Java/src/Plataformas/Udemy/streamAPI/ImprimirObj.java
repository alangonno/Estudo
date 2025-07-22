package streamAPI;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Stream;


public class ImprimirObj {
    public static void main(String[] args) {
        List<String> lista = Arrays.asList("Gui", "lucas", "ana", "alan");

        for(String nome: lista) {
            System.out.println(nome);
        }

        System.out.println("\nUsando Iterator");
        Iterator<String> iterator = lista.iterator();

        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }

        System.out.println("\nUsando Stream");
        Stream<String> stream = lista.stream();
        stream.forEach(System.out::println);
    }
}
