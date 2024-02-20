"""
I would avoid relying on the behaviour of serialising 
tuples to json and deserialising them back into python
objects with pydantic. In the following example, 
c3 != c4. c4.messages has the type List[ThingA] instead
of List[ThingB]. This is a trivial example, but it can
cause problems if you have lots of inheritance and 
complex schemas.
"""
import json
from typing import List
from pydantic import BaseModel

class ThingA(BaseModel):
    messages: List[List[str]] | None = None
    
class ThingB(BaseModel):
    messages: List[tuple[str, str, str]] | None = None

class ThingCollection(BaseModel):
    data: List[ThingA| ThingB] | None = None

if __name__ == "__main__":
    a = ThingA(messages=[["a","a","a"],["a","a","a"],["a","a","a"]])
    c1 = ThingCollection(
        data=[a,a,a]
    )
    data_a = c1.model_dump_json()
    data_a = json.loads(data_a)
    c2 = ThingCollection(**data_a)

    assert  c1 == c2

    b = ThingB(messages=[("b","b","b"),("b","b","b"),("b","b","b")])

    c3 = ThingCollection(
        data=[b,b,b]
    )
    data_b = c3.model_dump_json()
    data_b = json.loads(data_b)
    c4 = ThingCollection(**data_b)

    assert  c3 == c4

    