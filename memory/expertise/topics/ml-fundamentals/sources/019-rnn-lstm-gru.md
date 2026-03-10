# Recurrent Neural Networks: LSTM and GRU (Deep Dive)

**Source:** Wikipedia, Colah's Blog, Stanford CS231n
**Category:** Deep Learning Architectures
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Recurrent Neural Networks (RNNs)** process sequential data by maintaining a hidden state that captures information from previous time steps. **LSTM** and **GRU** are specialized RNN architectures designed to solve the vanishing gradient problem.

### Problem with Vanilla RNNs

In standard RNNs, gradients are multiplied by the same weight matrix at each time step during backpropagation:

```
∂L/∂h_t = ∂L/∂h_T × ∏_{k=t}^{T-1} W_hh
```

If eigenvalues of W_hh are < 1:
- **Vanishing gradient:** Gradients shrink exponentially
- **Long-term dependencies lost**

If eigenvalues of W_hh are > 1:
- **Exploding gradient:** Gradients grow exponentially
- **Numerical instability**

## LSTM (Long Short-Term Memory)

### Architecture

LSTM introduces a **memory cell** with **gates** that control information flow:

```
Cell State (c_t): Long-term memory
Hidden State (h_t): Working memory / Output
```

### Gates

**1. Forget Gate (f_t):** What to forget from cell state
```
f_t = σ(W_f × [h_{t-1}, x_t] + b_f)
```
- Output: 0 (forget all) to 1 (keep all)
- Controls what information to discard

**2. Input Gate (i_t):** What new information to store
```
i_t = σ(W_i × [h_{t-1}, x_t] + b_i)
c̃_t = tanh(W_c × [h_{t-1}, x_t] + b_c)
```
- i_t: Which values to update
- c̃_t: Candidate values to store

**3. Output Gate (o_t):** What to output from cell state
```
o_t = σ(W_o × [h_{t-1}, x_t] + b_o)
h_t = o_t ⊙ tanh(c_t)
```
- Controls what parts of cell state to output

### Cell State Update

```
c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t
```

**Key insight:** The addition (rather than multiplication) allows gradients to flow unchanged through time → solves vanishing gradient.

### Why LSTM Solves Vanishing Gradient

**Vanilla RNN gradient flow:**
```
∂h_t/∂h_{t-1} = W_hh × σ'(z_t)
```
- If σ'(z_t) < 1 and W_hh < 1 → gradient vanishes

**LSTM gradient flow:**
```
∂c_t/∂c_{t-1} = f_t  (forget gate)
```
- Gradient can flow through if f_t ≈ 1
- Network can learn to keep f_t close to 1 for long-term dependencies

**Constant Error Carousel (CEC):**
- The additive connection c_t = f_t ⊙ c_{t-1} + ... allows error to "carouse" through time
- Network learns which gates to open/close for gradient flow

## GRU (Gated Recurrent Unit)

### Architecture

GRU simplifies LSTM by combining gates:

```
z_t = σ(W_z × [h_{t-1}, x_t])        # Update gate
r_t = σ(W_r × [h_{t-1}, x_t])        # Reset gate
h̃_t = tanh(W × [r_t ⊙ h_{t-1}, x_t])  # Candidate hidden state
h_t = (1 - z_t) ⊙ h_{t-1} + z_t ⊙ h̃_t  # New hidden state
```

### Gates

**1. Reset Gate (r_t):** How much of past to forget
- Controls how much previous state affects candidate state
- r_t = 0: Forget past completely

**2. Update Gate (z_t):** How much of past to keep
- Controls balance between past state and new candidate
- z_t = 0: Keep past state; z_t = 1: Use candidate state

### Comparison with LSTM

| Aspect | LSTM | GRU |
|--------|------|-----|
| **Gates** | 3 (forget, input, output) | 2 (reset, update) |
| **Cell state** | Separate (c_t) | Combined (h_t) |
| **Parameters** | More | Fewer |
| **Speed** | Slower | Faster |
| **Performance** | Similar (task-dependent) | Similar (task-dependent) |

## When to Use Each

| Scenario | Recommendation |
|----------|----------------|
| **Long sequences** | LSTM (more controlled gradient flow) |
| **Limited compute** | GRU (fewer parameters) |
| **Small dataset** | GRU (less overfitting) |
| **Long-term dependencies** | LSTM (explicit cell state) |
| **Default choice** | GRU (simpler, often sufficient) |

## Key Innovations

### 1. Gating Mechanism
- Gates learn to selectively remember/forget
- Gradient can flow through additive connections

### 2. Cell State (LSTM)
- Separate long-term memory from working memory
- Allows network to "carry" information over many time steps

### 3. Peephole Connections (Optional)
- Gates can "peek" at cell state
- f_t, i_t, o_t can depend on c_{t-1}, not just h_{t-1} and x_t

## Applications

| Task | Model |
|------|-------|
| Speech recognition | LSTM/GRU + CTC |
| Machine translation | LSTM/GRU + attention |
| Time series prediction | LSTM/GRU |
| Text generation | LSTM/GRU |
| Video analysis | ConvLSTM |
| Music generation | LSTM |

## Key Takeaways

1. **Vanilla RNNs suffer from vanishing gradient** - Multiplicative gradient flow
2. **LSTM solves this with additive gradient** - Cell state + gates
3. **GRU simplifies LSTM** - Fewer gates, fewer parameters
4. **Both learn long-term dependencies** - Up to thousands of time steps
5. **Gating allows selective information flow** - Learn what to remember/forget
6. **LSTM has explicit cell state** - More control over memory
7. **GRU has implicit cell state** - Simpler but often sufficient

## References

- Hochreiter & Schmidhuber (1997): "Long Short-Term Memory"
- Cho et al. (2014): "Learning Phrase Representations using RNN Encoder-Decoder"
- Gers et al. (2000): "Learning to Forget: Continual Prediction with LSTM"
- Greff et al. (2017): "LSTM: A Search Space Odyssey"