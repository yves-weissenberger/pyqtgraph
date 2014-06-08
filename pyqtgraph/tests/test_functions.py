import pyqtgraph as pg
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_almost_equal
from pyqtgraph.python2_3 import asUnicode as u

np.random.seed(12345)


def test_siScale():
    expected_values=((0.0001, (1e6, u('µ'))),
                    (0.1, (1e3, u('m'))),
                    (3, (1, u(''))),
                    (5432, (1e-3, u('k'))))

    for inp, out in expected_values:
        result = pg.siScale(inp)
        assert result[1] == out[1]
        assert_almost_equal(result[0], out[0])


def test_siEval():
    expected_values=((u("100 µV"), 1e-4),
                    (u("100µV"), 1e-4),
                    (u("100uV"), 1e-4),
                    (u("100 uV"), 1e-4),
                    (u("100μV"), 1e-4),
                    (u("100 μV"), 1e-4),
                    (u("430MPa"), 430e6),
                    (u("-32 PVfds"), -32e15))

    for inp, out in expected_values:
        result = pg.siEval(inp)
        assert_almost_equal(result, out)


def test_siFormat():
    expected_values=((((0.0001,), {'suffix':'V'}),u'100 µV'),
                     (((1000,), {'suffix':'V','error':23, 'groupedError':True}),u("1.00 ±  0.02   kV")),
                     (((10,), {'suffix':'V','error':230, 'groupedError':True}),u(" 10  ±  200    V")),
                     (((432432,), {'suffix':'V','error':230,'precision':4 , 'groupedError':True}),u("432.4 ±  0.2    kV")),
                     (((432432,), {'suffix':'V','error':230,'precision':4}),u("432.4 kV ± 230 V")),
                     (((1000,), {'suffix':'V','error':23}),u("1 kV ± 23 V")),
                     (((1000,), {'suffix':'V','error':23, 'groupedError':True}),u("1.00 ±  0.02   kV")),
                     (((432432,), {'suffix':'V','error':230,'precision':5 , 'groupedError':True}),u("432.4  ±  0.2    kV")),
                     (((432432,), {'suffix':'V','error':23000,'precision':5 , 'groupedError':True}),u(" 430   ±   20    kV")),
                     (((432432,), {'suffix':'V','error':30,'precision':5 , 'groupedError':True}),u("432.43 ±  0.03   kV")),
                     (((432432,), {'suffix':'V','error':0.01,'precision':4 , 'groupedError':True}),u("432.4 ± 1e-05   kV")),
                     (((23,), {'suffix':'V','error':45334,'precision':4 , 'groupedError':True}),u(" 20   ± 50000   V")),
                     (((23,), {'suffix':'V','error':4533432424,'precision':4 , 'groupedError':True}),u(" 20   ± 5e+09   V")),
                    )
    
    for inp, out in expected_values:
        result = fnc.siFormat(*inp[0], **inp[1])
        assert result == out




def testSolve3D():
    p1 = np.array([[0,0,0,1],
                   [1,0,0,1],
                   [0,1,0,1],
                   [0,0,1,1]], dtype=float)
    
    # transform points through random matrix
    tr = np.random.normal(size=(4, 4))
    tr[3] = (0,0,0,1)
    p2 = np.dot(tr, p1.T).T[:,:3]
    
    # solve to see if we can recover the transformation matrix.
    tr2 = pg.solve3DTransform(p1, p2)
    
    assert_array_almost_equal(tr[:3], tr2[:3])


def test_interpolateArray():
    data = np.array([[ 1.,   2.,   4.  ],
                     [ 10.,  20.,  40. ],
                     [ 100., 200., 400.]])
    
    x = np.array([[  0.3,   0.6],
                  [  1. ,   1. ],
                  [  0.5,   1. ],
                  [  0.5,   2.5],
                  [ 10. ,  10. ]])
    
    result = pg.interpolateArray(data, x)
    
    #import scipy.ndimage
    #spresult = scipy.ndimage.map_coordinates(data, x.T, order=1)
    spresult = np.array([  5.92,  20.  ,  11.  ,   0.  ,   0.  ])  # generated with the above line
    
    assert_array_almost_equal(result, spresult)
    
    # test mapping when x.shape[-1] < data.ndim
    x = np.array([[  0.3,   0],
                  [  0.3,   1],
                  [  0.3,   2]])
    
    r1 = pg.interpolateArray(data, x)
    r2 = pg.interpolateArray(data, x[0,:1])
    assert_array_almost_equal(r1, r2)
    
    
    # test mapping 2D array of locations
    x = np.array([[[0.5, 0.5], [0.5, 1.0], [0.5, 1.5]],
                  [[1.5, 0.5], [1.5, 1.0], [1.5, 1.5]]])
    
    r1 = pg.interpolateArray(data, x)
    #r2 = scipy.ndimage.map_coordinates(data, x.transpose(2,0,1), order=1)
    r2 = np.array([[   8.25,   11.  ,   16.5 ],  # generated with the above line
                   [  82.5 ,  110.  ,  165.  ]])

    assert_array_almost_equal(r1, r2)
    
    
    
    
if __name__ == '__main__':
    test_interpolateArray()