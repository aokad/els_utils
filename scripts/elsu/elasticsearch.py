# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 12:21:06 2018

@author: Okada
"""

import json
import subprocess

def __print(mesg, debug):
    if debug:
        print(mesg)

def __get_url(conf):
    import yaml
    data = yaml.load(open(conf))
    return data["elastic_host"]

##########
# post
##########
def _post_datafile(url, file_path, debug, dryrun):

    __print (">> _post_datafile ({url}, {file_path})".format(url = url, file_path = file_path), debug)
    
    cmd = "curl -XPOST -s {elastic_host}/_bulk -H 'Content-Type: application/json' --data-binary @{file}".format(
            elastic_host = url, file=file_path)
    
    if dryrun:
        print (cmd)
        return True
    
    __print(cmd, debug)

    try:
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        msg = json.loads(res.stdout)
        __print (msg, debug)
        
        if "error" in msg:
            print("[ERROR] [%d] [%s] [%s]" % (msg["status"], msg["error"]["type"], msg["error"]["reason"]))
            print ("[Failure] post datafile %s" % (file_path))
            return False
        
        if msg["errors"] == False:
            print ("[Success] post datafile %s" % (file_path))
            return True
        else:
            for item in msg["items"]:
                if "error" in item["index"]:
                    print("[ERROR] %s" % (json.dumps(item["index"]["error"])))
            print ("[Failure] post datafile %s" % (file_path))
            return False
        
    except Exception as e:
        print("[Exception] {0}".format(e))
    
    print ("[Failure] post datafile %s" % (file_path))
    return False

def post_if(args):
    return _post_datafile(__get_url(args.conf), args.file, args.debug, args.dryrun)

##########
# get
##########
def _get_object (url, mode, detail, index, debug):

    __print (">> _get_object ({url}, {mode}, {detail}, {index})".format(url = url, mode = mode, detail = detail, index = index), debug)
    
    form = "json"
    
    if mode == "db":
        if detail:
            cmd = "curl -XGET {elastic_host}/_cat/indices?v".format(elastic_host = url)
            form = "text"
        else:
            cmd = "curl -XGET {elastic_host}/_aliases -s | jq '. | keys'".format(elastic_host = url)            
    
    elif mode == "table":
        cmd = "curl -XGET {elastic_host}/{index} -s | jq .".format(elastic_host = url, index = index)
    
    elif mode == "record":
    
        cmd = ("type=$(curl -XGET {elastic_host}/{index}/ -s | jq -r '.[].mappings | keys[0]'); "
            + "curl -XGET {elastic_host}/{index}/${{type}}/0 -s | jq '._source'").format(
            elastic_host = url, index = index)
        
    __print(cmd, debug)

    try:
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        __print (res, debug)
        
        if res.returncode == 0:
            returncode = res.stdout.decode('utf-8').rstrip()
            
            if form == "text":
                for item in returncode.split("\n"):
                    print (item)
            else:
                import pprint 
                pprint.pprint(json.loads(returncode))
        else:
            returncode = res.stderr.decode('utf-8').rstrip()
            import pprint 
            pprint.pprint(json.loads(returncode))
            return False
        
    except Exception as e:
        print("[Exception] {0}".format(e))
        print ("[Failure] get object %s" % (mode))
        return False
    
    return True

def get_if(args):
    if args.type in ["table", "record"]:
        if args.name == "":
            print ("[ERROR] set --name option")
            return False
    return _get_object(__get_url(args.conf), args.type, args.detail, args.name, args.debug)

##########
# delete
##########
def _delete_object (url, index, debug, dryrun):

    __print (">> _delete_object ({url}, {index})".format(url = url, index = index), debug)
    
    cmd = "curl -XDELETE {elastic_host}/{index}".format(elastic_host = url, index = index)
    
    if dryrun:
        print (cmd)
        return True
    
    __print(cmd, debug)
    
    try:
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        msg = json.loads(res.stdout)
        __print (msg, debug)
        
        if "error" in msg:
            print("[ERROR] [%d] [%s] [%s]" % (msg["status"], msg["error"]["type"], msg["error"]["reason"]))
            print ("[Failure] delete object %s" % (index))
            return False
        
        if msg["errors"] == False:
            print ("[Success] delete object %s" % (index))
            return True
        else:
            for item in msg["items"]:
                if "error" in item["index"]:
                    print("[ERROR] %s" % (json.dumps(item["index"]["error"])))
            print ("[Failure] delete object %s" % (index))
            return False
        
    except Exception as e:
        print("[Exception] {0}".format(e))
    
    print ("[Failure] delete object %s" % (index))
    return False

def delete_if(args):
    return _delete_object(__get_url(args.conf), args.name, args.debug, args.dryrun)
    
if __name__ == "__main__":
    pass
