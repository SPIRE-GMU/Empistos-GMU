import layers, activation, costfunction, sequential

if __name__ == "__main__":

    alexnet = sequential.Sequential(layers = [
        layers.Input((227, 227), channels = 3, batch_size = 32),
        layers.Conv2D(size = 11, stride = 4, filters = 96, activation = activation.Activation.RELU), 
        layers.MaxPooling2D(size = 3, stride = 2, padding = 0),
        layers.Conv2D(size = 5, pad = 2, filters = 256, activation = activation.Activation.RELU),
        layers.MaxPooling2D(size = 3, stride = 2, padding = 0),
        layers.Conv2D(size = 3, pad = 1, filters = 384, activation = activation.Activation.RELU),
        layers.Conv2D(size = 3, pad = 1, filters = 384, activation = activation.Activation.RELU),
        layers.Conv2D(size = 3, pad = 1, filters = 256, activation = activation.Activation.RELU),
        layers.MaxPooling2D(size = 3, stride = 2),
        layers.Split(clients = ['a', 'b'], server = 'server'),
        layers.Dense(4096, activation = activation.Activation.RELU),
        layers.Dropout(0.5),
        layers.Dense(4096, activation = activation.Activation.RELU),
        layers.Dropout(0.5),
        layers.Softmax(1000),
        layers.Cost(costfunction.CostFunction.SSE)
    ])

    alexnet.savemodel("splitnet")
    #alexnet.makelabels("alexnet", labels = ['1','2','3','4'])
    
    #alexnet = sequential.Sequential.loadmodel("alexnet.json")
    #print(alexnet)