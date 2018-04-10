from mygrad.operation_base import Operation, BroadcastableOp
import numpy as np


__all__ = ["Abs",
           "Sqrt",
           "Cbrt",
           "Maximum",
           "Minimum"]


class Abs(Operation):
    def __call__(self, a):
        self.variables = (a,)
        return np.abs(a.data)

    def backward_var(self, grad, index, **kwargs):
        a = self.variables[index]
        a.backward(grad * np.piecewise(a.data,
                                       [a.data < 0, a.data == 0, a.data > 0],
                                       [-1, np.nan, 1]),
                   **kwargs)


class Sqrt(Operation):
    def __call__(self, a):
        """ f(a) = sqrt(a)

            Parameters
            ----------
            a : mygrad.Tensor"""
        self.variables = (a,)
        return np.sqrt(a.data)

    def backward_var(self, grad, index, **kwargs):
        a = self.variables[index]
        a.backward(grad / (2 * np.sqrt(a.data)), **kwargs)


class Cbrt(Operation):
    def __call__(self, a):
        self.variables = (a,)
        return np.cbrt(a.data)

    def backward_var(self, grad, index, **kwargs):
        a = self.variables[index]
        a.backward(grad / (3 * np.cbrt(a.data ** 2)), **kwargs)


class Maximum(BroadcastableOp):
    def __call__(self, a, b):
        self.variables = (a, b)
        self.max_mask = a.data > b.data
        self.equal_mask = a.data == b.data
        return np.where(self.max_mask, a.data, b.data)

    def backward_var(self, grad, index, **kwargs):
        if index == 0:
            mask = self.max_mask
        elif index == 1:
            mask = np.logical_not(self.max_mask)
        else:
            raise IndexError

        #np.logical_not(mask, out=mask, where=self.equal_mask)
        self.variables[index].backward(mask * grad, **kwargs)


class Minimum(BroadcastableOp):
    def __call__(self, a, b):
        self.variables = (a, b)
        self.max_mask = a.data < b.data
        self.equal_mask = a.data == b.data
        return np.where(self.max_mask, a.data, b.data)

    def backward_var(self, grad, index, **kwargs):
        if index == 0:
            mask = self.max_mask
        elif index == 1:
            mask = np.logical_not(self.max_mask)
        else:
            raise IndexError

        #np.logical_not(mask, out=mask, where=self.equal_mask)
        self.variables[index].backward(mask * grad, **kwargs)
