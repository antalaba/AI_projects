There are some files in gstrb which cannot be resized because that already have a size of (30,29,3)
Using cv2.resize instad of np.resize solves this issue
Using larger pooling size lowers the accurancy
Incrising the number of layers in Con2D incrieses the accuracy but makes the code slower
Incrising kernel size to around 5 in Con2D incrieses the accuracy
The droput rate of 0.5 seems to be too large better accuracy can be achieved with a lower dropout rate
Adding more hidden layers resulted in lowering the accuracy
