package Plataformas.SantanderBootcamp.TratamentoDeErros.validator;

import Plataformas.SantanderBootcamp.TratamentoDeErros.exceptions.ValidatorException;
import Plataformas.SantanderBootcamp.TratamentoDeErros.model.UserModel;

public class UserValidator {

    private UserValidator(){

    }

    public static void verifyModel(final UserModel model) throws ValidatorException{
        if(StringIsBlank(model.getName()))
            throw new ValidatorException("Informe um nome correto");
        if (model.getName().length() < 2)
            throw new ValidatorException("Nome muito curto");
        if (StringIsBlank(model.getEmail())) throw new ValidatorException("Informe um Email");
        if(!model.getEmail().contains("@") || !model.getEmail().contains(".")) throw new ValidatorException(("Email Invalido"));
    }

    private static boolean StringIsBlank(final String string) {
        return string == null || string.isBlank();
    }
}
