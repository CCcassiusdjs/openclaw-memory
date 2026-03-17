import java.io.*;
import java.util.Scanner;

public class MainModelo {
    public static void main(String[] args) throws Exception {
        // Solicitar dados ao usuário
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("=== GERADOR DE CONTRATO ===");
        System.out.println("");
        
        System.out.print("Nome completo: ");
        String nome = scanner.nextLine();
        
        System.out.print("Data (ex: 16 de marco de 2026): ");
        String data = scanner.nextLine();
        
        System.out.print("Valor do emprestimo (R$): ");
        double valor = Double.parseDouble(scanner.nextLine().replace(",", "."));
        
        System.out.print("Numero de parcelas: ");
        int parcelas = Integer.parseInt(scanner.nextLine());
        
        System.out.print("Juros mensal (%): ");
        double juros = Double.parseDouble(scanner.nextLine().replace(",", "."));
        
        scanner.close();
        
        // Criar lexer com dados
        Modelo lexer = new Modelo(new FileReader(args.length > 0 ? args[0] : "test/modelo.rtf"));
        lexer.setNome(nome);
        lexer.setData(data);
        lexer.setValor(valor);
        lexer.setNumeroParcelas(parcelas);
        lexer.setJurosMensal(juros);
        
        System.out.println("");
        System.out.println("=== CONTRATO GERADO ===");
        System.out.println("");
        
        while (lexer.yylex() != Modelo.YYEOF) {
            // Continua lendo
        }
    }
}