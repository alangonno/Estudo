package Plataformas.Udemy.tratamentodeErros;

public class Basico {

    public static void main(String[] args) {

        Aluno a1 = null;
        try {
            imprimir(a1);
        } catch (Exception excecao) {
            System.out.println("Erro de impressao");
        }

        try {
            System.out.println(7 / 0);
        } catch (Exception execao) {
            System.out.println("Erro de divisão: " + execao.getMessage());
        }


    }

    public static void  imprimir(Aluno aluno) {
        System.out.println(aluno.nome);
    }
}
