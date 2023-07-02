"""TTOpt test"""

import numpy as np
from tt_opt import maximize

MODES_NUM = 20

def _encoder(index):
    if index is None:
        return None
    weights = 1 / (2 ** np.arange(0, MODES_NUM))
    return np.array(np.tensordot(index, weights, axes=1), dtype=np.complex128)


def _function(arg):
    return np.cos(250 * (arg - 1.23456789)) / ((arg - 1.23456789) ** 2 + 0.0001)\
          + 500 * (arg - 1.23456789) ** 2

def test_maximize():
    """Test TTOpt maximization function."""

    argmax, max_val = maximize(
        lambda x: _function(_encoder(x)),
        [2] * MODES_NUM,
        7,
        4,
        1e-5,
    )
    assert np.abs(_encoder(argmax) - 1.23456789) < 1e-6
    assert np.abs(max_val - 10000) < 1e-3
