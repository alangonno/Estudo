package POO.Heranca.Desafio;

public class Ferrari extends Carro implements Esportivo {


    public Ferrari() {
        super(300);
    }

    @Override
    public boolean acel() {
        for (int a = 0; a <= 2; a++) {
            super.acel();
        }
        return true;
    }

    @Override
    public void ligarTurbo() {
        for (int a = 0; a <= 5; a++) {
            super.acel();
        }

    }

    @Override
    public void desligarTurbo() {
        for (int a = 0; a <= 5; a++) {
            super.freiar();
        }

    }
}