# Quantum Computing: Notation & Linear Algebra Cheat Sheet

*Reference for Lecture 1 — Basics of Quantum Mechanics*

---

## Part 1: Symbol Quick Reference

| Symbol | Name | What it actually is | Linear algebra translation |
|---|---|---|---|
| $\|\psi\rangle$ | ket | A vector representing a quantum state | A column vector, e.g. $\begin{pmatrix}a_0\\a_1\\\vdots\end{pmatrix}$ |
| $\langle\psi\|$ | bra | The "dual" of a ket | The conjugate transpose (row vector) of $\|\psi\rangle$: $(a_0^*, a_1^*, \dots)$ |
| $\langle\psi\|\varphi\rangle$ | bra-ket / inner product | A number measuring overlap between two states | Row vector × column vector → a scalar (complex dot product) |
| $\|\psi\rangle\langle\varphi\|$ | ket-bra / outer product | An operator (matrix), not a number | Column vector × row vector → a matrix |
| $A^\dagger$ | dagger / adjoint | The "Hermitian conjugate" of a matrix | Transpose the matrix, then complex-conjugate every entry |
| $A = A^\dagger$ | Hermitian / self-adjoint | A matrix equal to its own dagger | Complex analogue of a *symmetric* matrix |
| $U^\dagger U = UU^\dagger = I$ | unitary | A matrix whose dagger is its inverse | Complex analogue of an *orthogonal* (rotation-like) matrix |
| $\mathcal{H}$ | Hilbert space | The vector space quantum states live in | For this course: just $\mathbb{C}^N$ with an inner product |
| $\mathbb{C}$ | complex numbers | The field of scalars used (instead of $\mathbb{R}$) | Numbers of the form $x+iy$ |
| $\|\cdot\|$ | norm | Length of a vector | $\|\psi\| = \sqrt{\langle\psi\|\psi\rangle}$, generalizes $\sqrt{x^2+y^2+\dots}$ |
| $E_n = \|n\rangle\langle n\|$ | projector | An operator that "projects onto" a direction | An outer product matrix; $E_n^2 = E_n$ |
| $\alpha_n$ | eigenvalue | The measured/observed value | Real number satisfying $A\|n\rangle = \alpha_n\|n\rangle$ |
| $A = \sum_n \alpha_n E_n$ | spectral decomposition | Diagonalizing an observable | Same as writing $A$ in its eigenbasis |
| $H$ | Hamiltonian | The observable for energy; generates time evolution | A Hermitian matrix |
| $\otimes$ | tensor product | Combines two systems into one bigger system | "Distribute everything against everything" (like FOIL, but for vectors/matrices) |
| $\rho$ | density matrix / density operator | Describes a state, including partial/mixed knowledge | $\rho = \|\psi\rangle\langle\psi\|$ for a pure state |
| $\text{tr}(\cdot)$ | trace | Sum of the diagonal entries of a matrix | Used to compute expectation values: $\text{tr}(M\rho)$ |
| $\text{tr}_B(\cdot)$ | partial trace | "Tracing out" one subsystem to describe the other alone | How you get $\rho_A$ from a joint state of $A$ and $B$ |
| $I$ | identity operator | The "do-nothing" matrix | 1's on the diagonal, 0's elsewhere |
| $e^{i\alpha}$ | global phase | A physically meaningless multiplicative factor | A complex number of magnitude 1 ($\|e^{i\alpha}\|=1$) |

---

## Part 2: Linear Algebra Refresher

### Vectors and complex numbers

A **complex number** is $z = x + iy$, with $i = \sqrt{-1}$. Its **complex conjugate** is $z^* = x - iy$ (flip the sign of the imaginary part). This matters constantly in QM because probabilities come from $|z|^2 = z^*z = x^2+y^2$, which is always a non-negative real number — exactly what you need for something to behave like a probability.

A **vector** here is just a list of complex numbers, e.g. $v = \begin{pmatrix}a\\b\end{pmatrix}$ with $a,b\in\mathbb{C}$. This is no different structurally from vectors in ordinary $\mathbb{R}^2$ or $\mathbb{R}^3$ — you're just allowing complex entries.

### Conjugate transpose (the "dagger," $\dagger$)

For a real matrix, "transpose" means flip rows and columns. For a complex matrix, you do that *and* conjugate every entry:

$$A = \begin{pmatrix} a & b \\ c & d\end{pmatrix} \quad\Longrightarrow\quad A^\dagger = \begin{pmatrix} a^* & c^* \\ b^* & d^*\end{pmatrix}$$

Applied to a vector, this is exactly how you turn a ket $|\psi\rangle$ into its bra $\langle\psi|$: transpose the column into a row, and conjugate each entry.

### Inner product (bra-ket, $\langle\psi|\varphi\rangle$)

This is the complex generalization of the **dot product**. For real vectors you compute $u\cdot v = u_1v_1+u_2v_2+\dots$. For complex vectors, you conjugate the *first* vector's entries before multiplying:

$$\langle\psi|\varphi\rangle = a_0^*b_0 + a_1^*b_1 + \cdots$$

Mechanically: turn $|\psi\rangle$ into the row vector $\langle\psi|$, then do ordinary matrix multiplication (row × column) against $|\varphi\rangle$. The result is a single complex number, and it tells you how much the two states "overlap."

A special case: $\langle\psi|\psi\rangle = |a_0|^2+|a_1|^2+\cdots$, which is always real and non-negative — this is where the normalization condition $\sum|a_i|^2=1$ comes from. It's the same idea as $\|v\|^2 = v\cdot v$ for ordinary vectors.

### Outer product ($|\psi\rangle\langle\varphi|$)

This is the *reverse* order of multiplication from the inner product — column vector times row vector — and it produces a **matrix**, not a number:

$$|\psi\rangle\langle\varphi| = \begin{pmatrix}a_0\\a_1\end{pmatrix}(b_0^*, b_1^*) = \begin{pmatrix} a_0b_0^* & a_0b_1^* \\ a_1b_0^* & a_1b_1^*\end{pmatrix}$$

This is exactly how projectors $E_n = |n\rangle\langle n|$ and density matrices $\rho=|\psi\rangle\langle\psi|$ are built. The rule of thumb: **bra-ket → number, ket-bra → matrix.**

### Hermitian matrices ($A=A^\dagger$)

These are the complex analogue of *symmetric* matrices ($A=A^T$) from ordinary linear algebra. The key fact carried over from your linear algebra course: **symmetric/Hermitian matrices always have real eigenvalues** and their eigenvectors can be chosen to be orthonormal. That's precisely why observables (measurable, real-valued quantities) are modeled as Hermitian matrices — the math guarantees you get real numbers out.

### Eigenvalues, eigenvectors, and diagonalization

Recall the core definition: $A|n\rangle = \alpha_n|n\rangle$ — applying the matrix to $|n\rangle$ just rescales it by the number $\alpha_n$, without changing its direction. The **spectral decomposition**

$$A = \sum_n \alpha_n |n\rangle\langle n|$$

is just diagonalization, written using outer products instead of the $PDP^{-1}$ form you may have seen before. Since Hermitian matrices have orthonormal eigenvectors, $P^{-1}=P^\dagger$, which is a big part of why this notation is so clean in quantum mechanics.

### Projectors

$E_n = |n\rangle\langle n|$ takes any vector and "projects" it onto the line spanned by $|n\rangle$ — geometrically, like a shadow cast onto an axis. Two defining properties:
- $E_n^\dagger = E_n$ (Hermitian)
- $E_n^2 = E_n$ (applying the projection twice does nothing new — once you're on the axis, projecting again doesn't move you)

### Unitary matrices ($U^\dagger U = UU^\dagger = I$)

This is the complex analogue of an **orthogonal matrix** (like a rotation or reflection) from ordinary linear algebra. Orthogonal matrices preserve lengths and angles between real vectors; unitary matrices preserve the inner product between complex vectors — which is exactly why applying $U$ to a quantum state keeps it normalized ($\|\psi\|=1$ stays true) and preserves overlaps between states. Practically: $U^\dagger$ *is* $U^{-1}$, so unitary matrices are always invertible, and "undoing" a quantum operation is as easy as applying its dagger.

### Tensor product ($\otimes$)

This is genuinely new territory if your linear algebra course didn't cover it — it's how you combine two separate vector spaces into one larger one. For vectors, it's essentially the distributive law taken to its logical conclusion:

$$(a|0\rangle+b|1\rangle)\otimes(c|0\rangle+d|1\rangle) = ac|00\rangle+ad|01\rangle+bc|10\rangle+bd|11\rangle$$

Every term of the first vector gets multiplied against every term of the second (like FOIL-ing two binomials), and the resulting basis states get concatenated ($|0\rangle\otimes|0\rangle \to |00\rangle$, etc.). If you have $N$ basis states in one space and $M$ in another, the combined space has $N\times M$ basis states — this is the source of the "exponential blowup" that makes multi-qubit systems so large: $n$ qubits → $2^n$ dimensions.

For matrices, $\otimes$ works similarly (each entry of one matrix gets multiplied by the *entire* other matrix), though the lecture mostly uses it on vectors and on operators like $M_A\otimes I_B$ (apply $M$ to system A, do nothing to system B).

### Trace ($\text{tr}$)

The trace of a matrix is just the sum of its diagonal entries: $\text{tr}(A) = \sum_i A_{ii}$. Two facts worth remembering:
- $\text{tr}(AB) = \text{tr}(BA)$ (cyclic property) — this is what lets you rewrite $\langle\psi|M|\psi\rangle$ as $\text{tr}(M\rho)$.
- The trace of a density matrix is always 1 ($\text{tr}(\rho)=1$), which is the matrix version of "probabilities sum to 1."

### Rank

The **rank** of a matrix is the dimension of the space its columns span — informally, "how many independent directions" it has. In the lecture, $\text{rank}(\rho)=1$ (pure state) means the density matrix is built from a *single* outer product $|\psi\rangle\langle\psi|$, i.e., there's no genuine classical uncertainty mixed in — only quantum uncertainty. A higher rank means you're blending multiple states together with classical probabilities (a mixed state).

---

## Part 3: How the Pieces Fit Together

A useful way to see the whole system at a glance:

| Concept | Built from | Purpose |
|---|---|---|
| State $\|\psi\rangle$ | Unit vector | Describes the system completely (if pure) |
| Observable $A$ | Hermitian matrix | Represents something measurable |
| Measurement | Eigenvalues/eigenvectors of $A$ | Predicts possible outcomes & probabilities |
| Evolution | Unitary matrix $U$ | Describes how the state changes over time |
| Composite systems | Tensor product $\otimes$ | Combines multiple qubits/systems |
| Partial description | Density matrix $\rho$, trace | Describes a subsystem when the whole system is entangled |
