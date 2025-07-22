package Plataformas.SantanderBootcamp.desafios;

import java.util.Scanner;

public class DesafioDois {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String url = scanner.nextLine();
        String urlCerta = url.toLowerCase().strip();
        System.out.println(urlCerta);
        scanner.close();

    }
}
