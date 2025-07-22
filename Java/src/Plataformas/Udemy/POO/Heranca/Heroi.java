package POO.Heranca;

public class Heroi extends Jogador{

    public Heroi(int x, int y) {
        super(x,y);
    }

    @Override
    public boolean atacar(Jogador inimigo) {
        boolean ataque1 = super.atacar(inimigo);

        boolean ataque2 = super.atacar(inimigo);

        return ataque1 || ataque2;
    }
}
