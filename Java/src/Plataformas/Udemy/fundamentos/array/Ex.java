package fundamentos.array;
 import java.util.Arrays;
public class Ex { 
    public static void main(String[] args) {

        double[] notas = new double[4];
        notas[0] = 6;
        notas[1] = 7.5;
        notas[2] = 1.2;
        notas[3] = 10;
        
        System.out.println(Arrays.toString(notas));

        double totalA = 0;
        for(int i = 0; i < notas.length; i++){
            totalA += notas[i];
        }
        System.out.println(totalA);

        double totalB = 0;

        double[] notasB = { 6.9, 2.3, 5.6, 1.2};
        for(int i = 0; i < notasB.length; i++) {
            totalB += notasB[i];
        }
        System.out.println(totalB);
    }
}