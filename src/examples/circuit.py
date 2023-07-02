#!/usr/bin/python

# pylint: skip-file

import sys
import yaml
import numpy as np

qubits_number = 4


h = (1 / np.sqrt(2)) * np.array([
   1,  1,
   1, -1,
], dtype=np.complex128).reshape((2, 2))
x = np.array([
   0, 1,
   1, 0,
], dtype=np.complex128).reshape((2, 2))
y = np.array([
    0,  1j,
   -1j,  0,
], dtype=np.complex128).reshape((2, 2))
z = np.array([
   1,  0,
   0, -1,
], dtype=np.complex128).reshape((2, 2))
cnot = np.array([
   1, 0, 0, 0,
   0, 1, 0, 0,
   0, 0, 0, 1,
   0, 0, 1, 0,
], dtype=np.complex128).reshape((4, 4))


def _apply_q2_gate(
        state: np.ndarray,
        gate: np.ndarray,
        pos2: int,
        pos1: int
) -> np.array:
  in_shape = state.shape
  qubits_number = len(state.shape)
  nppos1 = qubits_number - 1 - pos1
  nppos2 = qubits_number - 1 - pos2
  state = np.tensordot(gate.reshape((2, 2, 2, 2)), state, axes=[[2, 3], [nppos2, nppos1]])
  min_pos = min(nppos1, nppos2)
  max_pos = max(nppos1, nppos2)
  state = state.reshape((2, 2, 2 ** min_pos, 2 ** (max_pos - min_pos - 1), 2 ** (qubits_number - max_pos - 1)))
  if nppos2 > nppos1:
    state = state.transpose((2, 1, 3, 0, 4))
  else:
    state = state.transpose((2, 0, 3, 1, 4))
  return state.reshape(in_shape)


def _apply_q1_gate(
        state: np.ndarray,
        gate: np.ndarray,
        pos: int,
) -> np.ndarray:
  in_shape = state.shape
  qubits_number = len(state.shape)
  nppos = qubits_number - 1 - pos
  state = np.tensordot(gate, state, axes=[[1], [nppos]])
  state = state.reshape((2, 2 ** nppos, 2 ** (qubits_number - nppos - 1)))
  state = state.transpose((1, 0, 2))
  return state.reshape(in_shape)


def main():
    np.random.seed(42)
    config = yaml.safe_load(sys.stdin)
    params_number = len(config)
    target_state = np.random.normal(size = (16, 2))
    target_state = target_state[:, 0] + 1j * target_state[:, 1]
    target_state /= np.linalg.norm(target_state)
    state = np.zeros((16,), dtype=np.complex128).reshape((2, 2, 2, 2))
    state[0, 0, 0, 0] = 1
    for i in range(params_number):
        match config[str(i)]:
            case "h":
                pos = i % qubits_number
                state = _apply_q1_gate(state, h, pos)
            case "x":
                pos = i % qubits_number
                state = _apply_q1_gate(state, x, pos)
            case "y":
                pos = i % qubits_number
                state = _apply_q1_gate(state, y, pos)
            case "z":
                pos = i % qubits_number
                state = _apply_q1_gate(state, z, pos)
            case "id":
                pass
            case "cnot":
                pos1 = i % qubits_number
                pos2 = (i + 1) % qubits_number
                state = _apply_q2_gate(state, cnot, pos2, pos1)
    dotval = np.tensordot(target_state, np.conj(state.reshape((16,))), axes=1)
    print(np.log(float(np.abs(dotval).real)))
    return 0


if __name__ == '__main__':
    main()
