package fundamentos.array;

import java.util.Arrays;
import java.util.Scanner;

public class Matriz {
    public static void main(String[] args) {
        try(Scanner entrada = new Scanner(System.in)) {
           int qntdAlunos = entrada.nextInt();
           entrada.nextLine();
           int qntdNotas = entrada.nextInt();
           entrada.nextLine();
           double[][] NotasAlunos = new double[qntdAlunos][qntdNotas];
           double total = 0;
           for (int a = 0; a < qntdAlunos; a++) {
                for (int n = 0; n < qntdNotas; n++) {
                    System.out.printf("Informe a nota %d do aluno %d:", n+1, a+1);
                    NotasAlunos[a][n] = entrada.nextDouble();
                    entrada.nextLine();
                    total =+ NotasAlunos[a][n];
                    System.out.println(Arrays.toString(NotasAlunos[a]));
                }}

           System.out.println("o total das notas é " + total);
        }
    }
}