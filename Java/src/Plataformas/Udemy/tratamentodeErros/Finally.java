package Plataformas.Udemy.tratamentodeErros;

import java.util.Scanner;

public class Finally {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);

        try {
            System.out.println(7 / entrada.nextInt());

        } catch (Exception e){
            System.out.println(e.getMessage());

        } finally {
            entrada.close();
        }

    }

}
