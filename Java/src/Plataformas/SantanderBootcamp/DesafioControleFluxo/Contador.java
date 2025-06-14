package Plataformas.SantanderBootcamp.DesafioControleFluxo;

import Plataformas.SantanderBootcamp.DesafioControleFluxo.exceptions.ParametroInvalidosException;

import java.util.Scanner;

public class Contador {
    public static void main(String[] args) {

        try (Scanner entrada = new Scanner(System.in)) {
            System.out.println("Digite o primeiro parâmetro");
            int n1 = entrada.nextInt();
            entrada.nextLine();
            System.out.println("Digite o segundo parâmetro");
            int n2 = entrada.nextInt();
            entrada.nextLine();
            try{
                int n3 = getN3(n1, n2);
                for (int n = 0; n < n3; n += 1 ) {
                    System.out.printf("Imprimindo o número %d\n", n + 1);
                }
            }catch (ParametroInvalidosException error) {
                System.out.println(error.getMessage());
            }


        }
    }

    private static int  getN3(int n1, int n2) {
        if(n1 > n2) throw new ParametroInvalidosException("O segundo numero deve ser maior que o primeiro");
        int n3 = n2 - n1;
        return n3;
    }
}


