package teste.umpraum;

import infra.DAO;
import model.umpraum.Passageiro;

public class GetPassager {
    public static void main(String[] args) {
        DAO<Passageiro> dao = new DAO<>(Passageiro.class);

        dao.getAll(10,10);

    }
}
