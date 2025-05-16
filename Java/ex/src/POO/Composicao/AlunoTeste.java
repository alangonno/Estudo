package POO.Composicao;

public class AlunoTeste {

    public static void main(String[] args) {

        Aluno aluno1 = new Aluno("alan");
        Aluno aluno2 = new Aluno("al");
        Aluno aluno3 = new Aluno("an");

        Curso curso1 = new Curso("Java");
        Curso curso2 = new Curso("JS");
        Curso curso3 = new Curso("HTML");

        curso1.adicionarAluno(aluno1);
        aluno2.adicionarCurso(curso2);
        curso1.adicionarAluno(aluno3);

        for(Aluno aluno: curso1.alunos) {
            System.out.println(aluno.nome);
    }
        for(Curso curso: aluno1.cursos) {
            System.out.println(curso.nome);
        }
}
}
