package fundamentos;

import java.util.Scanner;

public class ex1 {
    public static void main(String[] args) {
        try(Scanner entrada = new Scanner(System.in)) {
        System.out.println("Idade:");
        int idade = entrada.nextInt();
        entrada.nextLine();
        System.out.println("Nome:");
        String nome = entrada.nextLine();
        System.out.printf("Sobrenome :");
        String Sobrenome = entrada.nextLine();
        
        System.out.printf("Nome %s Sobrenome %s idade %d", nome, Sobrenome, idade);
        }

    }
}
