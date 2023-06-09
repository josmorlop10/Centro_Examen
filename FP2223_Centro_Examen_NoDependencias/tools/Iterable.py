'''
Created on 15 jul. 2020

@author: migueltoro
'''
from typing import Iterable, Iterator, TypeVar, Callable, Optional
import random
from tools.File import lineas_de_fichero
from collections import Counter
from tools.Functions import optional_get

K = TypeVar('K')
V = TypeVar('V')
E = TypeVar('E')
R = TypeVar('R')

identity = lambda x:x

def aleatorios(n:int,a:int,b:int) -> Iterable[int]:
    for _ in range(n):
        yield random.randint(a,b)

def iterate(initial:E, operator:Callable[[E],E], predicate:Callable[[E],bool]=lambda _:True) -> Iterable[E]:
    e = initial
    while predicate(e):
        yield e
        e = operator(e)
        
def all_pairs(n:int,m:int,n0:int = 0, m0:int= 0)-> Iterable[tuple[int,int]]:
    for i in range(n0,n):
        for j in range(m0,m):
            yield (i,j)   

def distinct(iterable:Iterable[E])->Iterable[E]:
    seen:set[E] = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item 
            
def limit(iterable:Iterable[E],limit:int) -> Iterable[E]:
    i = 0
    for e in iterable:
        if i < limit:
            yield e
            i = i +1
        else:
            break
        
def count_if(iterable:Iterable[E],predicate:Callable[[E],bool]=lambda _:True)->int:
    n = 0
    for e in iterable:
        if predicate(e):
            n = n+1
    return n

def first(iterable:Iterable[E], p:Callable[[E],bool]=lambda _:True) -> Optional[E]:
    r:Optional[E] = None
    for e in iterable:
        if p(e):
            r = e
            break
    return r

def first_and_rest(iterable:Iterable[E]) -> Optional[tuple[E,Iterable[E]]]:
    it:Iterator[E] = iter(iterable)
    e:Optional[E] = next(it,None)
    if e is None:
        return None
    else:
        return (e,it)
    
def first_and_last(iterable:Iterable[E])->Optional[tuple[E,E]]:
    it = iter(iterable)
    first =  next(it, None)
    if first is None:
        return None
    else:
        last = first
        for last in it:
            pass
    return (first,last)

def first_index_true(iterable:Iterable[bool],default:int=-1)->int:
    for i,e in enumerate(iterable):
        if e:
            return i
    return default

def first_index_if(iterable:Iterable[E],predicate:Callable[[E],bool],default:int=-1)->int:
    for i,e in enumerate(iterable):
        if predicate(e):
            return i
    return default

def first_index_with_elem(iterable:Iterable[E],elem:E,default:int=-1)->int:
    for i,e in enumerate(iterable):
        if e == elem:
            return i
    return default
    
def flat_map(iterable:Iterable[E],key:Callable[[E],Iterable[R]]=identity) -> Iterable[R]:
    for e in iterable:
        for pe in key(e):
            yield pe
            
def enumerate_flat_map(iterable:enumerate[E],fm:Callable[[E],Iterable[R]]=identity) -> Iterable[tuple[int,R]]:
    for ln,lv in iterable:
        for r in fm(lv):
            yield (ln,r)
    
# def flat(e: E | Iterable[E]) -> Iterable[E]:
#     if isinstance(e,Iterable):
#         for x in e:
#             yield x 
#     else:
#         yield e
  
def strfiter(iterable:Iterable[E],sep:str=',',prefix:str='{',suffix:str='}',
             key:Callable[[E],str]=str)->str:
    r:str = sep.join(key(x) for x in iterable)
    return f"{prefix}{r}{suffix}"


def grouping_reduce(iterable:Iterable[E],key:Callable[[E],K], 
                    op:Callable[[V,V],V],value:Callable[[E],V]= identity) -> dict[K, V]:
    a:dict[K,V] = {}
    for e in iterable:
        k = key(e)
        if k in a:
            a[k] = op(a[k],value(e))
        else:
            a[k] = value(e)
    return a


def grouping_list(iterable:Iterable[E],key:Callable[[E],K],value:Callable[[E],V]=identity) -> dict[K,list[V]]:
    return grouping_reduce(iterable,key,lambda x,y:x+y,lambda x: [value(x)])

def grouping_set(iterable:Iterable[E],key:Callable[[E],K],value:Callable[[E],V]=identity) -> dict[K,set[V]]:
    return grouping_reduce(iterable,key,lambda x,y:x|y,lambda x: {value(x)}) 

# similar a Counter
def groups_size(iterable:Iterable[E],key:Callable[[E],K]=identity,value:Callable[[E],int]=lambda _:1) -> dict[K,int]:
    return grouping_reduce(iterable,key,op=lambda x,y:x+y,value=value)

if __name__ == '__main__':
    print(strfiter(range(0,100)))
    r: Iterable[int] = flat_map([[0,1],[2,3,4],[5,6],[9]],lambda x:x)
    print(strfiter(r))
    print(strfiter(range(2,100,5)))
#    print(first_index_true((x%29==0 for x in aleatorios(10,1000,50))))
    print(strfiter(lineas_de_fichero('../../../resources/datos.txt')))
    print(first_index_if((int(e) for e in lineas_de_fichero('../../../resources/datos.txt')),lambda x: x==7))
    print(first_and_last(range(3,500,29)))
    print(list(zip([1,2,3,5],[6,7,8,9,10],[11,12,13,14,15]))) 
    sm:Callable[[int,int],int] = lambda x,y:x+y
    g = grouping_reduce(range(0,10,2),key = lambda x: x%3,op=sm, value= lambda x:x)
    print(g[0])   
    cp = Counter(['a', 'b', 'c', 'a', 'b', 'b'])
    print(cp.most_common(1)[0][1])
    r = ((1, 2, 3, 4)*2)[-2:-1]
    print(r)   
    print(','.join(str(p) for p in all_pairs(3,4)))
    print(len(range(10,3000,7)))
    e,it = optional_get(first_and_rest(range(10,3000,7)))
    print(e)
    print(list(it))
    it2:Iterable[int] = (x for x in range(10,3000,7))
    e = optional_get(first(it2))
    print(f"first = {e}, iterable = {list(it2)}")
    it4:Iterable[int] = (x for x in range(10,3000,7))
    e2:tuple[int,Iterable[int]] = optional_get(first_and_rest(it4))
    print(f"first = {e2[0]}, rest = {list(e2[1])}")
    print(first_and_last((x for x in range(10,3000,7))))
    it = range(10,3000,7)
    
    
    