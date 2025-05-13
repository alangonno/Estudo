package fundamentos.colecoes;

import java.util.HashSet;
import java.util.Set;

public class ConjuntoBaguncado {
    
    public static void main(String[] args) {
        
        HashSet conjunto = new HashSet();
        
        conjunto.add(1.2);// double -> Double
        conjunto.add(true); // boolean -> Boolean etc
        conjunto.add("teste");
        conjunto.add(5);
        conjunto.add('c');

        System.out.println("tamanho: " + conjunto.size());

        System.out.println(conjunto.remove("teste"));
        System.out.println(conjunto.remove("a"));

        System.out.println("tamanho: " + conjunto.size());

        System.out.println(conjunto.contains("teste"));

        Set nums = new HashSet();
        nums.add(1);
        nums.add(2);
        nums.add(3);
        nums.add(5);

        System.out.println(nums);
        System.out.println(conjunto);

        conjunto.retainAll(nums); //Interceção
        System.out.println(conjunto);
        conjunto.addAll(nums);//Uniao
        System.out.println(conjunto);
        conjunto.clear();
        System.out.println(conjunto);
    }
}
