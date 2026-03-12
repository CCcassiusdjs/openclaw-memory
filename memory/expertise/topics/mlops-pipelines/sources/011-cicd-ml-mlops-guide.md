# CI/CD for Machine Learning - MLOps Guide

**Fonte:** https://mlops-guide.github.io/MLOps/CICDML/
**Tipo:** Tutorial
**Data:** 2026-03-12

---

## 🔄 CI/CD para ML vs Software Tradicional

Em ML, o pipeline depende não só do código, mas também de:
- **Data** - Dados de treino
- **Hyperparameters** - Parâmetros do modelo
- **Deploy complexo** - Mais etapas que software tradicional

## 📋 Continuous Integration (CI)

### Definição
CI em ML = toda vez que código ou data é atualizado, o ML pipeline re-executa

### Características
- **Versionado** - Tudo versionado e reprodutível
- **Compartilhável** - Codebase compartilhado entre projetos/teams
- **Comparável** - Fácil comparar com versões em produção

### CI Workflow Examples

| Trigger | Ação |
|---------|------|
| Commit no repo | Running + versioning training/evaluation |
| Pull Request | Running + comparing experiment runs |
| Periodicamente | Trigger new run (scheduled) |

### Testes em CI
- Code format tests
- Dataset values tests (NaN, wrong data types)
- Function output tests

## 🚀 Continuous Deployment (CD)

### Definição
Automatizar deployment de new releases para production/staging

### Benefícios
- Feedback mais rápido de usuários
- Changes mais rápidas e constantes
- Novos dados para retraining

### CD Workflow Examples

| Step | Ação |
|------|------|
| Verify requirements | Infrastructure environment checks |
| Model test | Test output com known input |
| Load testing | Model latency validation |

## 🛠️ Ferramentas CI/CD para ML

| Tool | Licença | Desenvolvedor | Observações |
|------|---------|---------------|-------------|
| **CML** (Continuous Machine Learning) | Open-source | Iterative | Mais popular para ML-specific CI/CD. Integra com DVC. Usa Github Actions ou GitLab CI/CD |
| **Jenkins** | Open-source | Jenkins CI | Popular para CI/CD geral. Configuração necessária para ML. Bom para local hardware ou cloud configurada |

## 💡 Conceitos-Chave

1. **Code + Data + Hyperparams** - ML depende de todos três
2. **Versioning everything** - Código, dados, experimentos
3. **Scheduled runs** - Trigger periódico além de commits
4. **Model testing** - Test output com known input antes de deploy
5. **Load testing** - Latência do modelo em produção

## 🔄 Pipeline CI/CD ML Flow

```
Code/Data Update → CI Pipeline Run → Version & Log → Compare → 
If Approved → CD Pipeline → Verify Infrastructure → Test Model → Deploy
```

## 🔗 Referências Cruzadas

- Pré-requisito: MLOps Principles (002)
- Relacionado a: MLOps Best Practices (003)
- Complementa: DVC (035-038)

---

**Conceitos aprendidos:** 6
**Relevância:** Alta (fundamentos CI/CD específicos para ML)