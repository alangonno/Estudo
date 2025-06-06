package streamAPI;

import java.util.Arrays;
import java.util.List;

public class Outros {
    public static void main(String[] args) {
        Aluno a1 = new Aluno("Joao", 7);
        Aluno a2 = new Aluno("Alan", 5);
        Aluno a3 = new Aluno("James", 9);
        Aluno a4 = new Aluno("Gui", 2);

        Aluno a5 = new Aluno("Joao", 10);
        Aluno a6 = new Aluno("Alan", 5);
        Aluno a7 = new Aluno("mes", 9);
        Aluno a8 = new Aluno("ui\n", 2);

        List<Aluno> alunos = Arrays.asList(a1, a2, a3, a4, a5, a6, a7, a8);

        alunos.stream().distinct().forEach(System.out::println);

        alunos.stream().distinct().skip(2).limit(2).forEach(System.out::println);
    }

}
