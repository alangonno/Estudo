package Plataformas.SantanderBootcamp.TratamentoDeErros.exceptions;

public class UserNotFoundException extends RuntimeException{

    public UserNotFoundException(String message) {
        super(message);
    }
}
