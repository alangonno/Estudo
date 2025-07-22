package POO.Heranca.Teste;

import POO.Heranca.Desafio.Carro;
import POO.Heranca.Desafio.Civic;
import POO.Heranca.Desafio.Ferrari;

public class Corrida {

    public static void main(String[] args) {
        Carro civic = new Civic();
        Carro ferrari = new Ferrari();

        System.out.println(civic.velAtual);
        System.out.println(ferrari.velAtual);
        civic.acel();
        ferrari.acel();
        System.out.println(civic.velAtual);
        System.out.println(ferrari.velAtual);
    }
}
