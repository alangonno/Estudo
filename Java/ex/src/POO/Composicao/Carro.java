package POO.Composicao;

public class Carro {

    Motot motor = new Motot();

    void acelerar () {
        motor.fatorInjecao += 0.4;
    }

    void frear() {
        motor.fatorInjecao -= 0.4;
    }

    void ligar() {
        motor.ligado = true;
    }

    void desligar() {
        motor.ligado = false;
    }

    boolean estaLigado() {
        return motor.ligado;
    }
}
