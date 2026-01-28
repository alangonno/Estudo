package infra;

import net.bytebuddy.implementation.bytecode.Throw;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import javax.persistence.TypedQuery;
import java.lang.reflect.Type;
import java.util.List;

public class DAO<E> {

    private static EntityManagerFactory emf;
    private EntityManager em;
    private Class<E> clas;

    static {
        emf = Persistence.createEntityManagerFactory("jpa");
    }

    public DAO() {
        this(null);
    }

    public DAO(Class<E> clas) {
        this.clas = clas;
        this.em = emf.createEntityManager();
    }

    public DAO<E> openTransaction() {
        em.getTransaction().begin();
        return this;
    }

    public DAO<E> closeTransaction() {
        em.getTransaction().commit();
        return this;
    }

    public DAO<E> persistence(E entity) {
        em.persist(entity);
        return this;
    }

    public List<E> getAll(int quant, int offset) {
        if(clas == null) {
            throw new UnsupportedOperationException("Class NULL");
        }

        String  jpql = "select e from " + clas.getName() + " e";
        TypedQuery<E> query = em.createQuery(jpql, clas);
        query.setMaxResults(quant);
        query.setFirstResult(offset);
        return query.getResultList();

    }

    public void fechar(){
        em.close();
        emf.close();
    }

    public List<E> consultar(String nomeConsulta, Object... params) {
        TypedQuery<E> query = em.createNamedQuery(nomeConsulta, clas);

        for (int i = 0; i < params.length; i += 2) {
            query.setParameter(params[i].toString(), params[i + 1]);
        }

        return query.getResultList();
    }

    public E consultarUm(String nomeConsulta, Object... params) {
        List<E> lista = consultar(nomeConsulta, params);
        return lista.isEmpty() ? null : lista.get(0);
    }


    }
