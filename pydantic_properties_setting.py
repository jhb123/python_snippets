"""
For some reason, you might want to have a pydantic model update a
property when you change another one. If you deprecate a field,
you may want to automatically update another field if you have
a complex dependency problem that you want to half fix.
"""
import json
from typing import List, Optional

from pydantic import BaseModel, Field
    

class ExampleModel(BaseModel):
    a: Optional[int] = Field(default=None, deprecate=True)
    b: Optional[int] = Field(default=None, deprecate=True)

    all: List[int]  = Field(default=[])

    def __setattr__(self, name, value):
        if name == 'a':
            self.all.append(value)
        if name == 'b':
            self.all.append(value)
        super().__setattr__(name, value)
    

if __name__ == "__main__":
    print(json.dumps(ExampleModel.model_json_schema(),indent=2))
    foo = ExampleModel(a=2)
    print(foo)
    foo.a = 1
    foo.b = 3
    print(foo)
