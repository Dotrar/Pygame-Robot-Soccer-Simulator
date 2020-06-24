''' Set of helpers and misc functions for navsim ai''' 
import np


def convolve(kernel: np.ndarray, vectors: np.ndarray) -> np.ndarray:
    ''' convolve a kernel and vectors array '''
    tmp = np.concatenate([vectors]*3)
    tmp = np.convolve(tmp, kernel, 'same')
    return np.array_split(tmp, 3)[1
