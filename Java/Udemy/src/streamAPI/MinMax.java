package streamAPI;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.function.Predicate;

public class MinMax {

    public static void main(String[] args) {

        Aluno a1 = new Aluno("Joao", 7);
        Aluno a2 = new Aluno("Alan", 5);
        Aluno a3 = new Aluno("James", 9);
        Aluno a4 = new Aluno("Gui", 2);

        List<Aluno> alunos = Arrays.asList(a1, a2, a3, a4);

        Comparator<Aluno> melhorNota = (al1,al2) -> {
            if (al1.nota > al2.nota) return 1;
            if (al1.nota < al2.nota) return -2;
            return 0;
        };

        System.out.println(alunos.stream().max(melhorNota).get());
        System.out.println(alunos.stream().min(melhorNota).get());

    }
}
