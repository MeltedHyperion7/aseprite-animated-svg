def n_dim_matrix(dims, start=0, fill=0):
    if start == len(dims):
        return fill
    matrix = [0] * dims[start]
    for i in range(dims[start]):
        matrix[i] = n_dim_matrix(dims, start+1, fill)

    return matrix
