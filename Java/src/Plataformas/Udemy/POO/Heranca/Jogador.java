package POO.Heranca;

public class Jogador {
    public int vida = 100;
    public int x = 0;
    public int y = 0;


    Jogador(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public boolean andar(Direcao direcao) {
        switch (direcao) {
            case NORTE: y++; break;
            case SUL: y-- ; break;
            case OESTE: x++; break;
            case LESTE: x--; break;
        }

        return true;
    }

    public boolean atacar(Jogador inimigo) {

        int difX = Math.abs(this.x - inimigo.x);
        int difY = Math.abs(this.y - inimigo.y);

        if (difX == 0 && difY == 1) {
            inimigo.vida -= 10;
            return true;
        } else if ((difX == 1 && difY == 0)) {
            inimigo.vida -= 10;
            return true;
        }

        return false;

    }
}
