package fundamentos.colecoes;

import java.util.*;

public class Exercicios {

    public static void main(String[] args) {
        try (Scanner entrada = new Scanner(System.in)) {
            List<String> nomes = new ArrayList<String>();
            System.out.println("Digite 5 nomes:");
            nomes.add(entrada.nextLine());
            nomes.add(entrada.nextLine());
            nomes.add(entrada.nextLine());
            nomes.add(entrada.nextLine());
            nomes.add(entrada.nextLine());

            for(String nome: nomes) {
                System.out.println(nome);
            }

            List<String> names = new ArrayList<String>();
            System.out.println("Digite 6 nomes:");
            for (int a = 0; a <= 5; a++) {
                names.add(entrada.nextLine());
            }

            Set<String> namesDuplicados = new HashSet<String>();
            for (String nome:nomes) {
                namesDuplicados.add(nome);
            }

            System.out.println(namesDuplicados.toString());

        }

    }

    }





