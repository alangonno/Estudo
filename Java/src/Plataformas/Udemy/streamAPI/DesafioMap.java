package streamAPI;

import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.function.UnaryOperator;

public class DesafioMap {

    static String inverter (String s) {
        String c = new StringBuilder(s).reverse().toString();
        return c;
    }

    public static void main(String[] args) {

        List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9);

        Function<String, Integer> BinarioDois = i -> Integer.parseInt(i, 2);


        nums.stream().map(Integer::toBinaryString).
                map(DesafioMap::inverter).
                map(BinarioDois).forEach(System.out::println);
    }
}
