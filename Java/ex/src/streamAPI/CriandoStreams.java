package streamAPI;

import java.util.Arrays;
import java.util.List;
import java.util.function.Consumer;
import java.util.stream.Stream;

public class CriandoStreams {

    public static void main(String[] args) {

        Consumer<String> print = System.out::println;

        Stream<String> langs = Stream.of("Java", "Lua", "Python\n");

        langs.forEach(print);

        String[] maisLangs = {"JS", "Assembly", "Go", "PErls\n"};

        Stream.of(maisLangs).forEach(print);

        Arrays.stream(maisLangs).forEach(print);
        Arrays.stream(maisLangs, 1, 2).forEach(print);

        List<String> outralangs = Arrays.asList("Kotlin", "PHP", "C");
        outralangs.stream().forEach(print);
        outralangs.parallelStream().forEach(print);

        //Stream.generate(() -> "a").forEach(print); INFINITO
        //Stream.iterate(0, n -> n + 1); INFINITO

    }
}
