package fundamentos;

public class Switch {
    public static void main(String[] args) {
        String aprovacao = "";
        int nota = 7;

        switch(nota) {
            case 2: case 3:
                aprovacao ="Reprovado";
                break;
            case 6: case 7:
                aprovacao ="na media";
                break;
            case 10: case 9:
                aprovacao ="execelente";
                break;
            }
    }
}
