public class DAOTeste {
    public static void main(String[] args) {
        DAO dao = new DAO();

        String sql = "INSERT INTO pessoas (nome) VALUES (?)";
        dao.incluir(sql, "Joao");
        System.out.println(dao.incluir(sql, "Guilherme"));
        System.out.println(dao.incluir(sql, "James"));

        dao.close();
        
 }   
}
