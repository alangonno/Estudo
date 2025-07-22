package Plataformas.SantanderBootcamp.bancoDigital;

public class ContaCorrente extends Conta{

    @Override
    public double calcularTaxa(double valor) {
        if (valor > 50) {
            return 10;
        }
        return 0;
    }



}
