package Plataformas.SantanderBootcamp.desafios;
import java.util.Scanner;

public class DesafioUm {

        public static void main(String[] args) {

            Scanner scanner = new Scanner(System.in);
            String nome = scanner.nextLine();
            int id = scanner.nextInt();
            String identificador = formatar(nome, id);
            System.out.println(identificador);


            scanner.close();
        }

        public static String formatar(String nome, int id) {
            String idString = Integer.toString(id);
            nome = nome.toLowerCase();
            String identificador = nome + "-" +idString;
            return  identificador;
        }
    }

