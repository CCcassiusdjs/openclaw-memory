# Docker Debugging - 7 Practical Tips (Lumigo)

**Fonte:** https://lumigo.io/container-monitoring/docker-debugging-common-scenarios-and-7-practical-tips/
**Tipo:** Blog Post
**Lido em:** 2026-03-10
**Status:** completed

---

## Cenários Comuns de Debugging

### 1. Container Lifecycle Issues
- Container não inicia
- Dockerfile configuration errors
- Missing dependencies

**Comandos:**
```bash
docker logs [container_id]
docker inspect [container_id]
```

### 2. Application Errors within Containers
- Code bugs
- Misconfigured environments

**Comandos:**
```bash
docker exec -it [container_id] bash
# Access container shell for real-time debugging
```

### 3. Docker Network Issues
- Containers não comunicam
- External network problems

**Comandos:**
```bash
docker network inspect [network_name]
ping / traceroute from within container
```

### 4. Performance Bottlenecks
- CPU, memory, I/O, network limits

**Comandos:**
```bash
docker stats
docker logs [container_id]
```

---

## 7 Practical Tips

### Tip 1: View stdout History with Logs
```bash
docker logs [container ID]
docker logs --tail 100 [container ID]
```

### Tip 2: Stream stdout with Attach
```bash
docker attach [container ID]
```
- Real-time stdout/stderr to terminal
- Interactive debugging

### Tip 3: Execute Arbitrary Commands with exec
```bash
docker exec [container ID] [command]
docker exec -it [container ID] bash
```
- Inspect environment
- Check permissions
- Install debugging tools

### Tip 4: Add Options with CMD
```dockerfile
CMD ["node", "--inspect", "app.js"]
```
- Modify behavior without rebuild
- Enable debugging features
- Change logging levels

### Tip 5: Pause and Unpause Container
```bash
docker pause [container ID]
docker unpause [container ID]
```
- Freeze container to inspect state
- Investigate without progression

### Tip 6: View Container Details with inspect
```bash
docker inspect [container ID]
```
- Network settings
- Environment variables
- Mounts
- Configuration details

### Tip 7: One Process per Container
- Isolate issues to specific containers
- Easier to diagnose
- Better modularity
- Microservices approach

---

## Quick Reference

| Scenario | Command |
|----------|---------|
| View logs | `docker logs --tail 100 [ID]` |
| Real-time output | `docker attach [ID]` |
| Shell access | `docker exec -it [ID] bash` |
| Container details | `docker inspect [ID]` |
| Resource usage | `docker stats [ID]` |
| Freeze container | `docker pause [ID]` |
| Network config | `docker network inspect [network]` |

## Próximos Passos
- [ ] Praticar cada comando
- [ ] Criar cheat sheet
- [ ] Configurar monitoring