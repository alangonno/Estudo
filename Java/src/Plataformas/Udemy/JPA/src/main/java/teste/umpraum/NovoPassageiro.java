package teste.umpraum;

import infra.DAO;
import model.umpraum.Assento;
import model.umpraum.Passageiro;

public class NovoPassageiro {
    public static void main(String[] args) {
        Assento assento = new Assento("D2");
        Passageiro passageiro = new Passageiro("Joao", assento);

        DAO<Object> dao = new DAO<>();
        dao.openTransaction()
                .persistence(assento)
                .persistence(passageiro)
                .closeTransaction()
                .fechar();

    }
}
