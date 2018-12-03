# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 13:25:11 2018

@author: Okada

.csv (or .tsv) ファイルをESにpostできる形式にする
"""

import json

def _convert(text, vtype = None):
    from decimal import Decimal, ROUND_HALF_EVEN

    try: 
        if vtype == type(0.1):
            return float(Decimal(str(text)).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))
        
        elif vtype != None:
            return vtype(text)
    except:
        pass
    
    try:
        value = int(text)
        return value
    except:
        pass

    try:
        return float(Decimal(str(text)).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))
    except:
        pass

    return text

def to_json(input_file, index_name, type_name, output_file, splt = None):
    
    if splt == None:
        ext = input_file.split(".")[-1].lower()
        if ext == "txt":
            splt = "\t"
        elif ext == "tsv":
            splt = "\t"
        else:
            splt = ","
    
    f = open(output_file, "w")
    
    header = []
    index = 0
    
    for l in open(input_file).readlines():
        col = l.rstrip().replace('"', "").split(splt)
        if len(header) == 0:
            header.extend(col)
            continue
        
        item1 = {
            "index": {
                "_index": index_name,
                "_type": type_name,
                "_id": index
            }
        }
        item2 = {}
        for i in range(len(header)):
            if header[i] == "":
                continue
            if col[i] == "":
                continue
            if col[i] == "NA":
                continue
            
            if header[i].startswith("V"):
                value = _convert(col[i], float)
            else:
                value = _convert(col[i])
            item2[header[i]] = value
        
        json.dump(item1, f, ensure_ascii=False)
        f.write("\n")
        json.dump(item2, f, ensure_ascii=False)
        f.write("\n")
        
        index += 1
        
    f.close()
    
if __name__ == "__main__":
    pass
    #to_json("./test.txt", "test001", "data", "output.json")
    