from .pypareto import (
    Cmp,
    Comparison,
    ComparisonChain,
    Domination,
    MaxMin,
    MaxMinList,
    by_none,
    by_value,
    by_value_and_not_none,
    cmp_to_target,
    dominates,
    find_dimension_maxmin_set,
    get_dominating_set,
    split_by_dimensions,
    split_by_pareto)

__doc__ = """
= pypareto =
Pypareto is a Python library for pareto front seaching
== Usage ==
""" + "\n".join( [l.lstrip(" ") for l in ComparisonChain.split_by_pareto.__doc__.split("\n")])

__all__ = [
    'Cmp',
    'Comparison',
    'ComparisonChain',
    'Domination',
    'MaxMin',
    'MaxMinList',
    'by_none',
    'by_value',
    'by_value_and_not_none',
    'cmp_to_target',
    'dominates',
    'find_dimension_maxmin_set',
    'get_dominating_set',
    'split_by_dimensions',
    'split_by_pareto']