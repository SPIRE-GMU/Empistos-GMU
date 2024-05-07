import activation as act
import costfunction as cost
import json

class Layer:
    # Base layer class
    def __init__(self, layertype=None, **kwargs) -> None:
        self.type = layertype
        self.options = { k: v for k, v in kwargs.items() if v is not None }

    def json(self) -> dict:
        return {
            "layer": self.type,
            **self.options
        }

    def __str__(self) -> str:
        return json.dumps(
            self.json(),
            default=lambda x : str(x)
        )  

class Input(Layer):
    def __init__(self, shape, batch, subdivisions = None, channels = None, momentum = None, decay = None, max_crop = None,
                 learning_rate = None, policy = None, power = None, max_batches = None, angle = None,
                 hue = None, saturation = None, exposure = None, aspect = None):

        if not isinstance(shape, (tuple, list)) or len(shape) != 2:
            raise TypeError("shape must be a list or tuple of size 2")

        super().__init__(
            "net",
            height=shape[0],
            width=shape[1],
            batch=batch,
            subdivisions=subdivisions,
            channels=channels,
            momentum=momentum,
            decay=decay,
            max_crop=max_crop,
            learning_rate=learning_rate,
            policy=policy,
            power=power,
            max_batches=max_batches,
            angle=angle,
            hue=hue,
            saturation=saturation,
            exposure=exposure,
            aspect=aspect
        )
        

class Conv2D(Layer):
    def __init__(self, batch_normalize=0, filters=1, size=1, groups=1, stride=1, padding=0, pad=False, dilation=1, activation=act.Activation.LOGISTIC) -> None:
        # TODO Parameter Error Checking
        super().__init__(
            "convolutional",
            batch_normalize=batch_normalize,
            filters=filters,
            size=size,
            groups=groups,
            stride=stride,
            padding=padding,
            pad=1 if pad else 0,
            dilation=dilation,
            activation=activation
        )

class MaxPooling2D(Layer):
    def __init__(self, size=1, stride=1, padding=0) -> None:
        # TODO Parameter Error Checking
        super().__init__(
            "maxpool",
            size=size,
            stride=stride,
            padding=padding
        )

class AveragePooling2D(Layer):
    def __init__(self) -> None:
        super().__init__(
            "avgpool",
        )

class Dropout(Layer):
    def __init__(self, probability) -> None:
        if not 0 < probability <= 1:
            raise AttributeError("probability must be between 0 and 1")

        super().__init__(
            "dropout",
            probability=probability
        )

class Dense(Layer):
    def __init__(self, output=1, activation=act.Activation.LOGISTIC) -> None:
        super().__init__(
            "connected",
            output=output,
            activation=activation
        )

class Softmax(Layer):
    def __init__(self, groups) -> None:
        if not 0 < groups:
            raise AttributeError("Groups must be greater than 0")
            
        super().__init__(
            "softmax",
            groups=groups
        )

class Cost(Layer):
    def __init__(self, costfunc=cost.CostFunction.SSE) -> None:
        if not isinstance(costfunc, cost.CostFunction):
            raise AttributeError("costfunc must be an instance of CostFunction")

        super().__init__(
            "cost",
            type=costfunc
        )