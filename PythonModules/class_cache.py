
from typing import Callable, Hashable, TypeVar, Sequence, Any

T = TypeVar('T')
_T = TypeVar('_T')

__original_functions: dict[Callable, Callable] = {}

def cache_property(fget: Callable[[Any], Any] | None = None, fset: Callable[[Any, Any], None] | None = None,
                   fdel: Callable[[Any], None] = None, doc: str | None = None) -> property:
    
    prop = property(fget=fget, fset=fset, fdel=fdel, doc=doc)
    
    __original_functions[fget, fset, fdel, doc] = prop
    
    return prop


def class_cache(function: Callable[..., _T]) -> Callable[..., _T]:
    
    def wrapper(instace: object, *args: Hashable, **kwargs: Hashable) -> _T:
        
        hash_kwargs = tuple((a, b) for a, b in kwargs.items())
        
        if '__cache' not in instace.__dict__:
            instace.__cache: dict[Callable[..., _T], dict[Hashable, dict[Hashable, _T]]] = {}
        
        if function not in instace.__cache:
            instace.__cache[function] = {}
            
        if args not in instace.__cache[function]:
            instace.__cache[function][args] = {}
            
        if hash_kwargs not in instace.__cache[function][args]:
            instace.__cache[function][args][hash_kwargs] = function(instace, *args, **kwargs)
            
        return instace.__cache[function][args][hash_kwargs]

    __original_functions[wrapper] = function

    return wrapper


def cache_breaker(breaking_functions: Sequence[Callable[..., Any]] | None = None, 
                  *breaking_args: Hashable, **breaking_kwargs: Hashable) -> Callable[[T], _T]:
    
    breaking_kwargs = tuple((a, b) for a, b in breaking_kwargs.items())
    
    
    if breaking_functions is not None: breaking_functions = [__original_functions[i] for i in breaking_functions]
    else: breaking_functions = [None]
    
    def decorator(function: Callable[[T], _T]) -> Callable[[T], _T]:
        
        def wrapper(instace: object, *args: Hashable, **kwargs: Hashable) -> None:
            
            if '__cache' not in instace.__dict__: 
                return function(instace, *args, **kwargs)
            
            for breaking_function in breaking_functions:

                dictionary: dict = instace.__cache

                if breaking_function is not None: dictionary = dictionary[breaking_function]
                if breaking_args: dictionary = dictionary[breaking_args]
                
                if breaking_kwargs: dictionary.pop(breaking_kwargs)
                else: dictionary.clear()
                
            
            return function(instace, *args, **kwargs)
            
        return wrapper
        
    return decorator

