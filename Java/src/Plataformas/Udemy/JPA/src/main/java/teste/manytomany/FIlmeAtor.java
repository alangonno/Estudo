package teste.manytomany;

import infra.DAO;
import model.muitosparamuitos.Ator;
import model.muitosparamuitos.Filme;

public class FIlmeAtor {

    public static void main(String[] args) {
        Filme filme = new Filme("O brilho", 7.0);

        Ator ator = new Ator("Leonardo de Caprio");
        Ator atriz = new Ator("Megan Fox");

        filme.addAtor(ator);
        filme.addAtor(atriz);

        DAO<Filme> dao =  new DAO<>();

        dao.openTransaction()
                .persistence(filme)
                .closeTransaction()
                .fechar();

    }

}
