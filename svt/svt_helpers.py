from typing import Union

import numpy as np
from scipy.sparse.linalg import svds


def frob_norm(A):
    return np.linalg.norm(A, ord="fro")


def svt_solver(
    M: np.ndarray,
    mask: np.ndarray,
    tol: float = 1e-2,
    delta: Union[float, None] = None,
    tau: Union[float, None] = None,
    n_iters: int = 100,
    random_state: int = 0,
):
    """
    The Singular Value Thresholding solver.
    The primary paper is https://arxiv.org/pdf/0810.3286.pdf

    """
    if not delta:
        # See Eq. (5.1)
        delta = 1.2 * np.prod(M.shape) / np.sum(mask)

    if not tau:
        tau = 5 * np.sum(M.shape) / 2

    # k0 = np.ceil(tau / delta / normPM2)
    k0 = np.ceil(tau / (delta * np.linalg.norm(M, ord=2)))

    # "The SVT algorithm starts with Y^0 = 0." See 5.1.3 Initial steps
    X = np.zeros_like(M)
    Y = k0 * delta * mask * M
    # Y = np.zeros_like(M)

    # r_prev = 0
    r_prev = k0
    print(r_prev)
    prev_err = np.inf
    best_X = X[:]

    for i in range(n_iters):
        k = r_prev + 1

        # if (i + 1) % 50 == 0:
        #   delta = delta / 1.1

        u, s, vh = svds(Y, k, random_state=random_state)
        idx = np.argsort(s)[::-1]
        u = u[..., idx]
        s = s[idx]
        vh = vh[idx]

        while np.min(s) >= tau:
            # Section 5.1.1
            # Otherwise, increment s_k by a predefined integer l repeatedly
            # until some of the singular values fall below tau.
            # In the experiments, we choose l = 5.
            k = k + 5
            u, s, vh = svds(Y, k, random_state=random_state)
            idx = np.argsort(s)[::-1]
            u = u[..., idx]
            s = s[idx]
            vh = vh[idx]

        shrink_s = np.maximum(s - tau, 0)
        r_prev = np.count_nonzero(shrink_s)
        X = u @ np.diag(shrink_s) @ vh
        Y += delta * mask * (M - X)
        # Stopping criteria, see Eq. (5.5)
        err = frob_norm(mask * (X - M)) / frob_norm(mask * M)
        print(f"Iteration: {i}; r_prev: {r_prev}; err: {err:.6f}")
        if err < prev_err:
            prev_err = err
            best_X = X[:]

        if err <= tol:
            break

    print(f"Best error: {prev_err}")
    return best_X
