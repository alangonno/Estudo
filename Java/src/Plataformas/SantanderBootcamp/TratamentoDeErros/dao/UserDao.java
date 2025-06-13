package Plataformas.SantanderBootcamp.TratamentoDeErros.dao;

import Plataformas.SantanderBootcamp.TratamentoDeErros.exceptions.EmptyStorageException;
import Plataformas.SantanderBootcamp.TratamentoDeErros.exceptions.UserNotFoundException;
import Plataformas.SantanderBootcamp.TratamentoDeErros.model.UserModel;

import java.util.ArrayList;

import java.util.List;

public class UserDao {

    private long nextId = 1L;

    private final List<UserModel> models = new ArrayList<>();


    public UserModel save(final UserModel model){
        model.setId(nextId++);
        models.add(model);
        return model;

    }

    public UserModel update(final UserModel model){
        UserModel toUpdate = findById(model.getId());
        models.remove(toUpdate);
        models.add(model);
        return model;
    }

    public void delete(final long id){
        UserModel toDelete = findById(id);
        models.remove(toDelete);
    }

    public UserModel findById(final long id) {
        verifyStorage();
        String message = String.format("Não existe usuario com o Id %s cadastrado", id);
        return models.stream()
                .filter(u ->u.getId() == id)
                .findFirst()
                .orElseThrow(() -> new UserNotFoundException(message));

    }

    public List<UserModel> findAll() {

        try {
            verifyStorage();
        }catch (EmptyStorageException error) {
            System.out.println(error.getMessage());
        }
        return models;
    }

    private void verifyStorage() {
        if (models.isEmpty()) throw new EmptyStorageException("Armazenamento está vazio");
    }

}
