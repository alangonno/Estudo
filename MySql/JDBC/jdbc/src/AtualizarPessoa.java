import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Scanner;

public class AtualizarPessoa {
    public static void main(String[] args) throws SQLException{
        try(Scanner entrada = new Scanner(System.in)) {
            System.out.println("Id do nome:");
            int id = entrada.nextInt();
            entrada.nextLine();
            System.out.println("Novo Nome:");
            String nome = entrada.nextLine();

            String sql = "UPDATE pessoas set nome = ? where codigo = ?";

            Connection conexao = FabricaConexao.getConexao();

            PreparedStatement stmt = conexao.prepareStatement(sql);
            stmt.setString(1, nome);
            stmt.setInt(2, id);
            stmt.execute();
            
            stmt.close();
            conexao.close();
    
        }
            
    }
    
}
