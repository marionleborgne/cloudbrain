__author__ = 'odrulea'

import base64
import json
import numpy as np


def MatrixToBuffer(ndarray):
    """
    In order to get a numpy matrix (array of arrays) into a json serializable form, we have to do a base64 encode
    We will wrap the matrix in an envelope with 3 elements:
    1. type of the ndarray
    2. the entire ndarray encoded as a base64 blob
    3. a list describing the dimensions of the ndarray (2 element list: [rows, cols])

    borrowed from: http://stackoverflow.com/questions/13461945/dumping-2d-python-array-with-json
    :param ndarray:
    :return:
    """
    return [str(ndarray.dtype),base64.b64encode(ndarray),ndarray.shape]

def BufferToMatrix(jsonDump):
    """
    After retrieving the encoded json from the message queue buffer, we need to translate the 3 element json
    back into its original form.
    To do this, use the 0th element to cast correct type, and 2nd element to set correct dimensions.

    borrowed from: http://stackoverflow.com/questions/13461945/dumping-2d-python-array-with-json
    :param jsonDump:
    :return:
    """
    loaded = json.loads(jsonDump)
    dtype = np.dtype(loaded[0])
    arr = np.frombuffer(base64.decodestring(loaded[1]),dtype)
    if len(loaded) > 2:
        return arr.reshape(loaded[2])
    return arr
