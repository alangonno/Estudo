package teste.consulta;

import infra.DAO;
import model.muitosparamuitos.Ator;
import model.muitosparamuitos.Filme;

import java.util.List;

public class ObterFilme {

    public static void main(String[] args) {

        DAO<Filme> dao = new DAO<>(Filme.class);
        List<Filme> filmes = dao.consultar("filmesNotaMaiorQue", "nota", 8.5);

        for(Filme filme: filmes) {
            System.out.println(filme.getNome());

            for(Ator ator: filme.getAtores()){
                System.out.println(ator.getNome());
            }
        }
    }



}
