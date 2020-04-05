
# pypareto
Pypareto is a Python library for pareto front seaching
## Usage 

ComparisonChain.split_by_pareto performs the pareto front split fronts

Here the None means just inferior value

    >>> values = [(0,None,None), (2,2,2), (0,1,1), (0,0,1), (None,0,1), (0,1,0), (None,1,1), (1,0,0), (0,0,0)]
    >>> chain = Comparison(by_value_and_not_none, MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)).as_chain()
    >>> chain.split_by_pareto(values)
    [[(2, 2, 2)], [(1, 0, 0), (0, 1, 1)], [(0, 1, 0), (None, 1, 1), (0, 0, 1)], [(None, 0, 1)], [(0, 0, 0)], [(0, None, None)]]

Here one extra None means that the whole row is inferior:

    >>> values = [(0,None,None), (2,2,2), (0,1,1), (0,0,1), (None,0,1), (0,1,0), (None,1,1), (1,0,0), (0,0,0)]
    >>> chain =  Comparison(by_none, MaxMinList(MaxMin.MIN, MaxMin.MIN, MaxMin.MIN)).and_then(
    ...    Comparison(by_value_and_not_none, MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)))
    >>> chain.split_by_pareto(values)
    [[(2, 2, 2)], [(1, 0, 0), (0, 1, 1)], [(0, 1, 0), (0, 0, 1)], [(None, 1, 1)], [(None, 0, 1)], [(0, 0, 0)], [(0, None, None)]]
