package Plataformas.SantanderBootcamp.desafios;

import java.util.Arrays;
import java.util.Scanner;

    public class DesafioQuatro {
        public static void main(String[] args) {

            Scanner scanner = new Scanner(System.in);

            String request = scanner.nextLine();

            scanner.close();
    }

    public static boolean validarIP(String ip) {

        String[] numeros = ip.split("\\.");
        boolean tudoCorreto = numeros.length >= 4;

        for (String numero : numeros) {
            if (!ehNumeroValido(numero)) {
                tudoCorreto = false;
                break;
            }
        }

        return tudoCorreto;
    }


    private static boolean ehNumeroValido(String str) {
        try {
            int num = Integer.parseInt(str);
            return num >= 0 && num <= 255;
        } catch (NumberFormatException e) {
            return false;
        }
        }
    }


