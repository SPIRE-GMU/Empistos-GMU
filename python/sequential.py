import layers
import json

class Sequential:
    def __init__(self, layers=None):
        self._layers = []
        self._has_input = False

        if layers is not None:
            if isinstance(layers, list):
                for l in layers:
                    self.add(l)
            else:
                raise TypeError("layers argument must be a list of Layer subclass objects")

    def add(self, layer, index: int = None):
        # Type Check
        if not issubclass(type(layer), (layers.Layer, layers.Input)):
            raise TypeError("layer is not a Layer subclass instance or Input")

        if self._has_input and isinstance(layer, layers.Input):
            raise TypeError("There can only be one input layer")
        
        # Point of insertion on stack
        index = index or len(self._layers)

        # If first layer is not Input throw an error
        if index == 0:
            if not isinstance(layer, layers.Input):
                raise TypeError("first layer must be an Input layer")
            else:
                self._has_input = True
        else:
            if isinstance(layer, layers.Input):
                raise TypeError("Input layer must be first")

        self._layers.insert(index, layer)

    def pop(self, index: int = None) -> layers.Layer:
        index = index or len(self._layers)
        try:
            layer = self._layers.pop(index)

            if isinstance(layer, layers.Input):
                self._has_input = False

        except IndexError:
            raise TypeError("no layers in model or index out of bounds")
        
    def json(self) -> list:
        return self._layers
    
    def savemodel(self, filename):
        with open(filename, "w") as f:
            json.dump(self, f, indent=4, default=lambda x: x.json())