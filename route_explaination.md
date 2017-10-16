# Replacement of `Include`

## Introduction

We can mimic the same pattern as `SubCommand` and create class structures for sub-routes. These classes will
provide the same interface as `Include`, but with the ability to be extended/overridden during instantiation

In the examples below, I will demonstrate how someone would build an equivalent route structure in the
current `Include` pattern, a new SubRoute pattern, and a potential future feature of ViewSet
(or view classes?).

This document assumes you've already read the `SubCommand` RFC.

---

## Implementation

### Current Pattern

This is a pretty simple sub-route that includes the ability to list, create, and get "dogs".

```python
dog0 = [
    Route('/', 'GET', list_dogs),
    Route('/{pk}', 'GET', list_dogs),
    Route('/', 'POST', create_dogs),
]
App(routes=[Include('/dogs', dog0)])
```

### SubRoute

The SubRoute class is very similar to the `SubCommand` implementation where it expects that you provide it
with a few properties. These include `path`, `routes`, and `name`. `path` and `routes` are required while
`name` is for the ability to use this route class more than once.

```python
class Dog1Routes(SubRoute):
    """ Dog 1.0 Management Routes

    This is some documentation going over dog endpoints.
    """
    path = '/dogs' # This could be automatically created off of the prefix of the class name
    routes = [
        Route('/', 'GET', list_dogs),
        Route('/{pk}', 'GET', list_dogs),
        Route('/', 'POST', create_dogs),
    ]
    name = 'dogs' # This could be automatically created off of the prefix of the class name

App(routes=[
    Dog1Routes(),
    Dog1Routes(path='/dog3', name='dog_three'),
])
```

### Future ViewSets?

I don't personally know the current standings of the ViewSet pattern or if there are any plans to bring it
to api star.

I could imagine a base ViewSet being part of the starapi library that provided the same functionality as DRF. This Viewset would need a way to provide its generic methods(`list`, `get`, ... `destroy`) as a list
of routes.

Below I define `ViewSet` which would be extended from `SubRoute`. This `ViewSet(SubRoute)` would build its
own `routes` list property by checking which methods where defined.

```python

class ViewSet(SubRoute):

    @property
    def routes(self):
        return [
            # generate a list of Routes based on which methods are implemented.
            Route(f'/', 'GET', self.list),
            Route(f'/{pk}', 'GET', self.get),
            Route(f'/', 'POST', self.create),
        ]
```

Using this new `ViewSet` class would be as easy as creating a new class that extended from it and implementing
a few ViewSet methods. Then adding it to a RouteConfig list would be as easy as instantiating the class.

```python
class Dog2ViewSet(ViewSet):
    """ Dog 2.0 management routes via ViewSet (equivalent to the first line of the SubRoute doc string)

    This implementation provides the same route structure, but the SubRoute is
    built into the ViewSet. (equivalent to the extended documentation lines of the SubRoute doc string)
    """

    def list(self) -> typesystem.List[Dog]:
        """ Retrieve Dogs

        Some extended documentation about retrieving dogs
        """
        return [Dog(), Dog()]

    def get(self, pk: str) -> Dog:
        return Dog()

    def create(self) -> Dog:
        dog = Dog(**POST_DATA)

        dog.save()

        return dog


App(routes=[
    Dog2ViewSet(),
    Dog2ViewSet(path='/dog4', name='dog_four'),
])
```
