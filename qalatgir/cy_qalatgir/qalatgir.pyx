import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.double
ctypedef np.double_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def get_consecutive_missing(np.ndarray[DTYPE_t, ndim=1] arr, int n):
    cdef int start = 0
    cdef intnull_found = 0
    cdef int miss_count = 0
    misses = np.empty((n // 2 + 1, 2), dtype=np.int64)
    cdef DTYPE_t v = 0
    for i in range(n):
        v = arr[i]
        if not v < 1e40 and not null_found:
            null_found = 1
            start = i
        elif not v < 1e40:
            continue
        elif null_found:
            misses[miss_count, 0] = start
            misses[miss_count, 1] = i
            miss_count += 1
            null_found = 0

    return misses[:miss_count]
