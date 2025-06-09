package streamAPI;

import java.util.Arrays;
import java.util.List;
import java.util.function.Function;

public class Filter {

    public static void main(String[] args) {

        List<Aluno> listadeAluno = Arrays.asList(new Aluno("Alan", 10),
                                                 new Aluno("Joao", 7),
                                                 new Aluno("Neivolas", 3),
                                                 new Aluno("James", 8.4),
                                                 new Aluno("Gomes", 5.2));

        Function<Aluno, String> saudacao =
                a -> "Parabens " + a.nome + " voce foi aprovado";

        listadeAluno.stream().
                filter(a -> a.nota >= 7).
                map(saudacao).
                forEach(System.out::println);

    }
}
