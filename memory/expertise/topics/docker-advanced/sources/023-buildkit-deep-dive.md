# Docker BuildKit Deep Dive (SparkFabrik)

**Fonte:** https://tech.sparkfabrik.com/en/blog/docker-cache-deep-dive/
**Tipo:** Blog Post (Technical Deep Dive)
**Lido em:** 2026-03-10
**Status:** completed

---

## BuildKit Architecture

### Components

| Component | Role |
|-----------|------|
| **Client** | CLI (docker build, buildx, buildctl) |
| **Server** | Daemon (buildkitd) via gRPC |
| **Frontend** | Interprets Dockerfile → LLB |
| **Solver** | Executes LLB graph |
| **Worker** | Runs operations in parallel |

### Workflow
```
buildctl → buildkitd → LLBSolver → Job → FrontendLLBBridge → Frontend (dockerfile.v0)
                                              ↓
                                          LLB Graph → Solver → Workers
```

### LLB (Low-Level Build)
- DAG (Directed Acyclic Graph)
- Each node = Vertex (build step)
- Content-addressable digest
- Parallel execution where possible

---

## Cache Types

### Default Cache (Always Active)
- `source.local`: Files from ADD/COPY
- `exec.cachemount`: RUN --mount=type=cache
- `source.git.checkout`: Git clones

Disable with `--no-cache`

### External Cache Sources

| Type | Description | Best For |
|------|-------------|----------|
| **Inline** | Embedded in image | Simple builds |
| **Registry** | Separate image in OCI registry | CI/CD, teams |
| **Local/Filesystem** | OCI layout in directory | Air-gapped, local |
| **GHA/S3/Azure** | Cloud storage | GitHub Actions |

---

## Inline vs Registry Cache

### Inline Cache
```bash
docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t myimage .
```

**Pros:**
- Simple, no extra config
- Cache travels with image

**Cons:**
- Limited for multi-stage builds
- Increased image size
- Final layers only

### Registry Cache
```bash
docker buildx build \
  --cache-to type=registry,ref=registry/cache:tag \
  --cache-from type=registry,ref=registry/cache:tag \
  -t myimage .
```

**Pros:**
- Team sharing
- Full cache with mode=max
- Works with any OCI registry

**Cons:**
- Network latency
- Storage costs

---

## mode=min vs mode=max

| Mode | What's Cached | Export Time | Rebuild Time | Use Case |
|------|---------------|-------------|--------------|----------|
| **min** (default) | Final layers only | Low | Slower | Simple builds, limited space |
| **max** | All layers (including intermediate) | High | Faster | Multi-stage, shared cache |

---

## Registry-Specific Config

### AWS ECR
```bash
--cache-to type=registry,ref=<ecr>:<tag>,image-manifest=true,oci-mediatypes=true
```

### Compression
```bash
--cache-to type=registry,ref=<registry>:<tag>,compression=zstd,compression-level=3
```

Options: gzip (default), zstd, estargz, uncompressed

---

## Best Practices

1. **Use Registry cache for CI/CD** - Share between pipelines
2. **mode=max for complex builds** - Cache intermediate stages
3. **Multiple cache-from** - Import from branch + main
4. **Compression zstd** - Better performance
5. **OCI metadata for ECR** - Required compatibility

---

## Performance Tips

### Parallel Execution
- BuildKit executes independent vertices in parallel
- Workers scale automatically

### Cache Hit Optimization
- Order instructions from least to most frequent changes
- Use cache mounts for package managers

### Remote Cache
- Share across machines
- Persist in ephemeral CI environments

## Próximos Passos
- [ ] Configure registry cache in CI/CD
- [ ] Test mode=min vs mode=max
- [ ] Implement compression zstd