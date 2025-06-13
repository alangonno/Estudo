package Plataformas.SantanderBootcamp.TratamentoDeErros.exceptions;

public class EmptyStorageException extends RuntimeException {

    public EmptyStorageException(String message) {
      super(message);
    }
}
