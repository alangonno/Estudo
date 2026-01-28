package teste.umpraum;

import infra.DAO;
import model.umpraum.Assento;
import model.umpraum.Passageiro;

public class NewPasseger {
    public static void main(String[] args) {

        Assento assento = new Assento("A32");
        Passageiro passageiro = new Passageiro("Ruan", assento);

        DAO<Passageiro> dao = new DAO<>();

    }
    }
