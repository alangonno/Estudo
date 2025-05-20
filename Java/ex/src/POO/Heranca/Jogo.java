package POO.Heranca;

public class Jogo {
    public static void main(String[] args) {

        Jogador heroi = new Heroi();
        Jogador monstro = new Monstro();
        heroi.andar(Direcao.NORTE);

        System.out.println(monstro.atacar(heroi));
        System.out.println(heroi.atacar(monstro));
        System.out.println(heroi.vida);
        System.out.println(monstro.vida);

    }
}
