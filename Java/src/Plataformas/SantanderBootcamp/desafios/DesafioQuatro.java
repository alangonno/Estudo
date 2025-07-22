package Plataformas.SantanderBootcamp.desafios;

import java.util.Scanner;

    public class DesafioQuatro {
        public static void main(String[] args) {

            try(Scanner entrada = new Scanner(System.in)) {

                int numero = entrada.nextInt();
                entrada.nextLine();

                String titular = entrada.nextLine();

                String valorComoTexto = entrada.nextLine();

                double saldo = Double.parseDouble(valorComoTexto);

                if (saldo < 0) {
                    System.out.println("Erro: O saldo nao pode ser negativo.");
                    return;
                }

                valorComoTexto = entrada.nextLine();

                double deposito = Double.parseDouble(valorComoTexto);

                if (deposito <= 0) {
                    System.out.println("Erro: O valor do deposito deve ser positivo.");
                    entrada.close();
                    return;
                }

                ContaBancaria conta = new ContaBancaria(numero, titular, saldo);

                conta.depositar(deposito);

                conta.exibirSaldo(conta);

            }
        }
    }


