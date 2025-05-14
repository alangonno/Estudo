package fundamentos.colecoes;

import java.util.LinkedList;
import java.util.Queue;

public class Fila {

    public static void main(String[] args) {
        Queue<String> fila = new LinkedList<>();

        fila.add("ana");
        fila.offer("Bia");
        fila.offer("Jonas");
        fila.offer("Marcos");
        fila.offer("Joao");

        System.out.println(fila.peek());
    }
}
