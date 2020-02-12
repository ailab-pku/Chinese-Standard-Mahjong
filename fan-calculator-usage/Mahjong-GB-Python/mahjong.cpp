#include <Python.h>
#include "../Mahjong-GB-CPP/MahjongGB/MahjongGB.h"
#include <iostream>
#include <stdio.h>
static PyObject *oMahjongFanCalculator(PyObject *self, PyObject *args)
{
    vector<pair<string, pair<string, int> > > pack;
    vector<string> hand;
    PyObject *oPack = PyTuple_GetItem(args, 0);
    PyObject *oHand = PyTuple_GetItem(args, 1);
    for(int i = 0; i < PyTuple_Size(oPack); i++) {
        PyObject *oCurrPack = PyTuple_GetItem(oPack, i);
        string packType = PyUnicode_AsUTF8(PyTuple_GetItem(oCurrPack, 0));
        string packTile = PyUnicode_AsUTF8(PyTuple_GetItem(oCurrPack, 1));
        int packData = PyLong_AsLong(PyTuple_GetItem(oCurrPack, 2));
        pack.push_back(make_pair(packType,make_pair(packTile,packData)));
    }
    for(int i = 0; i < PyTuple_Size(oHand); i++) {
        hand.push_back(PyUnicode_AsUTF8(PyTuple_GetItem(oHand, i)));
    }
    vector<pair<int, string> > ans;
    try{
        string winTile = PyUnicode_AsUTF8(PyTuple_GetItem(args, 2));
        int flowerCount = PyLong_AsLong(PyTuple_GetItem(args, 3));
        bool isZIMO = PyTuple_GetItem(args, 4) == Py_True;
        bool isJUEZHANG = PyTuple_GetItem(args, 5) == Py_True;
        bool isGANG = PyTuple_GetItem(args, 6) == Py_True;
        bool isLAST = PyTuple_GetItem(args, 7) == Py_True;
        int menFeng = PyLong_AsLong(PyTuple_GetItem(args, 8));
        int quanFeng = PyLong_AsLong(PyTuple_GetItem(args, 9));
        ans = MahjongFanCalculator(pack, hand, 
            winTile,
            flowerCount,
            isZIMO,
            isJUEZHANG,
            isGANG,
            isLAST,
            menFeng,
            quanFeng);
    }catch(const string &error){
        PyErr_SetString(PyExc_Exception, error.c_str());
        return NULL;
    }
    PyObject *oAns = PyList_New(0);
    for(auto i : ans){
        PyList_Append(oAns,PyTuple_Pack(2, PyLong_FromLong(i.first),PyUnicode_FromString(i.second.c_str())));
    }
    return PyList_AsTuple(oAns);
}
static PyMethodDef mahjongMethods[]={
    {"MahjongFanCalculator", oMahjongFanCalculator,METH_VARARGS,""},
    {NULL, NULL, 0, NULL},
};
static PyModuleDef mahjongModule = {
    PyModuleDef_HEAD_INIT,
    "MahjongGB",
    "asfa",
    0,
    mahjongMethods,
};
PyMODINIT_FUNC
PyInit_MahjongGB(void) {
    PyObject* m = PyModule_Create(&mahjongModule);
    MahjongInit();
    if (m == NULL) {
        return NULL;
    }
    return m;
}