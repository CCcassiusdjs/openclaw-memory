# Analisador Léxico - JFlex

Um analisador léxico para uma linguagem de programação simples, implementado com JFlex.

## 🎯 Reconhece

| Tipo | Padrão | Exemplos |
|------|--------|----------|
| **Palavras-chave** | `int`, `float`, `string`, `bool`, `if`, `else`, `while`, `for`, `func`, etc. | `int x = 10;` |
| **Identificadores** | `[a-zA-Z_][a-zA-Z0-9_]*` | `contador`, `_temp`, `var1` |
| **Números inteiros** | `[0-9]+` | `42`, `100`, `0` |
| **Números decimais** | `[0-9]+\.[0-9]+` | `3.14159`, `2.5` |
| **Notação científica** | `[0-9]+(\.[0-9]+)?[eE][+-]?[0-9]+` | `1.23e10`, `4.56e-5` |
| **Strings** | `"..."` ou `'...'` | `"Olá, Mundo!"`, `'teste'` |
| **Operadores aritméticos** | `+`, `-`, `*`, `/`, `%`, `\`, `^` | `x + y` |
| **Operadores relacionais** | `==`, `!=`, `<`, `>`, `<=`, `>=` | `x == y` |
| **Operadores lógicos** | `&&`, `||` | `a && b` |
| **Operadores de atribuição** | `=`, `+=`, `-=`, `*=`, `/=` | `x = 10`, `x += 1` |
| **Operadores de incremento** | `++`, `--` | `x++`, `y--` |
| **Delimitadores** | `;`, `:`, `,`, `.`, `(`, `)`, `{`, `}`, `[`, `]` | `(x + y)` |
| **Comentários de linha** | `// ...` | `// comentário` |
| **Comentários de bloco** | `/* ... */` | `/* multilinha */` |

## 📦 Estrutura

```
lexico-analyzer/
├── src/
│   ├── Lexer.flex      # Definição do analisador léxico
│   └── Main.java       # Programa principal
├── test/
│   └── teste_codigo.lang  # Arquivo de teste
├── build/              # Arquivos compilados (gerado)
├── build.sh            # Script de compilação
├── Makefile            # Makefile alternativo
└── README.md           # Este arquivo
```

## 🚀 Compilar e Executar

### Usando o script

```bash
./build.sh              # Compila e executa teste
./build.sh              # Executa com código de exemplo
```

### Usando Makefile

```bash
make                    # Compilar
make test               # Executar teste
make run FILE=test/teste_codigo.lang  # Analisar arquivo
make clean              # Limpar arquivos gerados
```

### Manual

```bash
# 1. Gerar Java a partir do Flex
jflex -d build src/Lexer.flex

# 2. Compilar Java
javac -d build build/Lexer.java src/Main.java

# 3. Executar
cd build && java Main --test
```

## 📊 Saída

```
[KEYWORD     ] L2:C1 = "int"
[IDENT       ] L2:C5 = "contador"
[OP_ASSIGN   ] L2:C14 = "="
[INT         ] L2:C16 = "0"
[SEMICOLON   ] L2:C17 = ";"

=== ESTATISTICAS DO LEXER ===
Tokens reconhecidos: 91
Erros lexicos: 0
Linhas processadas: 21
```

## 📝 Exemplo de Código

```javascript
// Variáveis globais
int contador = 0;
float pi = 3.14159;
string mensagem = "Olá, Mundo!";
bool ativo = true;

// Função principal
func main() {
    int x = 10;
    float y = 20.5;
    
    if (x < y) {
        contador++;
        return x + y;
    } else {
        contador--;
        return 0;
    }
    
    while (contador < 100) {
        contador += 1;
    }
    
    int[] nums = [1, 2, 3, 4, 5];
}
```

## 🔧 Estender o Analisador

Para adicionar novos tokens:

1. **Adicionar macro na seção de declarações:**
   ```
   NOVA_MACRO = [a-z]+
   ```

2. **Adicionar regra na seção de regras:**
   ```
   {NOVA_MACRO} { printToken("NOVO_TIPO", yytext()); }
   ```

3. **Recompilar:**
   ```bash
   ./build.sh
   ```

## 📚 Dependências

- **JFlex 1.7.0+** - Gerador de analisador léxico
- **Java 21+** - Runtime
- **OpenJDK** - Compilador Java

## 📖 Referências

- [JFlex Manual](https://jflex.de/manual.html)
- [JFlex User's Guide](/usr/share/doc/jflex/doc/manual.pdf)
- [Java Cup](https://version2.hofstra.edu/assets/0/3/0/4/8/7/30487.pdf) - Parser Generator

## 🎯 Próximos Passos

- [ ] Integrar com Java CUP para parser sintático
- [ ] Adicionar tabela de símbolos
- [ ] Implementar análise semântica
- [ ] Gerar AST (Árvore Sintática Abstrata)