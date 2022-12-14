from . import write_meta as meta
import csv
import json
import os

def outputExt(objType, fType):
    if objType == "str":
        objType = "username"
    outExt = f"/{objType}s.{fType}"

    return outExt

def addExt(base, objType, fType):
    if len(base.split('.')) == 1:
        createDirIfMissing(base)
        base += outputExt(objType, fType)

    return base

def Text(entry):
    print(entry.replace('\n', ' '))

def Type(config):
    _type = "tweet"
    return _type

def struct(obj, custom, _type):
    if custom:
        fieldnames = custom
        row = {}
        for f in fieldnames:
            row[f] = meta.Data(obj, _type)[f]
    else:
        fieldnames = meta.Fieldnames(_type)
        row = meta.Data(obj, _type)

    return fieldnames, row

def createDirIfMissing(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
