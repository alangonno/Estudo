package POO.Heranca.Desafio;

public class Carro {

    int velAtual;

    boolean acel() {
        velAtual += 5;
        return true;
    }

    boolean freiar() {
        velAtual -= 5;
        return true;
    }
}
