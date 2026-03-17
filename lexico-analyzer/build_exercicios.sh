#!/bin/bash
# Compilar e testar os exercícios

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          EXERCICIO 1 - PathFileName JFlex                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Criar diretório de build
mkdir -p build

# Compilar PathFileName
echo "📦 Compilando PathFileName..."
jflex --quiet -d build src/PathFileName.flex

# Criar Main para PathFileName
cat > build/MainPath.java << 'EOF'
import java.io.*;

public class MainPath {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Uso: java MainPath <arquivo>");
            System.out.println("     java MainPath --test    (usa exemplos)");
            System.exit(1);
        }
        
        if (args[0].equals("--test")) {
            String testPaths = "D:\\acad\\disc\\compil\\compil_u02_lexico\n" +
                "ExercicioLexico.doc\n" +
                "\\Windows\\System32\n" +
                "C:\\Users\\test\\file.txt\n" +
                "arquivo_sem_path.txt\n" +
                "D:\\path\\com\\espaços\\file\n" +
                "/unix/path/file.txt\n" +
                "C:file.txt\n";
            
            System.out.println("=== ENTRADAS DE TESTE ===");
            System.out.println(testPaths);
            System.out.println("=== ANALISE ===\n");
            
            PathFileName lexer = new PathFileName(new StringReader(testPaths));
            while (lexer.yylex() != PathFileName.YYEOF) {
                // Continua lendo
            }
        } else {
            FileReader reader = new FileReader(args[0]);
            PathFileName lexer = new PathFileName(reader);
            while (lexer.yylex() != PathFileName.YYEOF) {
                // Continua lendo
            }
        }
    }
}
EOF

javac -d build build/PathFileName.java build/MainPath.java

echo ""
echo "=== TESTE PATHFILENAME ==="
cd build && java MainPath --test

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          EXERCICIO 2 - Modelo RTF JFlex                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"

# Compilar Modelo
echo "📦 Compilando Modelo..."
jflex --quiet -d build src/Modelo.flex

# Criar TestModelo
cat > build/TestModelo.java << 'EOF'
import java.io.*;

public class TestModelo {
    public static void main(String[] args) throws Exception {
        // Dados de teste
        Modelo lexer = new Modelo(new FileReader("../test/modelo.rtf"));
        lexer.setNome("Cassio Jones Dhein");
        lexer.setData("16 de marco de 2026");
        lexer.setValor(15000.00);
        lexer.setNumeroParcelas(24);
        lexer.setJurosMensal(1.5);
        
        System.out.println("=== CONTRATO GERADO ===");
        System.out.println("");
        
        while (lexer.yylex() != Modelo.YYEOF) {
            // Continua lendo
        }
    }
}
EOF

javac -d build build/Modelo.java build/TestModelo.java

echo ""
echo "=== TESTE MODELO (com dados padrao) ==="
cd build && java TestModelo

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    COMPILAÇÃO CONCLUÍDA                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo "Para executar interativamente:"
echo "  cd build && java MainModelo ../test/modelo.rtf"