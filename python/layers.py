import activation as act
import costfunction as cost
import json

class Layer:
    # Base layer class
    def __init__(self, units = None, activation=act.Activation.RELU):
        self._activation = act.Activation(activation).value
        self._neurons = units

    def tojson(self) -> dict:
        result = {}
        if self._neurons is not None:
            result["output"] = self._neurons
        result["activation"] = self._activation
        return result
    
    # Print layer info
    def __str__(self):
        result = self.label + "\n"
        if self._neurons is not None: 
            result += "output=" + str(self._neurons) + "\n"
        result += "activation=" + self._activation + "\n"
        #return json.loads
        return result

# Net(?)
class Input(Layer):
    label = "[net]"
    def __init__(self, shape, batch_size, subdivisions = None, channels = None, momentum = None, decay = None, max_crop = None,
                 learning_rate = None, policy = None, power = None, max_batches = None, angle = None,
                 hue = None, saturation = None, exposure = None, aspect = None):
        if isinstance(shape, (tuple, list)) and len(shape) == 2:
            self._height = shape[0]
            self._width = shape[1]
        else:
            raise TypeError("shape must be a list or tuple of size 2")

        self._batch_size = batch_size
        self._subdivisions = subdivisions
        self._channels = channels
        self._momentum = momentum
        self._decay = decay
        self._max_crop = max_crop
        self._learning_rate = learning_rate
        self._policy = policy
        self._power = power
        self._max_batches = max_batches
        self._angle = angle
        self._hue = hue
        self._saturation = saturation
        self._exposure = exposure
        self._aspect = aspect

    def tojson(self) -> dict:
        result = {"layer": "net"}
        #result = self.label + "\n"
        result["batch"] = self._batch_size #result += "batch=" + str(self._batch_size) + "\n"
        if self._subdivisions is not None: result["subdivisions"] = self._subdivisions #result += "subdivisions=" + str(self._subdivisions) + "\n"
        result["height"] = self._height #result += "height=" + str(self._height) + "\n"
        result["width"] = self._width #result += "width=" + str(self._width) + "\n"
        if self._channels is not None: result["channels"] = self._channels #result += "channels=" + str(self._channels) + "\n"
        if self._momentum is not None: result["momentum"] = self._momentum #result += "momentum=" + str(self._momentum) + "\n"
        if self._decay is not None: result["decay"] = self._decay #result += "decay=" + str(self._decay) + "\n"
        if self._max_crop is not None: result["max_crop"] = self._max_crop #result += "max_crop=" + str(self._max_crop) + "\n"
        if self._learning_rate is not None: result["learning_rate"] = self._learning_rate #result += "learning_rate=" + str(self._learning_rate) + "\n"
        if self._policy is not None: result["policy"] = self._policy #result += "policy=" + str(self._policy) + "\n"
        if self._power is not None: result["power"] = self._power #result += "power=" + str(self._power) + "\n"
        if self._max_batches is not None: result["max_batches"] = self._max_batches #result += "max_batches=" + str(self._max_batches) + "\n"
        if self._angle is not None: result["angle"] = self._angle #result += "angle=" + str(self._angle) + "\n"
        if self._hue is not None: result["hue"] = self._hue #result += "hue=" + str(self._hue) + "\n"
        if self._saturation is not None: result["saturation"] = self._saturation #result += "saturation=" + str(self._saturation) + "\n"
        if self._exposure is not None: result["exposure"] = self._exposure #result += "exposure=" + str(self._exposure) + "\n"
        if self._aspect is not None: result["aspect"] = self._aspect #result += "aspect=" + str(self._aspect) + "\n"
        return result
    
    def __str__(self):
        result = self.label + "\n"
        result += "batch=" + str(self._batch_size) + "\n"
        if self._subdivisions is not None: result += "subdivisions=" + str(self._subdivisions) + "\n"
        result += "height=" + str(self._height) + "\n"
        result += "width=" + str(self._width) + "\n"
        if self._channels is not None: result += "channels=" + str(self._channels) + "\n"
        if self._momentum is not None: result += "momentum=" + str(self._momentum) + "\n"
        if self._decay is not None: result += "decay=" + str(self._decay) + "\n"
        if self._max_crop is not None: result += "max_crop=" + str(self._max_crop) + "\n"
        if self._learning_rate is not None: result += "learning_rate=" + str(self._learning_rate) + "\n"
        if self._policy is not None: result += "policy=" + str(self._policy) + "\n"
        if self._power is not None: result += "power=" + str(self._power) + "\n"
        if self._max_batches is not None: result += "max_batches=" + str(self._max_batches) + "\n"
        if self._angle is not None: result += "angle=" + str(self._angle) + "\n"
        if self._hue is not None: result += "hue=" + str(self._hue) + "\n"
        if self._saturation is not None: result += "saturation=" + str(self._saturation) + "\n"
        if self._exposure is not None: result += "exposure=" + str(self._exposure) + "\n"
        if self._aspect is not None: result += "aspect=" + str(self._aspect) + "\n"
        #return json.loads
        return result
        
#####################################################
# Layer-specific configuration is not complete yet! #
#####################################################

# Convolutional 
class Conv2D(Layer):
    """
    2D Convolutional Layer

    @param batch_normalize: Use batch normalization (Default: False)
    @param filters: Number of kernel filters (Default: 1)
    @param size: kernel size of filter (Default: 1)
    @param groups: Number of groups for grouped-convolutional (depth-wise) (Default: 1)
    @param stride: Stride (offset step) of kernel filter (Default: 1)
    @param padding: Size of padding (Default: 0)
    @param pad: If true, padding=size/2, if false, padding parameter value is used (Default: False)
    @param dilation: Size of dilation (Default: 1)
    @param activation: Activation function after convolution (Default: Logistic)
    """
    label = "[convolutional]"
    def __init__(self, batch_normalize=0, filters=1, size=1, groups=1, stride=1, padding=0, pad=False, dilation=1, activation=act.Activation.LOGISTIC):
        super().__init__(activation = activation)
        self._batch_normalize = batch_normalize
        self._filters = filters
        self._size = size
        self._groups = groups
        self._stride = stride
        self._padding = padding
        self._pad = 1 if pad else 0
        self._dilation = dilation
    
    def tojson(self) -> dict:
        # result = super().__str__()
        # result += "batch_normalize=" + str(self._batch_normalize) + "\n"
        # result += "filters=" + str(self._filters) + "\n"
        # result += "size=" + str(self._size) + "\n"
        # result += "groups=" + str(self._groups) + "\n"
        # result += "stride=" + str(self._stride) + "\n"
        # result += "padding=" + str(self._padding) + "\n"
        # result += "pad=" + str(self._pad) + "\n"
        # result += "dilation=" + str(self._dilation) + "\n"
        result = {"layer": "convolutional"}
        result.update(super().tojson())
        result["batch_normalize"] = self._batch_normalize
        result["filters"] = self._filters
        result["size"] = self._size
        result["groups"] = self._groups
        result["stride"] = self._stride
        result["padding"] = self._padding
        result["pad"] = self._pad
        result["dilation"] = self._dilation
        return result
    
    def __str__(self):
        result = super().__str__()
        result += "batch_normalize=" + str(self._batch_normalize) + "\n"
        result += "filters=" + str(self._filters) + "\n"
        result += "size=" + str(self._size) + "\n"
        result += "groups=" + str(self._groups) + "\n"
        result += "stride=" + str(self._stride) + "\n"
        result += "padding=" + str(self._padding) + "\n"
        result += "pad=" + str(self._pad) + "\n"
        result += "dilation=" + str(self._dilation) + "\n"
        return result
        #return json.loads(self.tojson(), indent = 3)

# Maxpool
class MaxPooling2D(Layer):
    label = "[maxpool]"

    def __init__(self, size = 1, stride = 1, padding = 0):
        self._size = size
        self._stride = stride
        self._padding = padding

    def tojson(self) -> dict:
        # result = f"{self.label}\n"
        # result += f"size={self._size}\n"
        # result += f"stride={self._stride}\n"
        return {"layer": "maxpool", "size": self._size, "stride": self._stride, "padding": self._padding}
    
    def __str__(self):
        result = f"{self.label}\n"
        result += f"size={self._size}\n"
        result += f"stride={self._stride}\n"
        return result

# Avgpool
class AveragePooling2D(Layer):
    label = "[avgpool]"

    def __init__(self, size = 1, stride = 1, padding = 0):
        self._size = size
        self._stride = stride
        self._padding = padding

    def __str__(self):
        result = f'{self.label}\n'
        result += f'size = {self._size}\n'
        result += f'stride = {self._stride}\n'
        result += f'padding = {self._padding}\n'
        return result
    
    def tojson(self) -> dict:
        return {'layer': 'avgpool', 'size': self._size, 'stride': self._stride, 'padding': self._padding}

# Dropout
class Dropout(Layer):
    label = "[dropout]"

    def __init__(self, probability: float):
        if not 0 < probability <= 1: raise AttributeError("probability out of bounds")
        self._probability = probability
    
    def tojson(self) -> dict:
        return {"layer" : "dropout", "probability": self._probability}
        #return f"{self.label}\nprobability={self._probability}\n"
    
    def __str__(self):
        return f"{self.label}\nprobability={self._probability}\n"
        #return json.loads(self.tojson(), indent = 3)

# Connected
class Dense(Layer):
    label = "[connected]"

    def tojson(self) -> dict:
        result = {"layer": "connected"}
        result.update(super().tojson())
        return result
    
    # def __str__(self):
    #     #result = f"{self.label}\n"
    #     result = super().__str__()
    #     return result

# Softmax
class Softmax(Layer):
    label = "[softmax]"

    def __init__(self, groups: int):
        self._groups = groups

    def tojson(self) -> dict:
        return {"layer": "softmax", "groups": self._groups}
        #return f"{self.label}\ngroups={self._groups}\n"
    
    def __str__(self):
        return f"{self.label}\ngroups={self._groups}\n"
        #return json.loads(self.tojson(), indent = 3)

# Cost
class Cost(Layer):
    label = "[cost]"
        
    def __init__(self, type = cost.CostFunction.SSE):
        self.cost = cost.CostFunction(type).value
    
    def tojson(self) -> dict:
        return {"layer" : "cost", "type": self.cost} #f"{self.label}\ntype={self.cost}\n"
    
    def __str__(self):
        return f"{self.label}\ntype={self.cost}\n"
        #return json.loads(self.tojson(), indent = 3)
        