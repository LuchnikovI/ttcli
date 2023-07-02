"""Tests checking that ttrs works correctly"""

import numpy as np
from ttrs import TTVc64  # type: ignore

MODES_NUM = 10

def _encoder(index):
    if index is None:
        return None
    weights = 1 / (2 ** np.arange(0, MODES_NUM))
    return np.array(np.tensordot(index, weights, axes=1), dtype=np.complex128)


def _function(arg):
    return np.cos(250 * (arg - 1.23456789)) / ((arg - 1.23456789) ** 2 + 0.0001)\
          + 500 * (arg - 1.23456789) ** 2


def test_tt_works():
    """Tests that ttrs finds a global optima of a simple function correctly."""
    tt_function = TTVc64(
        MODES_NUM * [2],
        20,
        1e-5,
        True,
    )
    for _ in range(MODES_NUM * 3):
        index = tt_function.get_args()
        if index is None:
            tt_function.update(None)
        else:
            val = _function(_encoder(index))
            tt_function.update(val)
    argmax = tt_function.argmax_modulo(1e-10, 200, 20, 10)
    assert np.abs(_encoder(argmax) - 1.23456789) < 0.001
