# Sistema de Auto-Aprendizado

## Como Funciona

1. **Cron Job** executa a cada 4 horas
2. **Lê queue.yaml** para encontrar próximo tópico
3. **Busca fonte** (docs ou papers)
4. **Resumo e salva** em topics/[topico]/
5. **Atualiza progress.json**
6. **Commita mudanças**

## Estrutura

```
expertise/
├── queue.yaml          # Fila de tópicos
├── progress.json       # Progresso atual
├── topics/            # Resumos por tópico
│   ├── ardupilot-ekf/
│   ├── drone-sensors/
│   └── ...
├── papers/             # Resumos de papers
└── heuristics.md       # Padrões aprendidos
```

## Status dos Tópicos

- `queued`: Aguardando estudo
- `in_progress`: Sendo estudado
- `completed`: Estudado completamente

## Próxima Execução

O cron job `auto-study-expertise` roda a cada 4 horas automaticamente.
