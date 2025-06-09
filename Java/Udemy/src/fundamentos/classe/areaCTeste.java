package fundamentos.classe;

public class areaCTeste {
    public static void main(String[] args) {
        areaC a1 = new areaC(10);
        System.out.println(a1.area());
        System.out.println(areaC.area(10));
    }
}
