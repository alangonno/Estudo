package streamAPI;

import java.util.Arrays;
import java.util.List;
import java.util.function.BiFunction;
import java.util.function.BinaryOperator;
import java.util.function.Function;
import java.util.function.Predicate;

public class ReduceTres {
    public static void main(String[] args) {
        Aluno a1 = new Aluno("Joao", 7);
        Aluno a2 = new Aluno("Alan", 5);
        Aluno a3 = new Aluno("James", 9);
        Aluno a4 = new Aluno("Gui", 2);

        List<Aluno> alunos = Arrays.asList(a1, a2, a3, a4);

        Predicate<Aluno> aprovado = aluno -> aluno.nota >= 7;
        Function<Aluno, Double> getNota = aluno -> aluno.nota;
        BiFunction<Media, Double, Media> calcularMedia =
                (media, nota) -> media.adicionar(nota);

        BinaryOperator<Media> combinarMedia =
                (m1,m2) -> Media.combinar(m1,m2);

        Media media = alunos.stream().
                        filter(aprovado).
                        map(getNota).
                        reduce(new Media(),calcularMedia, combinarMedia);

         System.out.println(media.getMedia());


    }

}
