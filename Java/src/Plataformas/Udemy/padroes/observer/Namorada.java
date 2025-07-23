package Plataformas.Udemy.padroes.observer;

public class Namorada implements ObservadorChegadaAniversariante{

    @Override
    public void chegou(EventoChegadaAniversariante evento) {
        System.out.println("Apaga as luzes");
        System.out.println("SURPRESA!!!");
    }
}
