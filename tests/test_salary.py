import sys
import os
import math

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import SalaryRecord


def approx(a, b, rel=1e-6):
    return math.isclose(a, b, rel_tol=rel, abs_tol=1e-3)


def run_tests():
    cases = [
        ('A', SalaryRecord('SAL-A', 'E', 12, 2025, 10_000_000, 26, 0, 0, 0, 0, 0, None), 10_000_000, 8_390_000, 0),
        ('B', SalaryRecord('SAL-B', 'E', 12, 2025, 10_000_000, 20, 8, 200_000, 50_000, 100_000, 0, None), 8619230.769230769, 6999230.769230769, 5),
        ('C', SalaryRecord('SAL-C', 'E', 12, 2025, 10_000_000, 15, 20, 500_000, 200_000, 300_000, 0, None), 8211538.461538462, 6541538.461538462, 30),
    ]

    for name, rec, exp_gross, exp_net, late in cases:
        gross = rec.calculate_gross_salary()
        net = rec.calculate_net_salary(late_minutes=late)
        print(f"Case {name}: gross={gross:,.0f}, net={net:,.0f}")
        assert approx(gross, exp_gross), f"Gross mismatch for {name}: {gross} != {exp_gross}"
        assert approx(net, exp_net), f"Net mismatch for {name}: {net} != {exp_net}"

    print('All tests passed')


if __name__ == '__main__':
    run_tests()
