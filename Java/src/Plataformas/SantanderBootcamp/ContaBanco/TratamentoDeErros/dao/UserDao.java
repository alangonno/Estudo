package Plataformas.SantanderBootcamp.ContaBanco.TratamentoDeErros.dao;

import Plataformas.SantanderBootcamp.ContaBanco.TratamentoDeErros.exceptions.UserNotFoundException;
import Plataformas.SantanderBootcamp.ContaBanco.TratamentoDeErros.model.UserModel;

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
        String message = String.format("Não existe usuario com o Id %s cadastrado", id);
        return models.stream()
                .filter(u ->u.getId() == id)
                .findFirst()
                .orElseThrow(() -> new UserNotFoundException(message));

    }

    public List<UserModel> findAll() {
        return models;
    }

}
