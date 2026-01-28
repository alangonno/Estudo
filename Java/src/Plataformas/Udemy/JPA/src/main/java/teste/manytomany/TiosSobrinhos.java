package teste.manytomany;

import infra.DAO;
import model.muitosparamuitos.Sobrinho;
import model.muitosparamuitos.Tio;

import java.util.List;

public class TiosSobrinhos {

    public static void main(String[] args) {
        DAO<Object> dao = new DAO<>();

        Tio tio = new Tio("Tio1");
        Tio tio2 = new Tio("Tio2");

        Sobrinho sobrin = new Sobrinho("Sobrinho1");
        Sobrinho sobrin2 = new Sobrinho("Sobrinho2");

        tio.getSobrinhos().add(sobrin);
        sobrin.getTios().add(tio);

        tio2.getSobrinhos().add(sobrin2);
        sobrin2.getTios().add(tio2);

        tio2.getSobrinhos().add(sobrin);
        sobrin.getTios().add(tio2);

        tio.getSobrinhos().add(sobrin2);
        sobrin2.getTios().add(tio);

        dao.openTransaction()
                .persistence(tio)
                .persistence(tio2)
                .persistence(sobrin)
                .persistence(sobrin2)
                .closeTransaction()
                .fechar();







    }

}
