package POO.Heranca.Desafio;

public class Carro {

    public int velAtual;
    private final int VEL_MAX;

    protected Carro(int velMax) {
        VEL_MAX = velMax;
    }

    public boolean acel() {
        if(velAtual + 5 > VEL_MAX) {
            return false;
        }
        velAtual += 5;
        return true;
    }

    public boolean freiar() {
        if (velAtual - 5 < 0) {
            return false;
        }
        velAtual -= 5;
        return true;
    }
}
