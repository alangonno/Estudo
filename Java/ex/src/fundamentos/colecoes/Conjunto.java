package fundamentos.colecoes;

import java.util.SortedSet;
import java.util.TreeSet;

public class Conjunto {
    public static void main(String[] args) {
        SortedSet<String> lista = new TreeSet<String>();
        //Set<String> lista = new HashSet<String>();
        lista.add("ana");
        lista.add("joao");
        lista.add("alan");
        lista.add("luan");
        System.out.println(lista);

        for (String candidato : lista) {
            System.out.println(candidato);
        }
    }
}
