package fundamentos;

import java.util.Scanner;

public class Calculadora {
    public static void main(String[] args) {
       try(Scanner entrada = new Scanner(System.in)) {
        System.out.println("n1:");
        double n1 = entrada.nextDouble();
        entrada.nextLine();
        System.out.println("n2:");
        double n2 = entrada.nextDouble();
        entrada.nextLine();
        System.out.println("+ / * - %\nR:");
        String op = entrada.nextLine();
        double resposta = "+".equals(op) ? n1+n2 : 0;
        resposta = "-".equals(op) ? n1-n2 : resposta;
        resposta = "*".equals(op) ? n1*n2 : resposta;
        resposta = "/".equals(op) ? n1/n2 : resposta;
        resposta = "%".equals(op) ? n1%n2 : resposta;
        System.out.println(resposta);


       }
    }
}
        //ler1
        //ler2
        // + - * / %

        /*System.out.println("n1:");
        double n1 = entrada.nextDouble();
        entrada.nextLine();
        System.out.println("n2:");
        double n2 = entrada.nextDouble();
        entrada.nextLine();
        System.out.println("+ / * - %\n R:");
        String rUsu = entrada.nextLine();
        boolean somaV = rUsu.equals("+");
        boolean subV = rUsu.equals("-");
        boolean diviV = rUsu.equals("/");
        boolean multiV = rUsu.equals("*");  
        boolean restaV = rUsu.equals("%");
        Double soma = n1 + n2;
        Double sub = n1 - n2;
        Double div = n1 / n2;
        Double multi = n1 * n2;
        Double resta = n1 % n2;
        String res = true == somaV ? soma.toString() : 
        true == subV ? sub.toString(): 
        true == diviV ? div.toString() : 
        true == multiV ? multi.toString() : 
        true == restaV ? resta.toString(): "Valor incorreto";
        System.out.println(res);*/