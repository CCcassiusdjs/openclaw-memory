%%
/* ============================================================================
 * EXERCÍCIO 2 - Modelo RTF JFlex
 * 
 * Objetivo: Processar template RTF substituindo tags por valores dinâmicos
 * 
 * Tags reconhecidas:
 *   #data#     → data atual
 *   #nome#     → nome do cliente
 *   #valor#    → valor do empréstimo
 *   #numero#   → número de parcelas
 *   #juros#    → taxa de juros mensal
 *   #parcelas# → lista de parcelas calculadas
 * 
 * Funcionamento:
 *   1. Scanner lê arquivo RTF caractere por caractere
 *   2. Quando detecta uma tag, substitui pelo valor correspondente
 *   3. Caracteres normais são passados para saída inalterados
 * ============================================================================ */

%class Modelo
%unicode
%int
%standalone

%{
    /* ========================================================================
     * DADOS DO CONTRATO
     * 
     * Variáveis que serão substituídas nas tags do template RTF.
     * Podem ser alteradas via métodos setters antes de executar o scanner.
     * ======================================================================== */
    
    // Dados do cliente
    private String nome = "Cássio Jones Dhein";
    private String data = "16 de março de 2026";
    
    // Dados financeiros
    private double valor = 15000.00;       // Valor do empréstimo
    private int numeroParcelas = 24;       // Número total de parcelas
    private double jurosMensal = 1.5;      // Taxa de juros mensal (%)
    
    // Controle interno
    private int parcelaCount = 0;          // Contador de parcelas processadas
    private double saldoDevedor = valor;  // Saldo devedor atual
    
    /* ========================================================================
     * SETTERS - Métodos para alterar dados do contrato
     * ======================================================================== */
    
    public void setNome(String n) { nome = n; }
    public void setData(String d) { data = d; }
    public void setValor(double v) { valor = v; saldoDevedor = v; }
    public void setNumeroParcelas(int n) { numeroParcelas = n; }
    public void setJurosMensal(double j) { jurosMensal = j; }
    
    /* ========================================================================
     * MÉTODOS AUXILIARES
     * ======================================================================== */
    
    /**
     * Formata valor monetário no formato brasileiro: R$ X.XXX,XX
     */
    private String formatarMoeda(double valor) {
        return String.format("R$ %.2f", valor);
    }
    
    /**
     * Gera lista de parcelas com cálculo de juros sobre saldo devedor.
     * 
     * Sistema de amortização:
     *   - Amortização: valor / número de parcelas
     *   - Juros: saldo devedor × (taxa mensal / 100)
     *   - Parcela: amortização + juros
     *   - Novo saldo: saldo anterior - amortização
     * 
     * Exemplo (R$ 15000, 24 parcelas, 1.5% a.m.):
     *   Parcela 1: amort=625, juros=225, total=850
     *   Parcela 2: amort=625, juros=215.63, total=840.63
     *   ...
     *   Parcela 24: amort=625, juros=9.38, total=634.38
     */
    private String gerarParcelas() {
        StringBuilder sb = new StringBuilder();
        saldoDevedor = valor;
        
        for (int i = 1; i <= numeroParcelas; i++) {
            // Cálculos
            double amortizacao = valor / numeroParcelas;
            double jurosValor = saldoDevedor * (jurosMensal / 100);
            double valorParcela = amortizacao + jurosValor;
            saldoDevedor -= amortizacao;
            
            // Formatação
            sb.append("\\par\n");  // RTF: quebra de linha
            sb.append(String.format("%d. Parcela %d: %s", i, i, formatarMoeda(valorParcela)));
            if (i < numeroParcelas) {
                sb.append("\\par\n");
            }
        }
        return sb.toString();
    }
%}

/* ============================================================================
 * PADRÕES DE TAGS
 * 
 * Cada tag tem o formato #nome# e será substituída pelo valor correspondente.
 * As tags são case-sensitive e devem aparecer exatamente como definido.
 * ============================================================================ */

/* ----------------------------------------------------------------------------
 * PADRÃO: Tag de data
 * Substituído por: data formatada (ex: "16 de março de 2026")
 * ---------------------------------------------------------------------------- */
DATA = "#data#"

/* ----------------------------------------------------------------------------
 * PADRÃO: Tag de nome
 * Substituído por: nome completo do cliente
 * ---------------------------------------------------------------------------- */
NOME = "#nome#"

/* ----------------------------------------------------------------------------
 * PADRÃO: Tag de valor
 * Substituído por: valor do empréstimo formatado (ex: "R$ 15000.00")
 * ---------------------------------------------------------------------------- */
VALOR = "#valor#"

/* ----------------------------------------------------------------------------
 * PADRÃO: Tag de número de parcelas
 * Substituído por: número inteiro de parcelas
 * ---------------------------------------------------------------------------- */
NUMERO = "#numero#"

/* ----------------------------------------------------------------------------
 * PADRÃO: Tag de juros
 * Substituído por: taxa de juros mensal formatada (ex: "1.5%")
 * ---------------------------------------------------------------------------- */
JUROS = "#juros#"

/* ----------------------------------------------------------------------------
 * PADRÃO: Tag de parcelas
 * Substituído por: lista numerada de parcelas com valores calculados
 * Formato: "1. Parcela 1: R$ 850.00\n...\n24. Parcela 24: R$ 634.38"
 * ---------------------------------------------------------------------------- */
PARCELAS = "#parcelas#"

%%

/* ============================================================================
 * REGRAS LÉXICAS
 * 
 * Cada regra detecta uma tag específica e a substitui pelo valor correspondente.
 * A ordem das regras importa - JFlex usa "最长匹配" (longest match).
 * ============================================================================ */

/* ----------------------------------------------------------------------------
 * REGRA: Substituir #data# pela data atual
 * Exemplo: "#data#" → "16 de março de 2026"
 * ---------------------------------------------------------------------------- */
{DATA} {
    System.out.print(data);
}

/* ----------------------------------------------------------------------------
 * REGRA: Substituir #nome# pelo nome do cliente
 * Exemplo: "#nome#" → "Cássio Jones Dhein"
 * ---------------------------------------------------------------------------- */
{NOME} {
    System.out.print(nome);
}

/* ----------------------------------------------------------------------------
 * REGRA: Substituir #valor# pelo valor do empréstimo
 * Exemplo: "#valor#" → "R$ 15000.00"
 * ---------------------------------------------------------------------------- */
{VALOR} {
    System.out.print(formatarMoeda(valor));
}

/* ----------------------------------------------------------------------------
 * REGRA: Substituir #numero# pelo número de parcelas
 * Exemplo: "#numero#" → "24"
 * ---------------------------------------------------------------------------- */
{NUMERO} {
    System.out.print(numeroParcelas);
}

/* ----------------------------------------------------------------------------
 * REGRA: Substituir #juros# pela taxa de juros mensal
 * Exemplo: "#juros#" → "1.5%"
 * ---------------------------------------------------------------------------- */
{JUROS} {
    System.out.print(String.format("%.1f%%", jurosMensal));
}

/* ----------------------------------------------------------------------------
 * REGRA: Substituir #parcelas# pela lista de parcelas calculadas
 * 
 * Algoritmo:
 *   Para cada parcela i (1 até n):
 *     amortização = valor / n
 *     juros = saldo_devedor × (taxa/100)
 *     parcela = amortização + juros
 *     saldo_devedor -= amortização
 * 
 * Exemplo (R$ 15000, 24 parcelas, 1.5% a.m.):
 *   "1. Parcela 1: R$ 850.00
 *    2. Parcela 2: R$ 840.63
 *    ...
 *    24. Parcela 24: R$ 634.38"
 * ---------------------------------------------------------------------------- */
{PARCELAS} {
    System.out.print(gerarParcelas());
}

/* ----------------------------------------------------------------------------
 * REGRA: Fallback - Passar caracteres normais para saída
 * 
 * Qualquer caractere que não seja uma tag é impresso inalterado.
 * Isso preserva a formatação RTF do template.
 * 
 * NOTA: A ordem importa - esta regra deve ser a ÚLTIMA
 *       JFlex usa regras na ordem em que aparecem
 *       Se esta regra viesse primeiro, consumiria todos os caracteres
 * ---------------------------------------------------------------------------- */
[^] {
    System.out.print(yytext());
}