package streamAPI;

public class MediaTeste {

    public static void main(String[] args) {

        Media m1 = new Media().adicionar(8.3).adicionar(2.3);
        Media m2 = new Media().adicionar(10).adicionar(6.3);


        System.out.println(m1.getMedia());
        System.out.println(m2.getMedia());

        System.out.println(Media.combinar(m1, m2).getMedia());


    }
}
