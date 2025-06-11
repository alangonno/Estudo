package fundamentos.classe;

public class areaC {

    double raio;
    static final double pi = 3.14;

    areaC(double raioI) {
        raio = raioI;
    }

    double area() {
        return  pi * raio * raio ;
    }

    static double area(double area) {
        return pi * Math.pow(pi, area);
    }
}
