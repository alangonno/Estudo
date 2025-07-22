package fundamentos.array;

import java.util.Scanner;

public class DesArray {
    public static void main(String[] args) {
        try(Scanner entrada = new Scanner(System.in)) {

        System.out.println("Digite a quantidade de notas: ");
        double[] notas = new double[entrada.nextInt()];
        entrada.nextLine();    
        for(int i = 0;i < notas.length; i++) {
            System.out.printf("Digite a nota %d: ", i+1);
            notas[i] = entrada.nextDouble();
            entrada.nextLine();
            
        }
        double soma = 0;

        for(double nota: notas) {
            soma += nota;
        }

        System.out.println("A media é igual a :" + soma / notas.length + "\n e a soma: " + soma);
    }
    }
}
