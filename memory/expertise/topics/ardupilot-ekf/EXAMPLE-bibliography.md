# Exemplo: Levantamento Bibliográfico

Este arquivo mostra como deve ser feito o levantamento bibliográfico quando um novo tópico é adicionado.

## Processo

### 1. Buscas Realizadas

```yaml
queries:
  - engine: "brave"
    query: "ArduPilot EKF3 extended kalman filter documentation"
    
  - engine: "brave"
    query: "site:arxiv.org state estimation drone EKF"
    
  - engine: "brave"
    query: "site:ieee.org extended kalman filter drone survey"
    
  - engine: "brave"
    query: "kalman filter tutorial book pdf"
    
  - engine: "brave"
    query: "ArduPilot EKF3 source code github"
```

### 2. Resultados Organizados

```markdown
# BIBLIOGRAPHY: ArduPilot EKF & State Estimation

## FUNDAMENTAL (Leitura Obrigatória)

### Documentação Oficial
1. [✓] ArduPilot EKF3 Overview
   - URL: https://ardupilot.org/copter/docs/ekf3-estimation.html
   - Tipo: Official Documentation
   - Prioridade: CRÍTICA
   - Estimativa: 2h
   - Status: pending

2. [✓] ArduPilot EKF3 Developer Guide
   - URL: https://ardupilot.org/dev/docs/ekf3.html
   - Tipo: Developer Documentation
   - Prioridade: CRÍTICA
   - Estimativa: 4h
   - Status: pending

3. [✓] ArduPilot EKF Innovations
   - URL: https://ardupilot.org/copter/docs/common-ekf-innovations.html
   - Tipo: Operational Guide
   - Prioridade: ALTA
   - Estimativa: 1h
   - Status: pending

### Papers Fundamentais
4. [✓] "A Tutorial on Nonlinear Filtering and Estimation"
   - Autores: Dan Simon
   - Ano: 2006
   - URL: https://www.mathworks.com/help/fusion/ug/extended-kalman-filter.html
   - Tipo: Tutorial
   - Prioridade: ALTA
   - Estimativa: 4h
   - Status: pending

5. [✓] "Optimal State Estimation: Kalman, H∞, and Nonlinear Approaches"
   - Autor: Dan Simon
   - Ano: 2006
   - Tipo: Book
   - Prioridade: ALTA
   - Estimativa: 40h (capítulos relevantes: 5h)
   - Status: pending

## COMPLEMENTAR (Leitura Recomendada)

### Papers de State of Art
6. [ ] "A Survey of Motion Planning and Control Techniques for Self-Driving Urban Vehicles"
   - Autores: Paden et al.
   - Ano: 2016
   - Tipo: Survey Paper
   - Prioridade: MÉDIA
   - Estimativa: 3h
   - Status: pending

7. [ ] "A Survey of Autonomous Driving: Common Practices and Emerging Technologies"
   - Autores: Yurtsever et al.
   - Ano: 2020
   - Tipo: Survey Paper
   - Prioridade: MÉDIA
   - Estimativa: 3h
   - Status: pending

### Tutoriais e Cursos
8. [ ] MATLAB Extended Kalman Filter Tutorial
   - URL: mathworks.com/help/fusion/ug/extended-kalman-filter.html
   - Tipo: Interactive Tutorial
   - Prioridade: MÉDIA
   - Estimativa: 2h
   - Status: pending

### Código Fonte
9. [ ] ArduPilot EKF3 Source Code
   - URL: https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_NavEKF3
   - Tipo: Source Code
   - Prioridade: BAIXA (ler após entender teoria)
   - Estimativa: 8h
   - Status: pending

## AVANÇADO (Leitura Opcional)

### Papers Especializados
10. [ ] "A Nonlinear Estimator for GPS/INS Integration"
    - Autores: Rogers
    - Ano: 2005
    - Tipo: Research Paper
    - Prioridade: BAIXA
    - Estimativa: 3h
    - Status: pending

---

## RESUMO DO LEVANTAMENTO

| Categoria | Quantidade | Tempo Estimado |
|-----------|------------|----------------|
| Fundamental | 5 fontes | ~51h (capítulos relevantes: ~12h) |
| Complementar | 4 fontes | ~16h |
| Avançado | 1 fonte | ~3h |
| **TOTAL** | **10 fontes** | **~31h (fundamental + complementar)** |

## ORDEM DE LEITURA RECOMENDADA

1. EKF3 Overview (2h) - Documentação oficial
2. EKF Innovations (1h) - Guia operacional
3. EKF3 Developer Guide (4h) - Documentação técnica
4. Dan Simon Tutorial (4h) - Fundamentação teórica
5. MATLAB Tutorial (2h) - Prática
6. Livro Dan Simon - Capítulos relevantes (5h)
7. Survey Papers (6h) - Estado da arte
8. Código fonte (8h) - Implementação
```

## Status

| Campo | Valor |
|-------|-------|
| Levantamento Completo | ✅ Sim |
| Total de Fontes | 10 |
| Tempo Estimado | ~31h |
| Próxima Ação | Ler fonte #1 (EKF3 Overview) |