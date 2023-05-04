from enum import Enum


# class syntax
class Runtime(str, Enum):
    DBR_13 = "13.0.x-scala2.12"
    DBR_13_ML = "13.0.x-cpu-ml-scala2.12"
    DBR_13_ML_GPU = "13.0.x-gpu-ml-scala2.12"
