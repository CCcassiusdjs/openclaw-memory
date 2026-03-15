# OpenClaw Limits Update - 2026-03-14

## Mudanças Aplicadas

### Limites de Leitura (read tool)
| Constante | Antes | Depois |
|-----------|-------|--------|
| `DEFAULT_READ_PAGE_MAX_BYTES` | 50 KB | 10 GB |
| `MAX_ADAPTIVE_READ_MAX_BYTES` | 512 KB | 10 GB |

### Limites de Download/Fetch
| Constante | Antes | Depois |
|-----------|-------|--------|
| `MAX_CAMERA_URL_DOWNLOAD_BYTES` | 250 MB | 10 GB |
| `DEFAULT_MAX_BYTES_MB` | 10 MB | 10 GB |
| `DEFAULT_FETCH_MAX_RESPONSE_BYTES` | 2 MB | 10 GB |
| `DEFAULT_ERROR_MAX_BYTES` | 64 KB | 10 GB |

### Limites de Mídia/Imagem
| Constante | Antes | Depois |
|-----------|-------|--------|
| `MEDIA_MAX_BYTES` | 5 MB | 10 GB |
| `DEFAULT_IMAGE_MAX_BYTES` | 5 MB | 10 GB |

### Limites de web_fetch
| Constante | Antes | Depois |
|-----------|-------|--------|
| `maxChars` (default) | 200.000 chars | 1.000.000.000 chars |

### Limites de Bootstrap
| Constante | Antes | Depois |
|-----------|-------|--------|
| `DEFAULT_BOOTSTRAP_MAX_CHARS` | 20.000 chars | 100.000 chars |
| `DEFAULT_BOOTSTRAP_TOTAL_MAX_CHARS` | 150.000 chars | 500.000 chars |

## Arquivos Modificados
- `dispatch-4PYvcEOv.js`
- `dispatch-Co2ceCdc.js`
- `dispatch-D1dE7Hll.js`
- `dispatch-De_tC0oP.js`
- `dispatch-fIZr3WqW.js`
- `config-mlcrIFGX.js`
- `model-auth-4L-d39tw.js`
- `model-auth-BfsjuQOC.js`
- `model-auth-CTzD-epg.js`
- `model-auth-DkZtfSM9.js`
- `sessions-C7QoPtDq.js`

## Correções Adicionais

### Permissões
- Corrigido owner de `/home/csilva/src/openclaw/` de `root` para `csilva`
- Isso resolveu erros EACCES ao indexar arquivos para memória

### Cache
- Deletado cache de 4.5 GB (`cache-trace.jsonl`)
- Configurado crontab para limpar cache diariamente às 3h

## Razão das Mudanças

Hardware do usuário:
- CPU: i9-12900HX (24 cores)
- RAM: 62 GB
- Modelos em nuvem (não locais)

Como os modelos rodam em nuvem, o gargalo não é CPU/RAM local, então é seguro aumentar os limites para permitir análise de projetos grandes.