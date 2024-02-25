import layers as lay
import os
import json

class Sequential:
    def __init__(self, name: str = "network", layers: list[lay.Layer] = None):
        self._layers = []
        self.name = name
        self._split = (False, 0)

        if layers is not None:
            if isinstance(layers, list):
                for index, layer in enumerate(layers):
                    self.add(layer)
                    if isinstance(layer, lay.Split):
                        if isinstance(layers[index - 1], (lay.Dropout, lay.Cost)): raise IndexError("Can't Split after Dropout or Cost Layer")
                        self._split = (True, index)
                        layer.previouslayer = layers[index - 1]
            else:
                raise TypeError("layers argument must be a list of Layer subclass objects")        

    def add(self, layer: lay.Layer, index: int = None):
        if index is None: index = len(self._layers)
        if issubclass(type(layer), lay.Layer):
            if isinstance(layer, lay.Split):
                if isinstance(self._layers[index - 1], (lay.Dropout, lay.Cost)): raise IndexError("Can't Split after Dropout or Cost Layer")
                self._split = (True, index)
            self._layers.insert(index, layer)
        else:
            raise TypeError("layer is not a Layer subclass instance")
        
    def pop(self, index: int = None):
        try:
            layer = self._layers.pop(index if index is not None else len(self._layers) - 1)
            if isinstance(layer, lay.Split):
                self._split = (False, 0)
        except IndexError:
            raise TypeError("no layers in model or index out of bounds")

    def __tojson(self, layers: list[lay.Layer]) -> list:
        result = []
        for layer in layers:
            result.append(layer.tojson())
        return result
    
    def __str__(self):
        return json.dumps(self.__tojson(self._layers), indent = 3)
    
    def labels(self, labels: list[str]):
        self._labels = labels
        if len(labels) != self._layers[-2]._groups:
            raise ValueError("number of labels doesn't match output of network")
        
    def loadlabels(self, name: str):
        with open(name, 'r') as f:
            labels = [line.strip() for line in f]
        return labels
        
    
    def savemodel(self, name: str = "network"):
        split, index = self._split
        if split:
            clients = self._layers[index].clients
            server = self._layers[:index + 1]
            for count, client in enumerate(clients):
                with open(f'{name}{count + 1}.json', 'w') as f:
                    self._layers[index].clients = client
                    f.write(json.dumps(self.__tojson(self._layers[index:]), indent = 3))
            server[index].send = True
            server[index].clients = clients
            with open(f"{name}.json", 'w') as f:
                f.write(json.dumps(self.__tojson(server), indent = 3))
        with open(f'{name}' + '_master.json' if split else '.json', 'w') as f:
            f.write(json.dumps(self.__tojson(self._layers), indent = 3))
        
    # def savemetadata(self, name: str = "network", datapath = 'data/', results: int = 3):
    #     dictionary = {}
    #     dictionary['classes'] = self._layers[-2]._groups
    #     dictionary['train'] = f'{datapath}train_{name}.json'
    #     dictionary['valid'] = f'{datapath}test_{name}.json'
    #     dictionary['labels'] = f'{datapath}labels_{name}.json'
    #     dictionary['names'] = f'{datapath}names_{name}.json'
    #     dictionary['backup'] = f'models/{name}'
    #     dictionary['top'] = results

    #     with open(f"{name}_metadata.json", 'w') as f:
    #         f.write(json.dumps(dictionary, indent = 3))

    def makelabels(self, name: str = "network", labels: list = None):
        with open(f"{name}_labels.list", 'w') as f:
            for label in labels:
                f.write(f'{label}\n')

    def makenames(self, name: str = "network", names: list = None):
        with open(f"names_{name}.list", 'w') as f:
            for n in names:
                f.write(f'{n}\n')

    def savemetadata(self, name: str = "network", datapath: str = 'data/', results: int = 3):
        with open(f"{name}.dataset", 'w') as f:
            f.write(f'classes = {self._layers[-2]._groups}\n')
            f.write(f"train = {datapath + name}_train.list\n")
            f.write(f'valid = {datapath + name}_test.list\n')
            f.write(f'labels = {datapath + name}labels.list\n')
            f.write(f'names = {datapath + name}names.list\n')
            f.write(f'backup = {datapath}models/{name}\n')
            f.write(f'top = {results}\n')
            
    @staticmethod
    def __getlayertype(layer: str):
        match layer:
            case "net":
                return lay.Input
            case "connected":
                return lay.Dense
            case "maxpool":
                return lay.MaxPooling2D
            case "convolutional":
                return lay.Conv2D
            case "dropout":
                return lay.Dropout
            case "softmax":
                return lay.Softmax
            case "cost":
                return lay.Cost
            case "avgpool":
                return lay.AveragePooling2D

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
            arguments = json.load(f)
            for layer in arguments:
                layertype = Sequential.__getlayertype(layer['layer'])
                layer.pop('layer')
                layer = Sequential.__formatarguments(layer)
                layers.append(layertype(**layer))
        return Sequential(layers = layers)        