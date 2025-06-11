package Plataformas.SantanderBootcamp.ContaBanco;

import java.util.Scanner;

public class ContaTerminal {
    public static void main(String[] args) {
        try(Scanner entrada = new Scanner(System.in)) {
            System.out.println("Digite o Numero da Agencia: ");
            int numero = entrada.nextInt();
            entrada.nextLine();
            System.out.println("Digite a Agencia: ");
            String agencia = entrada.nextLine();
            System.out.println("Digite seu Nome: ");
            String nomeCliente = entrada.nextLine();
            System.out.println("Digite o Saldo: ");
            double saldo = entrada.nextDouble();
            entrada.nextLine();

            System.out.printf("Ola %s, obrigado por criar uma conta em nosso banco," +
                                " sua agencia é %s, conta %d e seu saldo %.2f " +
                                "já esta disponivel para saque", nomeCliente, agencia, numero, saldo);

        }
    }


}
