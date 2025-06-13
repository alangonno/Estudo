package Plataformas.SantanderBootcamp.TratamentoDeErros;

import Plataformas.SantanderBootcamp.TratamentoDeErros.dao.UserDao;
import Plataformas.SantanderBootcamp.TratamentoDeErros.exceptions.EmptyStorageException;
import Plataformas.SantanderBootcamp.TratamentoDeErros.exceptions.UserNotFoundException;
import Plataformas.SantanderBootcamp.TratamentoDeErros.exceptions.ValidatorException;
import Plataformas.SantanderBootcamp.TratamentoDeErros.model.MenuOption;
import Plataformas.SantanderBootcamp.TratamentoDeErros.model.UserModel;
import Plataformas.SantanderBootcamp.TratamentoDeErros.validator.UserValidator;

import java.util.Scanner;

public class Main {

    private final static Scanner entrada = new Scanner(System.in);

    private final static UserDao dao = new UserDao();

    public static void main(String[] args) {

        while (true) {
            System.out.println("===================\nBem vindo ao seu crud de banco");
            System.out.println("1 - Cadastrar");
            System.out.println("2 - Atualizar");
            System.out.println("3 - Excluir");
            System.out.println("4 - Buscar por id");
            System.out.println("5 - Listar");
            System.out.println("6 - Sair\n==================");

            int userInputOption = entrada.nextInt();

            var selectionOption = MenuOption.values()[userInputOption - 1];
            switch (selectionOption) {

                case SAVE ->{
                    try {
                        UserModel user = dao.save(requestToSave());
                        System.out.printf("Usuario Cadastrado %s", user);
                    }catch (ValidatorException error) {
                        System.out.println(error.getMessage());
                    }
                }

                case UPDATE -> {
                    try {
                        UserModel user = dao.update(requestToUpdate());
                    }catch (UserNotFoundException | EmptyStorageException | ValidatorException error) {
                        System.out.println(error.getMessage());
                    } finally {
                        System.out.println("===================");
                    }
                }

                case DELETE -> {
                    try{
                        dao.delete(requestId());
                        System.out.println("Usuario excluido");
                    }catch (UserNotFoundException | EmptyStorageException error) {
                        System.out.println(error.getMessage());
                    } finally {
                        System.out.println("===================");
                    }
                }

                case FIND_BY_ID -> {
                    try {
                        UserModel user = dao.findById(requestId());
                        System.out.printf("Usuario Procurado %s", user);
                    } catch (UserNotFoundException | EmptyStorageException error) {
                        System.out.println(error.getMessage());
                    } finally {
                        System.out.println("===================");
                    }
                }

                case FIND_ALL -> {
                    var users = dao.findAll(); //lista
                    if (!users.isEmpty()) {
                    System.out.println("Usuarios Cadastrados\n");
                    users.forEach(System.out::println);
                    }
                }

                case EXIT ->  System.exit(0);

            }

        }
    }


    private static UserModel requestToSave()  throws ValidatorException {
        System.out.println("Informe o nome do Usuario:");
        String name = entrada.next();
        System.out.println("Informe o email do Usuario:");
        String email = entrada.next();
        System.out.println("Informe o data de nascimento do Usuario: (dd/MM/yyyy)");
        String birthday = entrada.next();

        return validateInput(0, name, email, birthday);

    }

    private static UserModel requestToUpdate() throws ValidatorException {

        System.out.println("Informe o Id do Usuario:");
        long id = entrada.nextLong();
        entrada.nextLine();

        System.out.println("Informe o nome do Usuario:");
        String name = entrada.next();
        System.out.println("Informe o email do Usuario:");
        String email = entrada.next();
        System.out.println("Informe o data de nascimento do Usuario: (dd/MM/yyyy)");
        String birthday = entrada.next();

        return validateInput(id, name, email, birthday);
    }

    private static long requestId() {
        System.out.println("Informe o Id do Usuario:");
        return entrada.nextLong();
    }

    private static UserModel validateInput ( final long id, final String name, final String email, final String birthday) throws ValidatorException {
        UserModel user = new UserModel(id, name, email, birthday);
        UserValidator.verifyModel(user);
        return user;
    }
}

