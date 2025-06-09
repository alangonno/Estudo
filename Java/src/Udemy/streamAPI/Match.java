package streamAPI;

import java.util.Arrays;
import java.util.List;
import java.util.function.Predicate;

public class Match {

    public static void main(String[] args) {
        Aluno a1 = new Aluno("Joao", 7);
        Aluno a2 = new Aluno("Alan", 5);
        Aluno a3 = new Aluno("James", 9);
        Aluno a4 = new Aluno("Gui", 2);

        List<Aluno> alunos = Arrays.asList(a1, a2, a3, a4);

        Predicate<Aluno> aprovado = aluno -> aluno.nota >= 7;
        Predicate<Aluno> reprovado = aprovado.negate();

        System.out.println(alunos.stream().allMatch(aprovado)); // todos aprovados
        System.out.println(alunos.stream().anyMatch(aprovado)); //alguem aprovado?
        System.out.println(alunos.stream().noneMatch(reprovado)); // ninguem reprovado
    }

}
