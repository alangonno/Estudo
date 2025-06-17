package Plataformas.SantanderBootcamp.desafios;

public class ContaBancaria {
        private int numero;
        private String titular;
        private double saldo;

        ContaBancaria(int numero, String titular, double saldo) {
            this.numero = numero;
            this.titular = titular;

            if (saldo < 0) {
                System.out.println("Erro: O saldo nao pode ser negativo.");
                return;
            }

            this.saldo = saldo;
        }


        public void depositar(double valor) {
            if (valor <= 0) {
                System.out.println("Erro: O valor do depósito deve ser positivo.");
                return;
            }
            saldo += valor;
        }

        public void exibirSaldo(Plataformas.SantanderBootcamp.desafios.ContaBancaria conta){
            System.out.printf("Conta #%d - Titular: %s - Saldo: R$%.2f", conta.numero, conta.titular.toLowerCase(), conta.saldo);

        }

    }

