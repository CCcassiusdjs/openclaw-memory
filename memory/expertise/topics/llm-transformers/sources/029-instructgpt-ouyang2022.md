# InstructGPT: Training Language Models to Follow Instructions with Human Feedback

**Source ID:** 029
**Type:** Research Paper (ArXiv)
**Authors:** Long Ouyang, Jeff Wu, Xu Jiang, et al. (OpenAI)
**URL:** https://arxiv.org/abs/2203.02155
**Published:** 2022
**Read Date:** 2026-03-12

---

## 📖 Summary

InstructGPT demonstrates how to align language models with user intent through fine-tuning with human feedback. Using a combination of supervised learning and reinforcement learning from human feedback (RLHF), a 1.3B parameter InstructGPT model outperforms the 175B GPT-3 on human evaluations.

### Core Contribution
- **RLHF for alignment** - Reinforcement learning from human feedback
- **Small model beats large** - 1.3B InstructGPT > 175B GPT-3
- **Improved truthfulness** - Reduced hallucinations
- **Reduced toxicity** - Better safety profile

---

## 🔑 Key Concepts Learned

### 1. Three-Step Training Process

```
Step 1: Supervised Fine-Tuning (SFT)
  - Collect demonstrations from labelers
  - Fine-tune GPT-3 on these demonstrations
  
Step 2: Reward Model Training
  - Collect rankings of model outputs
  - Train reward model to predict human preferences
  
Step 3: PPO Fine-Tuning
  - Use reward model to score outputs
  - Optimize policy with PPO algorithm
```

### 2. Data Collection

| Stage | Data Type | Size |
|-------|-----------|------|
| SFT | Labeler demonstrations | ~13k prompts |
| Reward Model | Output rankings | ~33k comparisons |
| PPO | Prompt distribution | API prompts |

### 3. Reward Model Training

**Process:**
1. Model generates multiple outputs for same prompt
2. Labelers rank outputs by quality
3. Train reward model to predict rankings
4. Use reward model as objective for RL

### 4. PPO (Proximal Policy Optimization)

**Objective:**
```
L(θ) = E[reward_model(output) - β × KL(output || initial_model)]
```

- Maximize reward model score
- KL penalty prevents drift from initial model
- Ensures model doesn't deviate too far

---

## 📊 Performance Results

### Human Evaluations

| Model | Parameters | Preference Rate |
|-------|------------|----------------|
| GPT-3 (175B) | 175B | ~20% |
| InstructGPT (1.3B) | 1.3B | ~85% |

### Key Improvements

| Metric | GPT-3 | InstructGPT |
|--------|-------|-------------|
| Following instructions | Poor | Good |
| Truthfulness | Lower | Higher |
| Toxicity | Higher | Lower |
| Hallucinations | More | Fewer |

---

## 🔬 Key Insights

### 1. Alignment > Scale

- 100x smaller model can outperform larger model
- Fine-tuning for alignment is highly effective
- Human feedback teaches user intent

### 2. Safety Improvements

**Truthfulness:**
- Reduced making things up
- Better at admitting uncertainty
- Less confabulation

**Toxicity:**
- Fewer harmful outputs
- Better refusal of inappropriate requests
- More consistent with human values

### 3. Training Distribution Shift

- Model trained on API prompts
- Generalizes to wider distribution
- Some regression on academic NLP tasks

---

## 🎓 Practical Implementation

### SFT Details
- Learning rate: Decayed from 9.65e-6
- Epochs: Variable (based on validation loss)
- Batch size: 8

### Reward Model Details
- Architecture: Same as policy model
- Output: Scalar reward
- Training: Binary classification on preferences

### PPO Details
- KL coefficient (β): 0.02
- PPO clip range: 0.2
- Learning rate: 1.5e-5

---

## 📝 Key Takeaways

1. **Human feedback is powerful** - Small aligned model beats large unaligned
2. **RLHF is effective** - Reward model + PPO works well
3. **Trade-offs exist** - Some NLP task regression
4. **Safety improves** - Reduced toxicity, hallucinations
5. **Foundation for ChatGPT** - This approach led to ChatGPT

---

## 🔗 Impact

InstructGPT influenced:
- **ChatGPT** - Direct application of RLHF
- **GPT-4** - Continued alignment work
- **Claude** - Constitutional AI builds on RLHF
- **Llama 2 Chat** - Open-source RLHF implementation

---

**Relevância:** ★★★★★ (Foundational RLHF Paper)
**Status:** `completed`
**Reading Time:** Paper ~30 pages, Core concepts ~25 minutes