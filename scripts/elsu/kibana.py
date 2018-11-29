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
    return data["kibana_host"]

##########
# post
##########
def __object_exits(url, object_type, object_id, debug):
    
    __print (">> __object_exits ({url}, {object_type}, {object_id})".format(
        url = url, object_type = object_type, object_id = object_id), debug
    )
    cmd = "curl -XGET -s {url}/api/saved_objects/{object_type}/{object_id}".format(
            url = url, object_type = object_type, object_id = object_id) + ' -o /dev/null -w "%{http_code}"'
    
    __print(cmd, debug)

    try:
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if res.stdout == b"200":
            return True
        
    except Exception as e:
        print("[Exception] {0}".format(e))
    
    return False

def _create_indexpattern(url, index_id, debug):
    
    __print (">> _create_indexpattern ({url}, {index_id})".format(url = url, index_id = index_id), debug)
    
    if not __object_exits(url, "index-pattern", index_id, debug):
        
        attr = json.dumps({"attributes":{"title": index_id}})
        cmd = "curl -XPOST -s -H 'Content-Type: application/json' -H 'kbn-xsrf: anything' {url}/api/saved_objects/index-pattern/{id} '-d{attr}'".format(
            url = url, id = index_id, attr = attr)
    
        __print(cmd, debug)

        try:
            res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            msg = json.loads(res.stdout)
            
            if "id" in msg:
                print ("[Success] create index-pattern %s" % (index_id))
                return True
            
            __print (msg, debug)
            print ("[Failure] create index-pattern %s" % (index_id))
            
        except Exception as e:
            print("[Exception] {0}".format(e))
    
    else:
        print ("Already exists index-pattern %s" % (index_id))
        return True

    return False

def _create_visualization(url, file_path, debug):

    __print (">> _create_visualization ({url}, {file_path})".format(url = url, file_path = file_path), debug)
    
    cmd = "curl -XPOST -s -H 'Content-type: application/json' -H 'kbn-xsrf:true' {url}/api/kibana/dashboards/import -d @{file_path}".format(
        url = url, file_path = file_path)

    __print(cmd, debug)

    try:
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        msg = json.loads(res.stdout)
        
        if "objects" in msg and "id" in msg["objects"][0]:
            print ("[Success] create object: %s" % (file_path))
            return True
        
        __print (msg, debug)
        
    except Exception as e:
        print("[Exception] {0}".format(e))

    print ("[Failure] create object: %s" % (file_path))
    return False

def _create_dashboard(url, file_path, debug):

    __print (">> _create_dashboard ({url}, {file_path})".format(url = url, file_path = file_path), debug)
    
    dashboard_conf = json.load(open(file_path))
    dashboard_id = dashboard_conf["objects"][-1]["attributes"]["title"]
    dashboard_url = "%s/app/kibana#/dashboard/%s" % (url, dashboard_id)
    
    #if not object_exits(url, "dashboard", dashboard_id, debug):
    if True:
        
        cmd = "curl -XPOST -s -H 'Content-type: application/json' -H 'kbn-xsrf:true' {url}/api/kibana/dashboards/import -d @{file_path}".format(
            url = url, file_path = file_path)
    
        __print(cmd, debug)
    
        try:
            res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            msg = json.loads(res.stdout)
            
            if "objects" in msg and "id" in msg["objects"][0]:
                print ("[Success] create dashboard: %s" % (dashboard_url))
                return True
            
            __print (msg, debug)
            
        except Exception as e:
            print("[Exception] {0}".format(e))
    
    else:
        print ("Already exists dashboard: %s" % (dashboard_url))
        return True

    return False

    print ("[Failure] creted dashboard: %s" % (file_path))
    return False

def post_if(args):
    
    if args.mode == "index-pattern":
        if args.index == "":
            print ("[ERROR] set --index option")
            return False
        return _create_indexpattern(__get_url(args.conf), args.index, args.debug)
    
    elif args.mode == "visualization":
        if args.file == "":
            print ("[ERROR] set --file option")
            return False
        return _create_visualization(__get_url(args.conf), args.file, args.debug)
    
    elif args.mode == "dashboard":
        if args.file == "":
            print ("[ERROR] set --file option")
            return False
        return _create_dashboard(__get_url(args.conf), args.file, args.debug)

##########
# get
##########
def __get_request (cmd, debug):
    
    try:
        __print(cmd, debug)
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        __print (res, debug)
    
        if res.returncode == 0:
            returncode = res.stdout.decode('utf-8').rstrip()
            print (returncode)
        else:
            returncode = res.stderr.decode('utf-8').rstrip()
            print (returncode)
            return False
            
    except Exception as e:
        print("[Exception] {0}".format(e))
        return False

    return True

def _get_object (url, mode, debug):

    __print (">> _get_object ({url}, {mode})".format(url = url, mode = mode), debug)
    
    if mode in ["dashboard", "visualization", "index-pattern"]:
        cmd = "curl -X GET '{kibana_host}/api/saved_objects/_find?type={type}' -s -H 'kbn-xsrf: true' | jq -r '.saved_objects[] | .attributes.title'".format(
            kibana_host = url, type = mode)
        return __get_request (cmd, debug)
    
    elif mode == "all":
        print ('=== dashboards ===')
        cmd = "curl -X GET '{kibana_host}/api/saved_objects/_find?type=dashboard' -s -H 'kbn-xsrf: true' | jq -r '.saved_objects[] | .attributes.title'".format(
            kibana_host = url)
        success = __get_request (cmd, debug)
    
        if success:
            print ('=== visualizations ===')
            cmd = "curl -X GET '{kibana_host}/api/saved_objects/_find?type=visualization' -s -H 'kbn-xsrf: true' | jq -r '.saved_objects[] | .attributes.title'".format(
                kibana_host = url)
            success = __get_request (cmd, debug)
        
        if success:
            print ('=== index-patterns ===')
            cmd = "curl -X GET '{kibana_host}/api/saved_objects/_find?type=index-pattern' -s -H 'kbn-xsrf: true' | jq -r '.saved_objects[] | .attributes.title'".format(
                kibana_host = url)
            success = __get_request (cmd, debug)
        return success
    
    elif mode == "challenge":
        cmd = "curl -X GET '{kibana_host}/api/saved_objects/_find?type=dashboard' -s -H 'kbn-xsrf: true' | jq -r '.saved_objects[] | .attributes.title' | sed -n 's/-dashboard//gp'".format(
            kibana_host = url)
        return __get_request (cmd, debug)
    
    return False

def get_if(args):
    return _get_object(__get_url(args.conf), args.type, args.debug)

##########
# delete
##########
def __get_object_ids(url, mode, prefix, attr, debug):
    
    __print (">> __get_object_ids ({url}, {mode}, {prefix})".format(
        url = url, mode = mode, prefix = prefix), debug
    )
            
    address = "{url}/api/saved_objects/_find?type={mode}".format(url = url, mode = mode)
    footer = "-H 'kbn-xsrf: true' | jq -r '.saved_objects[] | {attr}'".format(attr = attr)
    cmd = "curl -X GET -sS '{address}' {footer}".format(address = address, footer = footer)
    __print(cmd, debug)

    try:
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if res.returncode == 0:
            results = res.stdout.decode('utf-8').rstrip().split("\n")
            
            if prefix == "":
                return results
            
            filted = []
            for item in results:
                if item.startswith(prefix):
                    filted.append(item)
            return filted
        
    except Exception as e:
        print("[Exception] {0}".format(e))
    
    return []

def _delete_dashboard (url, prefix, delete_all, debug, dryrun):
    
    __print (">> _delete_dashboard ({url}, {prefix}, {delete_all})".format(url = url, prefix = prefix, delete_all = delete_all), debug)

    item = __get_object_ids(url, "dashboard", prefix, ".attributes.title", debug) 
    
    print (item)
    return
    try:
        for index in item:
            
            delete = False
            if delete_all:
                delete = True
            elif index.startswith(prefix):
                delete = True
            
            if not delete:
                continue
            
            cmd = "curl -X DELETE -sS {kibana_host}/api/saved_objects/dashboard/{id} -H 'kbn-xsrf: true' | jq .".format(
                    kibana_host = url, id = index
                    )
            print (cmd)
            if dryrun:
                continue
                
            res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            msg = json.loads(res.stdout)
            __print (msg, debug)
            
            if "error" in msg:
                print("[ERROR] [%d] [%s] [%s]" % (msg["status"], msg["error"]["type"], msg["error"]["reason"]))
                print ("[Failure] delete object %s" % (index))
                return False
            
            if msg["errors"] == False:
                print ("[Success] delete object %s" % (index))
                
            else:
                for item in msg["items"]:
                    if "error" in item["index"]:
                        print("[ERROR] %s" % (json.dumps(item["index"]["error"])))
                print ("[Failure] delete object %s" % (index))
                return False
        
    except Exception as e:
        print ("[Exception] {0}".format(e))
        print ("[Failure] delete object %s" % (index))
        return False
    
    return True

def _delete_visualization (url, prefix, delete_all, debug, dryrun):
    
    __print (">> _delete_visualization ({url}, {prefix})".format(url = url, prefix = prefix), debug)

    item = __get_object_ids(url, "visualization", prefix, ".attributes.title", debug) 
    print (item)
    return
    try:
        for index in item:
            
            delete = False
            if delete_all:
                delete = True
            elif index.startswith(prefix):
                delete = True
            
            if not delete:
                continue
            
            cmd = "curl -X DELETE -sS {kibana_host}/api/saved_objects/visualization/{id} -H 'kbn-xsrf: true' | jq .".format(
                    kibana_host = url, id = index
                    )
            print (cmd)
            if dryrun:
                continue
                
            res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            msg = json.loads(res.stdout)
            __print (msg, debug)
            
            if "error" in msg:
                print("[ERROR] [%d] [%s] [%s]" % (msg["status"], msg["error"]["type"], msg["error"]["reason"]))
                print ("[Failure] delete object %s" % (index))
                return False
            
            if msg["errors"] == False:
                print ("[Success] delete object %s" % (index))
                
            else:
                for item in msg["items"]:
                    if "error" in item["index"]:
                        print("[ERROR] %s" % (json.dumps(item["index"]["error"])))
                print ("[Failure] delete object %s" % (index))
                return False
        
    except Exception as e:
        print ("[Exception] {0}".format(e))
        print ("[Failure] delete object %s" % (index))
        return False
    
    return True

def _delete_index_patterns (url, prefix, delete_all, debug, dryrun):
    
    __print (">> _delete_index_patterns ({url}, {prefix})".format(url = url, prefix = prefix), debug)

    item = __get_object_ids(url, "index-pattern", prefix, ".id, .attributes.title", debug) 
    print (item)
    return
    try:
        for text in item:
            li = text.split(",")
            index = li[0]
            title = li[1]
            
            if title == "version":
                continue
            
            delete = False
            if delete_all:
                delete = True
            elif index.startswith(prefix):
                delete = True
            
            if not delete:
                continue
            
            cmd = "curl -X DELETE -sS {kibana_host}/api/saved_objects/index-pattern/{id} -H 'kbn-xsrf: true' | jq .".format(
                    kibana_host = url, id = index
                    )
            print (cmd)
            if dryrun:
                continue
                
            res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            msg = json.loads(res.stdout)
            __print (msg, debug)
            
            if "error" in msg:
                print("[ERROR] [%d] [%s] [%s]" % (msg["status"], msg["error"]["type"], msg["error"]["reason"]))
                print ("[Failure] delete object %s" % (index))
                return False
            
            if msg["errors"] == False:
                print ("[Success] delete object %s" % (index))
                
            else:
                for item in msg["items"]:
                    if "error" in item["index"]:
                        print("[ERROR] %s" % (json.dumps(item["index"]["error"])))
                print ("[Failure] delete object %s" % (index))
                return False
        
    except Exception as e:
        print ("[Exception] {0}".format(e))
        print ("[Failure] delete object %s" % (index))
        return False
    
    return True

def delete_if(args):
    
    delete_dashboard = (args.type == "dashboard")
    delete_visulalization = (args.type == "visualization")
    delete_indexpattern = (args.type == "index-pattern")
    delete_all = False
    object_id = args.object_id
    
    if args.type == "challenge":
        object_id = "%s-*" % (args.challenge_id)
        delete_dashboard = True
        delete_visulalization = True
        delete_indexpattern = True
    
    elif args.type == "all":
        delete_all = True
        delete_dashboard = True
        delete_visulalization = True
        delete_indexpattern = True
    
    success = True
    
    if delete_dashboard and success:
        if args.type == "dashboard":
            if args.object_id == "":
                print ("[ERROR] set --object_id option")
                return False
        print ("=== remove dashboards ... ===")    
        success = _delete_dashboard (__get_url(args.conf), object_id, delete_all, args.debug, args.dryrun)
        print ("=== removed dashboards ===")
    
    if delete_visulalization and success:
        if args.type == "visualization":
            if args.object_id == "":
                print ("[ERROR] set --object_id option")
                return False
        print ("=== remove visualizations ... ===")
        success = _delete_visualization (__get_url(args.conf), object_id, delete_all, args.debug, args.dryrun)
        print ("=== removed visualizations ===")

    if delete_indexpattern and success:
        if args.type == "index-pattern":
            if args.object_id == "":
                print ("[ERROR] set --object_id option")
                return False
        print ("=== remove index-patterns ... ===")
        success = _delete_index_patterns (__get_url(args.conf), object_id, delete_all, args.debug, args.dryrun)
        print ("=== removed index-patterns ===")
    
    return success

if __name__ == "__main__":
    pass

