from enum import Enum

class Activation(Enum):
    # Activation functions for Layers
    LOGISTIC = 'logistic'
    RELU = 'relu'
    RELIE = 'relie'
    LINEAR = 'linear'
    RAMP = 'ramp'
    TANH = 'tanh'
    PLSE = 'plse'
    LEAKY = 'leaky'
    ELU = 'elu'
    LOGGY = 'loggy'
    STAIR = 'stair'
    HARDTAN = 'hardtan'
    LHTAN = 'lhtan'
    SELU = 'selu'