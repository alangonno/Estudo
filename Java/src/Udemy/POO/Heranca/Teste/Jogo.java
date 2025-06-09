package POO.Heranca.Teste;

import POO.Heranca.Direcao;
import POO.Heranca.Heroi;
import POO.Heranca.Jogador;
import POO.Heranca.Monstro;

public class Jogo {
    public static void main(String[] args) {

        Jogador heroi = new Heroi(10, 10);
        Jogador monstro = new Monstro(10, 10);
        heroi.andar(Direcao.NORTE);

        System.out.println(monstro.atacar(heroi));
        System.out.println(heroi.atacar(monstro));
        System.out.println(heroi.vida);
        System.out.println(monstro.vida);

    }
}
