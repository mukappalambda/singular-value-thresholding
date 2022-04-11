import numpy as np
from scipy.sparse.linalg import svds

def frob_norm(A):
  return np.linalg.norm(A, ord="fro")

def svt_solver(
  M: np.ndarray,
  mask: np.ndarray,
  tol: float = 1e-2,
  delta: float = None,
  tau: float = None,
  a_min: float = 0.,
  a_max: float = 1.,
  n_iters: int = 100,
  random_state: int = 0
):
  """
  The primary paper is https://arxiv.org/pdf/0810.3286.pdf
  
  """
  if not delta:
    # See Eq. (5.1)
    delta = 1.2 * np.prod(M.shape) / np.sum(mask)

  if not tau:
    tau = 5 * np.sum(M.shape) / 2
    
  normPM2 = np.linalg.svd(mask * M, compute_uv=False)[0]
  # k0 = np.ceil(tau / delta / normPM2)
  # "The SVT algorithm starts with Y^0 = 0." See 5.1.3 Initial steps
  Y = np.zeros_like(M)
  r_prev = 0
  
  for i in range(n_iters):
    
    if i == 0:
      X = np.zeros_like(M)
          
    k = r_prev + 1
      
    # if (i + 1) % 50 == 0:
    #   delta = delta / 1.1
      
    # u, s, vt = randomized_svd(Y, k)
    u, s, vt = svds(Y, k, random_state=random_state)
              
    while np.min(s) >= tau:
      # Section 5.1.1
      # Otherwise, increment s_k by a predefined integer l repeatedly
      # until some of the singular values fall below tau.
      # In the experiments, we choose l = 5.
      k = k + 5
      # u, s, vt = randomized_svd(Y, k)
      u, s, vt = svds(Y, k, random_state=random_state)
      
    shrink_s = np.maximum(s - tau, 0)
    r_prev = np.count_nonzero(shrink_s)
    X = u @ np.diag(shrink_s) @ vt
    Y += delta * mask * (M - X)
    # Stopping criteria, see Eq. (5.5)
    err = frob_norm(mask * (X-M)) / frob_norm(mask * M)
    print(f"Iteration: {i}; r_prev: {r_prev}; err: {err:.6f}")
    
    if err <= tol:
      # This step is to give reasonable pixel values
      X = np.clip(X, a_min, a_max)
      break
      
  return X