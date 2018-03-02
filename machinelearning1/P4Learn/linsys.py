from decimal import Decimal, getcontext
from copy import deepcopy

from machinelearning1.P4Learn.vector import Vector
from machinelearning1.P4Learn.plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def compute_triangular_form(self):
        system = deepcopy(self)
        l = len(system)
        # 将要达到的三角形式
        triangular_form = [i for i in range(l)]

        curr_triangular_form = system.indices_of_first_nonzero_terms_in_each_row()
        print(curr_triangular_form)
        new_planes = [None] * l
        for row, i in enumerate(curr_triangular_form):
            new_planes[i] = self[row]
        system.planes = new_planes
        curr_triangular_form = system.indices_of_first_nonzero_terms_in_each_row()

        while triangular_form != curr_triangular_form:

            pass

        return system

    def swap_rows(self, row1, row2):
        """交换方程式的位置"""
        self[row1], self[row2] = self[row2], self[row1]

    def multiply_coefficient_and_row(self, coefficient, row):
        """方程式等式两边乘以相同的系数"""
        n = self[row].normal_vector
        k = self[row].constant_term
        new_normal_vector = n.times_scalar(coefficient)
        new_constant_term = k * coefficient
        self[row] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        """将其中一个方程式等式两边乘以相同系数后加到另一个方程式（等式两边同时相加）"""
        n1 = self[row_to_add].normal_vector
        n2 = self[row_to_be_added_to].normal_vector
        k1 = self[row_to_add].constant_term
        k2 = self[row_to_be_added_to].constant_term

        new_normal_vector = n1.times_scalar(coefficient).plus(n2)
        new_constant_term = (k1 * coefficient) + k2
        self.planes[row_to_be_added_to] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


if __name__ == "__main__":
    # p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    # p1 = Plane(normal_vector=Vector(['2', '1', '0']), constant_term='2')
    # p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    # p3 = Plane(normal_vector=Vector(['1', '-3', '-2']), constant_term='2')
    # s = LinearSystem([p0, p1, p2, p3])
    # print(s)

    # p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    # p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    # p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    # p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    #
    # s = LinearSystem([p0, p1, p2, p3])
    # s.swap_rows(0, 1)
    # if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    #     print('test case 1 failed')
    #
    # s.swap_rows(1, 3)
    # if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    #     print('test case 2 failed')
    #
    # s.swap_rows(3, 1)
    # if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    #     print('test case 3 failed')
    #
    # s.multiply_coefficient_and_row(1, 0)
    # if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    #     print('test case 4 failed')
    #
    # s.multiply_coefficient_and_row(-1, 2)
    # if not (s[0] == p1 and
    #         s[1] == p0 and
    #         s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
    #         s[3] == p3):
    #     print('test case 5 failed')
    #
    # s.multiply_coefficient_and_row(10, 1)
    # if not (s[0] == p1 and
    #         s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10') and
    #         s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
    #         s[3] == p3):
    #     print('test case 6 failed')
    #
    # s.add_multiple_times_row_to_row(0, 0, 1)
    # if not (s[0] == p1 and
    #         s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10') and
    #         s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
    #         s[3] == p3):
    #     print('test case 7 failed')
    #
    # s.add_multiple_times_row_to_row(1, 0, 1)
    # if not (s[0] == p1 and
    #         s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12') and
    #         s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
    #         s[3] == p3):
    #     print('test case 8 failed')
    #
    # s.add_multiple_times_row_to_row(-1, 1, 0)
    # if not (s[0] == Plane(normal_vector=Vector(['-10', '-10', '-10']), constant_term='-10') and
    #         s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12') and
    #         s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
    #         s[3] == p3):
    #     print('test case 9 failed')

    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and
            t[1] == p2):
        print('test case 1 failed')

    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    # print(s.indices_of_first_nonzero_terms_in_each_row())
    print(s)
    t = s.compute_triangular_form()
    print(t)
    # if not (t[0] == p1 and
    #         t[1] == Plane(constant_term='1')):
    #     print('test case 2 failed')
    #
    # p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    # p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    # p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    # p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    # s = LinearSystem([p1, p2, p3, p4])
    # t = s.compute_triangular_form()
    # if not (t[0] == p1 and
    #         t[1] == p2 and
    #         t[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
    #         t[3] == Plane()):
    #     print('test case 3 failed')
    #
    # p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    # p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
    # p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
    # s = LinearSystem([p1, p2, p3])
    # t = s.compute_triangular_form()
    # if not (t[0] == Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2') and
    #         t[1] == Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1') and
    #         t[2] == Plane(normal_vector=Vector(['0', '0', '-9']), constant_term='-2')):
    #     print('test case 4 failed')
