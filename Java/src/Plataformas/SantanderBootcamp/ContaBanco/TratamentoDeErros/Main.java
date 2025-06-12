package Plataformas.SantanderBootcamp.ContaBanco.TratamentoDeErros;

import Plataformas.SantanderBootcamp.ContaBanco.TratamentoDeErros.dao.UserDao;
import Plataformas.SantanderBootcamp.ContaBanco.TratamentoDeErros.model.MenuOption;
import Plataformas.SantanderBootcamp.ContaBanco.TratamentoDeErros.model.UserModel;

import java.time.OffsetDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeFormatterBuilder;
import java.util.Scanner;

public class Main {

    private final static Scanner entrada = new Scanner(System.in);

    private final static UserDao dao = new UserDao();

    public static void main(String[] args) {

        while (true) {
            System.out.println("Bem vindo ao seu crud de banco");
            System.out.println("1 - Cadastrar");
            System.out.println("2 - Atualizar");
            System.out.println("3 - Excluir");
            System.out.println("4 - Buscar por id");
            System.out.println("5 - Listar");
            System.out.println("6 - Sair");

            int userInputOption = entrada.nextInt();

            var selectionOption = MenuOption.values()[userInputOption - 1];
            switch (selectionOption) {
                case SAVE ->{
                    UserModel user = dao.save(requestToSave());
                    System.out.printf("Usuario Cadastrado %s", user);
                }
                case UPDATE -> {
                    UserModel user = dao.update(requestToUpdate());
                    System.out.printf("Usuario Atualizado %s", user);
                }
                case DELETE -> {
                    dao.delete(requestId());
                    System.out.println("Usuario Excluido");
                }
                case FIND_BY_ID -> {
                    UserModel user = dao.findById(requestId());
                    System.out.printf("Usuario Procurado %s", user);
                }
                case FIND_ALL -> {
                    var users = dao.findAll(); //lista
                    System.out.println("Usuarios Cadastrados\n");
                    users.forEach(System.out::println);
                }

                case EXIT ->  System.exit(0);

            }

        }
    }


    private static UserModel requestToSave() {
        System.out.println("Informe o nome do Usuario:");
        String name = entrada.next();
        System.out.println("Informe o email do Usuario:");
        String email = entrada.next();
        System.out.println("Informe o data de nascimento do Usuario: (dd/MM/yyyy)");
        String birthday = entrada.next();

        UserModel user = new UserModel(0, name, email, birthday);

        return user;

    }

    private static UserModel requestToUpdate() {

        System.out.println("Informe o Id do Usuario:");
        long id = entrada.nextLong();
        entrada.nextLine();

        System.out.println("Informe o nome do Usuario:");
        String name = entrada.next();
        System.out.println("Informe o email do Usuario:");
        String email = entrada.next();
        System.out.println("Informe o data de nascimento do Usuario: (dd/MM/yyyy)");
        String birthday = entrada.next();


        UserModel user = new UserModel(id, name, email, birthday);

        return user;
    }

    private static long requestId() {
        System.out.println("Informe o Id do Usuario:");
        return entrada.nextLong();
    }
}

