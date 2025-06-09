package POO.Composicao;

public class CarroTeste {

    public static void main(String[] args) {
        Carro c = new Carro();
        System.out.println(c.estaLigado());
        c.ligar();
        System.out.println(c.estaLigado());
        System.out.println(c.motor.giros());
        c.acelerar();
        System.out.println(c.motor.giros());
        c.frear();
        c.frear();
        System.out.println(c.motor.giros());

    }
}
