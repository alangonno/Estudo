package POO.Heranca.Desafio;

public class Ferrari extends Carro {


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
}