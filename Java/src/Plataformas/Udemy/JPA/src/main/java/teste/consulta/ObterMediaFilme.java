package teste.consulta;

import infra.DAO;
import model.consulta.NotaFilme;
import model.muitosparamuitos.Filme;

public class ObterMediaFilme {

    public static void main(String[] args) {
        DAO<NotaFilme> dao = new DAO<>(NotaFilme.class);
        NotaFilme notaMediaFilme = dao.consultarUm("MediaGeralDosFilmes");

        System.out.println(notaMediaFilme.getMedia());

        dao.fechar();


    }

}
