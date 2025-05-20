package POO.Heranca;

public class Heroi extends Jogador{
    @Override
    boolean atacar(Jogador inimigo) {
        boolean ataque1 = super.atacar(inimigo);

        boolean ataque2 = super.atacar(inimigo);

        return ataque1 || ataque2;
    }
}
