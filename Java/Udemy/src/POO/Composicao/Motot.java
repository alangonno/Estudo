package POO.Composicao;

public class Motot {

    boolean ligado = false ;
    double fatorInjecao = 1;

    double giros() {
        if (!ligado) {
            return 0;
        } else {
        return fatorInjecao * 3000;
    }
    }
}
