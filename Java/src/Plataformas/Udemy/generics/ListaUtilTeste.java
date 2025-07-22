package Plataformas.Udemy.generics;

import java.util.Arrays;
import java.util.List;

public class ListaUtilTeste {

    public static void main(String[] args) {
        List<String> langs = Arrays.asList("JS", "PHP", "Java", "C++");
        List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5, 6);

        String ultimaLang = (String)  ListaUtil.getUltimo1(langs);
        System.out.println(ultimaLang);

        Integer ultimoNums = (Integer) ListaUtil.getUltimo1(nums);
        System.out.println(ultimoNums);

        String ultimaLang2 =  ListaUtil.getUltimo2(langs);
        System.out.println(ultimaLang2);

        Integer ultimoNums2 =  ListaUtil.getUltimo2(nums);
        System.out.println(ultimoNums2);
    }
}
