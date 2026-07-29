def ngetest(measured, target, tolerance):
    error = abs(measured - target)
    return error <= tolerance