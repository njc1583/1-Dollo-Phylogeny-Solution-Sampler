import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_formula import get_cnf, read_matrix
from get_vars import write_vars
from count_num_solutions import get_num_solutions

sharpSAT_path = '../../../scratch/software/src/sharpSAT/build/Release/sharpSAT'
tmp_formula_path = 'tmp_formula.cnf'

class CheckFormula(unittest.TestCase):

    # A single forbidden matrix, no clustering allowed, no false positives or false negatives allowed,
    # all losses allowed
    #
    # 3 solutions are:
    # 1 2   1 0   1 2
    # 0 1   2 1   2 1
    # 1 1 , 1 1,  1 1
    def test_simple_forbidden(self):
        get_cnf('tests/test_inputs/simple_forbidden.txt', tmp_formula_path, 3, 2, True, None, 0, 0)
        num_sols = get_num_solutions(sharpSAT_path, tmp_formula_path)
        os.system(f'rm {tmp_formula_path}')

        self.assertEqual(num_sols, 3)

    # No way to cluster this matrix to a 4x4 using only one fn
    def test_no_solutions_no_clustering(self):
        get_cnf('tests/test_inputs/no_clustering.txt', tmp_formula_path, 4, 4, True, None, 1, 0)
        num_sols = get_num_solutions(sharpSAT_path, tmp_formula_path)
        os.system(f'rm {tmp_formula_path}')

        self.assertEqual(num_sols, 0)
    
    # 6 possible solutions for given matrix:
    # 1 0 0  1 2 0  1 2 2  1 2 2  1 0 0  1 2 0  
    # 1 1 0  1 1 0  1 1 0  1 1 2  1 1 2  1 1 2  
    # 1 1 1, 1 1 1, 1 1 1, 1 1 1, 1 1 1, 1 1 1
    def test_harder_no_error(self):
        get_cnf('tests/test_inputs/test_harder.txt', tmp_formula_path, 4, 4, True, None, 0, 0)
        num_sols = get_num_solutions(sharpSAT_path, tmp_formula_path)
        os.system(f'rm {tmp_formula_path}')

        self.assertEqual(num_sols, 6)

if __name__ == '__main__':
    unittest.main()