package Plataformas.Udemy.padroes.observer;

public class AniversarioSupresa {
    public static void main(String[] args) {
        Namorada namorada = new Namorada();
        Porteiro porteiro = new Porteiro();

        porteiro.registrarObservador(namorada);
        porteiro.monitorar();
    }

}
