package fundamentos;

import java.util.Scanner;

public class controle {
    public static void main(String[] args) {
        double media = 0;
        int notas = 0;
        double total = 0;
        double res = 0;
        try(Scanner entrada = new Scanner(System.in)) {
            while(res != -1) {
                System.out.println("Nota:");
                res = entrada.nextDouble();
                if(0 <= res && res <= 10){
                    notas++;
                    total += res;
                    }
                else {
                    System.out.println("Nota Invalida!");
                }
            }
            media = total / notas;
            System.out.printf("Quantidade de notas: %d, Media: %.2f, Total: %.2f", notas, media, total);
        }

       }
}

