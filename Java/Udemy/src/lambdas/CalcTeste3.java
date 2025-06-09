package lambdas;

import java.util.function.BinaryOperator;

public class CalcTeste3 {

    public static void main(String[] args) {
        BinaryOperator<Double> calc = (x, y) -> { return x + y; };
        System.out.println(calc.apply(2.0, 3.0));
    }
}
