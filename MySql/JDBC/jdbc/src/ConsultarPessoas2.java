import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ConsultarPessoas2 {

    public static void main(String[] args) throws SQLException {
        try(Scanner entrada = new Scanner(System.in)) {
            System.out.println("Digite a procura");
            String nome = entrada.nextLine();
            String sql = "SELECT * FROM pessoas WHERE nome LIKE ?";
    
            Connection conexao = FabricaConexao.getConexao();
            PreparedStatement stmt = conexao.prepareStatement(sql);
            stmt.setString(1, "%" + nome + "%");
            ResultSet resultado = stmt.executeQuery();

            List<Pessoa> pessoas = new ArrayList();
            
            while(resultado.next()) {
                pessoas.add(new Pessoa(resultado.getInt("codigo"), resultado.getString("nome")));
            }

            for(Pessoa p: pessoas) {
                System.out.println(p.getNome());
            }
            stmt.close();
            conexao.close();
        }
    }
    }
