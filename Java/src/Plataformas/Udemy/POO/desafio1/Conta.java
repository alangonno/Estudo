package POO.desafio1;

public abstract class Conta {

    String numeroDaConta;
    double saldo = 0;
    String titular;

    void depositar(double valor) {
        this.saldo += valor;
        double taxa = calcularTaxa(valor);
        if (taxa > 0) {
            this.saldo -= taxa;
            System.out.println("Taxa de 10 reais Acrescentada");
        }
        System.out.format("Voce depositou %.2f saldo atual %.2f\n", valor, this.saldo);
    }

    void sacar (double valor) {

        if (valor <= this.saldo) {
            this.saldo -= valor;
            System.out.format("Voce sacou %.2f saldo atual %.2f\n", valor, this.saldo);
        } else System.out.format("Saldo Insuficiente\n");

    }

    public double getSaldo() {
        return saldo;
    }

    public abstract double calcularTaxa(double valor);
}
