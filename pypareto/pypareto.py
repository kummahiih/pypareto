"""
Copyright 2020 Pauli Henrikki Rikula

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from typing import List
from enum import Enum, auto
import abc
from collections import defaultdict, Counter

class MaxMin(Enum):
    MAX = 1
    MIN = 2
    SKIP = 3

    def __repr__(self) -> str:
        return self.name

class MaxMinList:
    def __init__(self, *target_list: List[MaxMin], none_is_good=False):
        """
        >>> MaxMinList(MaxMin.MAX, MaxMin.MIN)
        MaxMinList[MAX ,MIN]
        """
        self._target_list = target_list
        self._dim = len(target_list)
        self._none_is_good = none_is_good

    def __repr__(self) -> str:
        return "MaxMinList[{}]".format(" ,".join([i.__repr__() for i in self._target_list]))
    
    @property
    def dim(self) -> int: return self._dim

    @property
    def list(self) -> List[MaxMin]:
        return self._target_list
    
    @property
    def none_is_good(self):
        return self._none_is_good

class Domination(Enum):
    GREATER = 1
    EQUAL = 0
    LESS = -1
    
    def __repr__(self) -> str:
        return self.name


def by_none(a, b) -> Domination:
    """
    >>> by_none(None, 1)
    GREATER
    >>> by_none(1, None)
    LESS
    >>> by_none(None, None)
    EQUAL
    >>> by_none(1, 1)
    EQUAL
    
    """
    if a is None and b is not None:
        return Domination.GREATER
    if b is None and a is not None:
        return Domination.LESS
    return  Domination.EQUAL

def by_value(a, b) -> Domination:
    """
    >>> by_value(2, 1)
    GREATER
    >>> by_value(1, 2)
    LESS
    >>> by_value(2, 2)
    EQUAL
    >>> by_value(1, 1)
    EQUAL
    
    """
    if a > b:
        return Domination.GREATER
    if a < b:
        return Domination.LESS
    return  Domination.EQUAL

def cmp_to_target(a, b, cmp, target: MaxMin, none_is_good) -> Domination:
    """
    >>> cmp_to_target(2, 1, by_value, MaxMin.MAX, False)
    GREATER
    >>> cmp_to_target(1, 2, by_value, MaxMin.MAX, False)
    LESS
    >>> cmp_to_target(2, 2, by_value, MaxMin.MAX, False)
    EQUAL
    >>> cmp_to_target(1, 1, by_value, MaxMin.MAX, False)
    EQUAL
    >>> cmp_to_target(2, 1, by_value, MaxMin.MIN, False)
    LESS
    >>> cmp_to_target(1, 2, by_value, MaxMin.MIN, False)
    GREATER
    >>> cmp_to_target(2, 2, by_value, MaxMin.MIN, False)
    EQUAL
    >>> cmp_to_target(1, 2, by_value, MaxMin.SKIP, False)
    EQUAL
    >>> cmp_to_target(None, 1, by_value, MaxMin.MIN, False)
    LESS
    >>> cmp_to_target(1, None, by_value, MaxMin.MIN, False)
    GREATER
    >>> cmp_to_target(None, None, by_value, MaxMin.MIN, False)
    EQUAL
    >>> cmp_to_target(None, 1, by_none, MaxMin.MAX, False)
    LESS
    >>> cmp_to_target(1, None, by_none, MaxMin.MAX, False)
    GREATER
    >>> cmp_to_target(None, None, by_none, MaxMin.MAX, False)
    EQUAL

    """
    if target is MaxMin.SKIP:
        return Domination.EQUAL
    if a is None and b is not None:
        return Domination.LESS if not none_is_good else Domination.GREATER
    if a is not None and b is None:
        return Domination.GREATER if not none_is_good else Domination.LESS
   
    if a is None and b is None:
        return Domination.EQUAL

    cmp_result = cmp(a ,b)
    if target is MaxMin.MAX:
        return cmp_result
    else:
        if cmp_result is Domination.LESS:
            return Domination.GREATER
        elif cmp_result is Domination.GREATER:
            return Domination.LESS
        else:
            return Domination.EQUAL

def dominates(a: list, b: list, cmp, targets: MaxMinList) -> Domination:
    """
    >>> a = [None]
    >>> b = [1]
    >>> target = MaxMinList(MaxMin.MIN)
    >>> dominates(a, a, by_none, target)
    EQUAL
    >>> dominates(a, b, by_none, target)
    LESS
    >>> dominates(b, a, by_none, target)
    GREATER
    >>> dominates(b, b, by_none, target)
    EQUAL
    >>> a = [1, None]
    >>> b = [1, 1]
    >>> target = MaxMinList(MaxMin.MIN, MaxMin.MIN)
    >>> dominates(a, a, by_none, target)
    EQUAL
    >>> dominates(a, b, by_none, target)
    LESS
    >>> dominates(b, a, by_none, target)
    GREATER
    >>> dominates(b, b, by_none, target)
    EQUAL
    >>> dominates([1, None], [None, 1], by_none, target)
    EQUAL
    >>> a = [2, 1]
    >>> b = [2, 2]
    >>> target = MaxMinList(MaxMin.MAX, MaxMin.MAX)
    >>> dominates(a, a, by_value, target)
    EQUAL
    >>> dominates(a, b, by_value, target)
    LESS
    >>> dominates(b, a, by_value, target)
    GREATER
    >>> dominates(b, b, by_value, target)
    EQUAL
    >>> dominates([1, 0], [0, 1], by_value, target)
    EQUAL
    >>> dominates((None, 0, 1), (0, 0, 0), by_value, MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX, none_is_good=False))
    EQUAL
    

    """
    results = list()
    for d in range(targets.dim):
        results.append(cmp_to_target(a[d], b[d], cmp, targets.list[d], targets.none_is_good))
    
    is_greater_in_any = False
    for r in results:
        if r is Domination.GREATER:
            is_greater_in_any = True
            break

    is_less_in_any = False
    for r in results:
        if r is Domination.LESS:
            is_less_in_any = True
            break

    if is_greater_in_any and not is_less_in_any:
        return Domination.GREATER
    if is_less_in_any and not is_greater_in_any:
        return Domination.LESS
    return Domination.EQUAL


class DominanceMatrix:
    """
    Dominance matrix used in the fast non dominated search from:

    Verma G., Kumar A., Mishra K.K. (2011) A Novel Non-dominated Sorting Algorithm. 
    In: Panigrahi B.K., Suganthan P.N., Das S., Satapathy S.C. (eds) Swarm, Evolutionary, and Memetic Computing. 
    SEMCCO 2011. Lecture Notes in Computer Science, vol 7076. Springer, Berlin, Heidelberg
    

    >>> targets = MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)
    >>> dominates = Comparison(by_value, targets).compare
    >>> values = [(2,2,2), (0,1,1), (0,0,1), (0,1,0), (1,0,0), (0,0,0)]
    >>> for front in DominanceMatrix(values, dominates).get_pareto_fronts():
    ...   print(front)
    [(2, 2, 2)]
    [(0, 1, 1), (1, 0, 0)]
    [(0, 0, 1), (0, 1, 0)]
    [(0, 0, 0)]
    
    
    >>> values = [(1,0,0), (None,1,1), (None,0,1), (0,0,0)]
    >>> for front in DominanceMatrix(values, dominates).get_pareto_fronts():
    ...   print(front)
    [(1, 0, 0), (None, 1, 1)]
    [(None, 0, 1), (0, 0, 0)]

    """
    def __init__(self, values, dominates):
        dimension = len(values)
        self.is_dominating = defaultdict(list)
        self.dominated_by_counter = defaultdict(int)
        self.values = list(values)

        for i in range(dimension):
            for j in range(i + 1, dimension):
                a = values[i]
                b = values[j]
                rel = dominates(a, b)
                if rel == Domination.GREATER:
                    self.is_dominating[a].append(b)
                    self.dominated_by_counter[b] += 1
                elif rel == Domination.LESS:
                    self.is_dominating[b].append(a)
                    self.dominated_by_counter[a] += 1

    def get_pareto_fronts(self):
        while self.values:
            current_front = [ v for v in self.values if self.dominated_by_counter[v] == 0]
            yield current_front

            for v in current_front:
                for dominated in self.is_dominating[v]:
                    self.dominated_by_counter[dominated] -= 1

                self.values.remove(v)
                try:
                    del self.is_dominating[v]
                except KeyError:
                    pass
                try:
                    del self.dominated_by_counter[v]
                except KeyError:
                    pass


class Cmp(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def compare(self, a, b) -> Domination:
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def is_pareto(self) -> bool:
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def is_group(self) -> bool:
        raise NotImplementedError

    @abc.abstractclassmethod
    def group(self, a) -> int:
        raise NotImplementedError

class GroupNones(Cmp):
    def __init__(self, targets: MaxMinList):
        self._targets = targets
    @property
    def targets(self):
        return self._targets
    def compare(self, a, b) -> Domination:
        raise NotImplementedError
    def is_pareto(self) -> bool:
        return False
    def is_group(self) -> bool:
        return True

    def group(self, a) -> int:
        """
        GroupNones(MaxMinList(MaxMin.MIN, MaxMin.MIN, MaxMin.MIN)).group((0,None,None))
        -2
        """
        noneSum = 0
        for d in range(self.targets.dim):
            if self.targets.list[d] is MaxMin.SKIP:
                continue
            if self.targets.list[d] is MaxMin.MAX and a[d] is None:
                noneSum += 1
            if self.targets.list[d] is MaxMin.MIN and a[d] is None:
                noneSum -= 1
        return noneSum
    
    def and_then(self, c: Cmp) -> Cmp:
        return ComparisonChain(self, c)
    
    def as_chain(self):
        return ComparisonChain(self)


class Comparison(Cmp):
    def __init__(self, cmp, targets: MaxMinList):
        self._cmp = cmp
        self._targets = targets
    
    def is_pareto(self) -> bool: return True
    def is_group(self) -> bool: return False
    def group(self, a) -> int: return 1

    @property
    def cmp(self):
        return self._cmp

    @property
    def targets(self):
        return self._targets

    def compare(self, a,b) -> Domination:
        return dominates(a, b, self.cmp, self.targets)

    def and_then(self, c: Cmp) -> Cmp:
        return ComparisonChain(self, c)
    
    def as_chain(self):
        return ComparisonChain(self)

class ComparisonChain:
    def __init__(self, *chain: List[Comparison]):
        self._chain = chain

    @property
    def chain(self) -> List[Comparison]:
        return self._chain

    def compare(self, a, b) -> Domination:
        for c in self.chain[:-1]:
            if not c.is_pareto():
                continue
            result = c.compare(a, b)
            if result == Domination.EQUAL:
                continue
            return result
        return self.chain[-1].compare(a, b)
    
    def and_then(self, c: Cmp) -> Cmp:
        return ComparisonChain(self, *self.chain, c)

    
    def split_by_pareto(self, values):
        """ComparisonChain.split_by_pareto performs the pareto front split fronts.

Currently this works only for unique rows. You can add id as the last row (and not sort by it) to work around this restriction.

Here the None means just inferior value:

    >>> values = [(0,None,None), (2,2,2), (0,1,1), (0,0,1), (None,0,1), (0,1,0), (None,1,1), (1,0,0), (0,0,0)]
    >>> chain = Comparison(by_value, MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)).as_chain()
    >>> chain.split_by_pareto(values)
    [[(2, 2, 2)], [(0, 1, 1), (1, 0, 0)], [(0, 0, 1), (0, 1, 0), (None, 1, 1)], [(None, 0, 1), (0, 0, 0)], [(0, None, None)]]

Here one extra None means that the whole row is inferior:

    >>> values = [(0,None,None), (2,2,2), (0,1,1), (0,0,1), (None,0,1), (0,1,0), (None,1,1), (1,0,0), (0,0,0), (None, 0, None)]
    >>> chain = GroupNones(MaxMinList(MaxMin.MIN, MaxMin.MIN, MaxMin.MIN)).and_then(
    ...    Comparison(by_value, MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)))
    >>> chain.split_by_pareto(values)
    [[(2, 2, 2)], [(0, 1, 1), (1, 0, 0)], [(0, 0, 1), (0, 1, 0)], [(0, 0, 0)], [(None, 1, 1)], [(None, 0, 1)], [(0, None, None), (None, 0, None)]]

"""
        splitted = [values]
        for comparison in self.chain:
            if comparison.is_pareto():
                new_splitted = []
                while len(splitted) > 0:
                    group = splitted.pop(0)
                    new_groups = list(DominanceMatrix(group, comparison.compare).get_pareto_fronts())
                    new_splitted.extend(new_groups)
                splitted = new_splitted
            elif comparison.is_group():
                new_splitted = []
                while len(splitted) > 0:
                    group = splitted.pop(0)
                    group_dict = defaultdict(list)
                    for a in group:
                        group_dict[comparison.group(a)].append(a)
                    keys = list(group_dict.keys())
                    keys.sort()
                    keys.reverse()
                    new_groups = [group_dict[k] for k in keys]
                    
                    new_splitted.extend(new_groups)
                splitted = new_splitted
        return splitted

if __name__ == "__main__":
    import doctest
    doctest.testmod()