package POO.Heranca;

public class Jogador {
    int vida = 100;
    int x = 0;
    int y = 0;

    boolean andar(Direcao direcao) {
        switch (direcao) {
            case NORTE: y++; break;
            case SUL: y-- ; break;
            case OESTE: x++; break;
            case LESTE: x--; break;
        }

        return true;
    }

    boolean atacar(Jogador inimigo) {

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
