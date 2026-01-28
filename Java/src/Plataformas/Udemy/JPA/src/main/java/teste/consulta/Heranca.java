package teste.consulta;

import infra.DAO;
import model.heranca.Aluno;
import model.heranca.AlunoBolsista;

public class Heranca {

    public static void main(String[] args) {
        DAO<Object> dao =  new DAO<>();
        AlunoBolsista alunob =  new AlunoBolsista(203203942L, "Joao", 200.0);
        Aluno aluno = new Aluno(23829397293L, "Alan");

        dao.openTransaction().persistence(aluno).persistence(alunob).closeTransaction().fechar();

    }
}
