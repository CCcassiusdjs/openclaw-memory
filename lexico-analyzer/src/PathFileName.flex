%%
/* ============================================================================
 * EXERCÍCIO 1 - PathFileName JFlex
 * 
 * Objetivo: Reconhecer nomes de arquivos com caminho (formato Windows)
 * 
 * Gramática:
 *   PathFileName --> (Drive:\)?(\)?(PathName\)*FileName(.FileType)?
 *   Drive        --> letter
 *   PathName     --> id
 *   FileName     --> id
 *   FileType     --> id
 *   Id           --> (letter | digit)(letter | digit)*
 * 
 * Exemplos válidos:
 *   D:\acad\disc\compil\compil_u02_lexico
 *   ExercicioLexico.doc
 *   \Windows\System32
 *   C:\Users\test\file.txt
 * ============================================================================ */

%class PathFileName
%unicode
%int
%line
%column
%standalone

%{
    /* Contadores de estatísticas */
    private int validCount = 0;
    private int invalidCount = 0;
    
    public void printStats() {
        System.out.println("");
        System.out.println("=== ESTATISTICAS ===");
        System.out.println("Paths validos: " + validCount);
        System.out.println("Paths invalidos: " + invalidCount);
    }
%}

/* ============================================================================
 * DEFINIÇÕES REGULARES (Macros)
 * 
 * Cada macro define um padrão que pode ser usado nas regras léxicas.
 * As macros são expandidas textualmente pelo JFlex antes da compilação.
 * ============================================================================ */

/* ----------------------------------------------------------------------------
 * PADRÃO: Dígitos
 * Reconhece: 0-9
 * Exemplo: "0", "5", "9"
 * ---------------------------------------------------------------------------- */
DIGIT = [0-9]

/* ----------------------------------------------------------------------------
 * PADRÃO: Letras
 * Reconhece: a-z, A-Z (case insensitive)
 * Exemplo: "a", "Z", "M"
 * ---------------------------------------------------------------------------- */
LETTER = [a-zA-Z]

/* ----------------------------------------------------------------------------
 * PADRÃO: Underscore
 * Reconhece: caractere underscore (_)
 * Usado em identificadores como "minha_variavel"
 * ---------------------------------------------------------------------------- */
UNDERSCORE = "_"

/* ----------------------------------------------------------------------------
 * PADRÃO: Caracteres válidos em identificadores
 * Combina: letra | dígito | underscore
 * Este padrão reconhece QUALQUER caractere válido em um ID
 * ---------------------------------------------------------------------------- */
ID_CHAR = {LETTER}|{DIGIT}|{UNDERSCORE}

/* ----------------------------------------------------------------------------
 * PADRÃO: Identificador completo
 * Estrutura: primeiro caractere (letra|dígito) + resto (zero ou mais ID_CHAR)
 * 
 * Regex expandido: (letra|dígito|underscore) ((letra|dígito|underscore))*
 * 
 * Exemplos válidos:
 *   "abc"        → letra + letras
 *   "var1"       → letra + letra + dígito
 *   "_private"   → underscore + letras
 *   "Test_123"   → letra + mix de chars
 * 
 * Exemplos inválidos:
 *   "123abc"     → começa com dígito (mas a gramática aceita!)
 *   ""           → vazio (não aceito)
 * ---------------------------------------------------------------------------- */
ID = {ID_CHAR}+

/* ----------------------------------------------------------------------------
 * PADRÃO: Drive do Windows
 * Estrutura: letra seguida de dois pontos
 * 
 * Regex expandido: [a-zA-Z] ":"
 * 
 * Exemplos válidos: "C:", "D:", "E:"
 * Exemplos inválidos: "1:", "::", "AB:"
 * ---------------------------------------------------------------------------- */
DRIVE = {LETTER} ":"

/* ----------------------------------------------------------------------------
 * PADRÃO: PathName e FileName
 * Ambos são identificadores (ID)
 * 
 * PathName  → nome de diretório (ex: "Windows", "Program Files")
 * FileName  → nome do arquivo sem extensão (ex: "documento")
 * FileType  → extensão do arquivo (ex: "txt", "pdf")
 * ---------------------------------------------------------------------------- */
PATHNAME = {ID}
FILENAME = {ID}
FILETYPE = {ID}

/* ----------------------------------------------------------------------------
 * PADRÃO: Separador de caminho Windows
 * Caractere barra invertida: \
 * 
 * NOTA: Em strings Java/JFlex, \\ representa um único \
 *       No regex, \\ também precisa ser escapado, resultando em \\\\
 * ---------------------------------------------------------------------------- */
PATH_SEPARATOR = "\\"

/* ----------------------------------------------------------------------------
 * PADRÃO: Caminho (sequência de PathNames com separadores)
 * Estrutura: \PathName\PathName\...
 * 
 * Regex: {PATH_SEPARATOR}{PATHNAME}{PATH_SEPARATOR}*
 * 
 * Exemplos: "\Windows", "\Program Files", "\Users\admin"
 * 
 * NOTA: O * após PATH_SEPARATOR permite trailing slash
 *       Ex: "\Windows\" é válido
 * ---------------------------------------------------------------------------- */
PATH = {PATH_SEPARATOR}{PATHNAME}{PATH_SEPARATOR}*

/* ----------------------------------------------------------------------------
 * PADRÃO: Caminho opcional (zero ou mais segmentos)
 * Estrutura: (PATH)*
 * 
 * Permite caminhos sem PathName (ex: "\arquivo.txt")
 * ---------------------------------------------------------------------------- */
OPTIONAL_PATH = ({PATH})*

/* ----------------------------------------------------------------------------
 * PADRÃO: Drive opcional com separador
 * Estrutura: (Drive\)?  (opcional)
 * 
 * Exemplos: "C:\", "D:\", ou vazio (sem drive)
 * ---------------------------------------------------------------------------- */
OPTIONAL_DRIVE = ({DRIVE}{PATH_SEPARATOR})?

/* ----------------------------------------------------------------------------
 * PADRÃO: Extensão de arquivo opcional
 * Estrutura: (.FileType)?  (opcional)
 * 
 * Exemplos: ".txt", ".pdf", ".doc", ou vazio
 * ---------------------------------------------------------------------------- */
OPTIONAL_FILETYPE = ("."{FILETYPE})?

/* ============================================================================
 * PADRÃO COMPLETO: PathFileName
 * 
 * Estrutura completa (gramática do exercício):
 *   PathFileName --> (Drive:\)?(\)?(PathName\)*FileName(.FileType)?
 * 
 * Regex construído:
 *   OPTIONAL_DRIVE + PATH_SEPARATOR? + OPTIONAL_PATH + FILENAME + OPTIONAL_FILETYPE
 * 
 * Decomposição:
 *   1. (Drive:\)?          → OPTIONAL_DRIVE
 *   2. (\)?                → PATH_SEPARATOR? (barra após drive opcional)
 *   3. (PathName\)*        → OPTIONAL_PATH (caminho com separadores)
 *   4. FileName            → FILENAME
 *   5. (.FileType)?        → OPTIONAL_FILETYPE
 * 
 * Exemplos completos válidos:
 *   "D:\acad\disc\compil\compil_u02_lexico"
 *      ↓      ↓     ↓      ↓
 *   Drive:\  Path  Path   FileName
 *   
 *   "ExercicioLexico.doc"
 *      ↓          ↓
 *   FileName   .FileType
 *   
 *   "\Windows\System32"
 *      ↓       ↓
 *   \Path   PathName
 *   
 *   "C:file.txt"
 *      ↓  ↓    ↓
 *   Drive FileName .FileType
 * ============================================================================ */
PATH_FILENAME = {OPTIONAL_DRIVE}{PATH_SEPARATOR}?{OPTIONAL_PATH}{FILENAME}{OPTIONAL_FILETYPE}

/* ----------------------------------------------------------------------------
 * PADRÃO: Qualquer outro caractere (fallback)
 * Usado para capturar caracteres não reconhecidos pelos padrões anteriores
 * ---------------------------------------------------------------------------- */
ANY = .

%%

/* ============================================================================
 * REGRAS LÉXICAS
 * 
 * Cada regra tem a forma:
 *   PADRÃO { ação }
 * 
 * Quando o scanner encontra texto que corresponde ao PADRÃO,
 * a AÇÃO é executada.
 * ============================================================================ */

/* ----------------------------------------------------------------------------
 * REGRA: Reconhecer PathFileName válido
 * 
 * Quando o padrão PATH_FILENAME é encontrado:
 * 1. Incrementa contador de paths válidos
 * 2. Imprime localização (linha:coluna) e texto reconhecido
 * ---------------------------------------------------------------------------- */
{PATH_FILENAME} {
    validCount++;
    System.out.printf("[VALIDO] L%d:C%d = \"%s\"%n", yyline + 1, yycolumn + 1, yytext());
}

/* ----------------------------------------------------------------------------
 * REGRA: Fallback para caracteres não reconhecidos
 * 
 * Captura qualquer caractere que não foi reconhecido pelos padrões anteriores.
 * Neste exercício, apenas ignoramos esses caracteres.
 * 
 * Alternativamente, poderíamos contar como inválidos:
 *   {ANY} { invalidCount++; }
 * ---------------------------------------------------------------------------- */
{ANY} {
    /* Ignorar ou contar como inválido se for parte de um path mal formado */
}

/* ----------------------------------------------------------------------------
 * REGRA: Fim de arquivo
 * 
 * Quando o scanner atinge o final do input:
 * 1. Imprime estatísticas
 * 2. Retorna YYEOF (fim de arquivo)
 * ---------------------------------------------------------------------------- */
<<EOF>> {
    printStats();
    return YYEOF;
}