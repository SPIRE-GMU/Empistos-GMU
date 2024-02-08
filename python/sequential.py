import layers
import os
import json

class Sequential:
    def __init__(self, layers=None):
        self._layers = []

        if layers is not None:
            if isinstance(layers, list):
                for l in layers:
                    self.add(l)
            else:
                raise TypeError("layers argument must be a list of Layer subclass objects")        

    def add(self, layer, index: int = None):
        if issubclass(type(layer), layers.Layer):
            self._layers.append(layer) if index is None else self._layers.insert(index, layer)
        else:
            raise TypeError("layer is not a Layer subclass instance")
        
    def pop(self, index: int = None):
        try:
            self._layers.pop(index if index is not None else len(self._layers))
        except IndexError:
            raise TypeError("no layers in model or index out of bounds")

    def tojson(self):
        result = []
        for layer in self._layers:
            result.append(layer.tojson())
        return json.dumps(result, indent = 3)
    
    def __str__(self):
        return json.loads(self.tojson())
    
    def labels(self, labels: list[str]):
        self._labels = labels
        if len(labels) != self._layers[-2]._groups:
            raise ValueError("number of labels doesn't match output of network")
        
    def loadlabels(self, name: str):
        with open(name, 'r') as f:
            labels = [line.strip() for line in f]
        return labels
        
    
    def savemodel(self, name: str = "network", results: int = 3):
        # if not name.endswith(".cfg"):
        #     name = f"{name}.cfg"
        with open(f"{name}.json", 'w') as f:
            f.write(self.tojson())
        with open(f"{name}.dataset", 'w') as f:
            f.write(f'classes = {self._layers[-2]._groups}\n')
            f.write(f"train = train_{name}.list\n")
            f.write(f'valid = test_{name}.list\n')
            f.write(f'labels = labels_{name}.list\n')
            f.write(f'names = names_{name}.list\n')
            f.write(f'backup = models/{name}\n')
            f.write(f'top = {results}\n')

    
    
    @staticmethod
    def __getlayertype(layer: layers.Layer):
        match layer:
            case "[net]":
                return layers.Input
            case "[connected]":
                return layers.Dense
            case "[maxpool]":
                return layers.MaxPooling2D
            case "[convolutional]":
                return layers.Conv2D
            case "[dropout]":
                return layers.Dropout
            case "[softmax]":
                return layers.Softmax
            case "[cost]":
                return layers.Cost
            case "[avgpool]":
                return layers.AveragePooling2D

    @staticmethod        
    def __formatarguments(arguments: dict):
        if 'batch' in arguments:
            arguments['batch_size'] = arguments['batch']
            arguments.pop('batch')
        if 'height' in arguments:
            if 'shape' not in arguments:
                arguments['shape'] = [arguments['height']]
            else:
                arguments['shape'].insert(0, arguments['height'])
            arguments.pop('height')
        if 'width' in arguments:
            if 'shape' in arguments:
                arguments['shape'].append(arguments['width'])
            else:
                arguments['shape'] = [arguments['width']]
            arguments.pop('width')
        if 'output' in arguments:
            arguments['units'] = arguments['output']
            arguments.pop('output')
        return arguments

    @staticmethod
    def __parseargument(argument):
        try:
            return int(argument) if '.' not in argument else float(argument)
        except ValueError:
            return argument

    @staticmethod
    def loadmodel(model: str):
        layers = []
        with open(model, 'r') as f:
            line = f.readline()
            while True:
                if line.startswith('[') and line.endswith(']\n'):
                    layertype = Sequential.__getlayertype((line[:-1]))
                    line = f.readline()
                    arguments = {}
                    while line and not line.startswith('['):
                        if line == '\n':
                            line = f.readline()
                            continue
                        arg = line.split('=')
                        arguments[arg[0].strip()] = Sequential.__parseargument(arg[1].strip())
                        line = f.readline()
                    arguments = Sequential.__formatarguments(arguments)
                    layers.append(layertype(**arguments))
                if not line: break
        return Sequential(layers)        