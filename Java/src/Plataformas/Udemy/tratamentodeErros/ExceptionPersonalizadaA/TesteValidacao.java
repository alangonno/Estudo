package Plataformas.Udemy.tratamentodeErros.ExceptionPersonalizadaA;

import Plataformas.Udemy.tratamentodeErros.Aluno;

public class TesteValidacao {

    public static void main(String[] args) {

        try {
            Aluno aluno = new Aluno("Alan", -2);
            Validar.aluno(aluno);

        } catch (StringVaziaException | NumeroNegativoException e) {
            System.out.println(e.getMessage());
        }
    }
}
