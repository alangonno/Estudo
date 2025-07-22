package streamAPI;

import java.util.Arrays;
import java.util.List;
import java.util.function.BinaryOperator;
import java.util.function.Function;
import java.util.function.Predicate;

public class ReduceDois {

    public static void main(String[] args) {

        Aluno a1 = new Aluno("Joao", 7);
        Aluno a2 = new Aluno("Alan", 5);
        Aluno a3 = new Aluno("James", 9);
        Aluno a4 = new Aluno("Gui", 2);

        List<Aluno> alunos = Arrays.asList(a1, a2, a3, a4);

        Predicate<Aluno> aprovado = aluno -> aluno.nota >= 7;

        Function<Aluno, Double> getNota =  aluno -> aluno.nota;

        BinaryOperator<Double> somaNotas = (nota1, nota2) -> nota1 + nota2;

        alunos.stream().
                filter(aprovado).
                map(getNota).
                reduce(somaNotas).
                ifPresent(System.out::println);

    }


}
