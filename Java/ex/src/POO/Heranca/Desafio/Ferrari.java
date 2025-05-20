package POO.Heranca.Desafio;

public class Ferrari extends Carro {

    @Override
    boolean acel() {
        for (int a = 0; a <= 2; a++) {
            super.acel();
        }
        return true;
    }
}