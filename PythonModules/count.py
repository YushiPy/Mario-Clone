
from typing import Callable, Sequence, TypeVar, Any

T = TypeVar('T')
_T = TypeVar('_T')

class Count:

    def __init__(self) -> None:
        
        self.counter: dict = {}

        self.events: list[Event] = []
        self.ordered_events: list[Event] = []


    def count(self, value: int, key: Any | None = None) -> bool:

        self.counter[key] = self.counter.get(key, 0) + 1
        
        if self.counter[key] >= value:
            self.counter[key] %= value
            return True
        
        return False

    
    def check_events(self) -> list[Any]:

        return [(self.events.pop if a.times == 0 else self.events.__getitem__)(i).call() 
                for i, a in enumerate(self.events) if self.count(a.value, a.key)]
    

    def check_ordered(self) -> list[Any]:

        if not self.ordered_events: return []

        event = self.ordered_events[0]

        if not event.count(): return []

        return [(self.ordered_events.pop(0) if event.times else event).call()] + self.check_ordered()
    

    
    def reset(self, __value: int | None = None, __key: Any | None = None) -> None:
 
        if not __key in self.count: return

        if __value is None: self.count[__key].clear() 
        else: self.count[__key][__value] = 0
        

    def __call__(self, __value: int, __key: Any | None = None) -> bool:
        return self.count(__value, __key)


    def __str__(self) -> str:
        return ', '.join(f'{a}={b}' for a, b in self.__dict__.items())


class Event:
    def __init__(self, function: Callable[[...], T], args: Sequence[_T] = [], 
                 value: int = 1, times: int = 1, key: Any | None = None) -> None:
        
        self.function = function
        self.args = args
        self.value = value
        self.__times = times

        self.key = function if key is None else key
        
        self.__count = 0


    def count(self) -> _T:
        
        self.__count += 1

        if self.__count >= self.value and self.times != 0:
            return self.call()


    @property
    def times(self) -> int:
        self.__times -= 1

        return self.__times


    def call(self) -> T:
        return self.function(*self.args)


    def __repr__(self) -> str:
        return ', '.join(f'{a}={b}' for a, b in self.__dict__.items() if a not in {'function', 'key'})

