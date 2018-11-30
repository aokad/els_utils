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

def __get_objects(url, mode, object_id, object_title, attr, max_items, debug):
    
    __print (">> __get_object_ids ({url}, {mode}, {object_id}, {max_items}, {attr})".format(
        url = url, mode = mode, attr = attr, object_id = object_id, max_items = max_items), debug
    )
    
    if object_id != "":
        itype = "id"
        value = object_title    
    else:
        itype = "title"
        value = object_id
    
    address = "{url}/api/saved_objects/_find".format(url = url)
    
    query = "?type={mode}&search_fields={type}&per_page={max}".format(
        mode = mode, type = itype, max = max_items
    )
    if value != "":
        query = "?type={mode}&search_fields={type}&per_page={max}&search={value}".format(
            mode = mode, value = value, type = itype, max = max_items
        )
    
    footer = "-H 'kbn-xsrf: true' | jq -r '.saved_objects[] | {attr}'".format(attr = attr)
    cmd = "curl -X GET -sS '{address}{query}' {footer}".format(address = address, query = query, footer = footer)
    __print(cmd, debug)
 
    try:
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if res.returncode == 0:
            return res.stdout.decode('utf-8').rstrip()
            
    except Exception as e:
        print("[Exception] {0}".format(e))
        
    return None

def __res_to_list (item, title_prefix = ""):
    
    if item == None:
        return None
    
    k = item.split("\n")
    if len(k) < 2:
        return None
    
    r = []
    for i in range(0, len(k), 2):
        if k[i+1].startswith(title_prefix.rstrip("*")):
            r.append([k[i], k[i+1]])
    
    return r

##########
# get
##########

def __print_items (item, title_prefix = ""):
    
    fitem = __res_to_list (item, title_prefix)
    if fitem == None:
        return False
    
    m = 0
    for f in fitem:
        if m < len(f[0]):
            m = len(f[0])
        if m < len(f[1]):
            m = len(f[1])
    m += 1
    print (("{0:%ds} {1:%ds}" % (m,m)).format("id", "title"))
    print ("="*m + " " + "="*m)
    for i in fitem:
        print (("{0:%ds} {1:%ds}" % (m,m)).format(i[0], i[1]))
        
    return True

def _get_object (url, mode, object_id, object_title, max_items, debug):

    __print (">> _get_object ({url}, {mode})".format(url = url, mode = mode), debug)
    
    
    if mode in ["dashboard", "visualization", "index-pattern"]:
        item = __get_objects(url, mode, object_id, object_title, ".id, .attributes.title", max_items, debug) 
        return __print_items (item, object_title)
    
    elif mode == "all":
        print ('\n[dashboard]')
        item = __get_objects(url, "dashboard", "", "", ".id, .attributes.title", max_items, debug) 
        if __print_items (item):
            print ('\n[visualization]')
            item = __get_objects(url, "visualization", "", "", ".id, .attributes.title", max_items, debug) 
            if __print_items (item):
                print ('\n[index-pattern]')
                item = __get_objects(url, "index-pattern", "", "", ".id, .attributes.title", max_items, debug)
                return __print_items (item)
        return False
    
    elif mode == "challenge":
        item = __get_objects(url, "dashboard", "", "*", ".attributes.title", max_items, debug)
        if item == None:
            return False
        
        print ("challenge")
        print ("="*30)
        for i in item.split("\n"):
            print (i.replace("-dashboard", ""))
        return True
    
    return False

def get_if(args):
    
    return _get_object(__get_url(args.conf), args.type, args.id, args.title, args.max, args.debug)

##########
# delete
##########

def _delete_object (url, mode, object_id, debug, dryrun):
    
    __print (">> _delete_object ({url}, {mode}, {object_id})".format(url = url, mode = mode, object_id = object_id), debug)

    try:
        cmd = "curl -X DELETE -sS {kibana_host}/api/saved_objects/{mode}/{id} -H 'kbn-xsrf: true' | jq .".format(
                kibana_host = url, mode = mode, id = object_id
                )
        if dryrun:
            print (cmd)
            return True
            
        res = subprocess.run(cmd, shell =True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        msg = json.loads(res.stdout)
        __print (msg, debug)
        
        if "error" in msg:
            print("[ERROR] %s" % (msg))
            print ("[Failure] delete object %s %s" % (mode, object_id))
            return False
        
        print ("[Success] delete object %s %s" % (mode, object_id))
        return True
        
    except Exception as e:
        print ("[Exception] {0}".format(e))
        print ("[Failure] delete object %s %s" % (mode, object_id))
    
    return False
    
def _delete_object_title (url, mode, object_title, debug, dryrun):
    
    __print (">> _delete_object ({url}, {mode}, {object_title})".format(url = url, mode = mode, object_title = object_title), debug)

    item = __res_to_list(__get_objects(url, mode, "", object_title, ".id, .attributes.title", 100, debug), object_title)
    
    if item == None:
        return False

    success = True
    for text in item:
        [index, title] = text.split(",")
        
        if mode == "index-pattern" and title == "version":
            continue
        
        success = _delete_object (url, mode, index, debug, dryrun)
        if success == False:
            return False
    
    return True

def delete_if(args):
    
    if args.type in ["dashboard", "visualization", "index-pattern"]:
        if args.id == "" and args.title == "":
            print ("[ERROR] set --id or --title option")
            return False
        
        success = True
        if args.id != "":
            success = _delete_object (__get_url(args.conf), args.type, args.id, args.debug, args.dryrun)
        if args.title != "" and success:
            success = _delete_object_title (__get_url(args.conf), args.type, args.title, args.debug, args.dryrun)
        
        return success
        
    if args.type == "all":
        success = _delete_object_title (__get_url(args.conf), "dashboard", "*", args.debug, args.dryrun)
        if success:
            success = _delete_object_title (__get_url(args.conf), "visualization", "*", args.debug, args.dryrun)
            if success:
                success = _delete_object_title (__get_url(args.conf), "index-pattern", "*", args.debug, args.dryrun)
        return success

    if args.type == "challenge":
        if args.challenge_id == "":
            print ("[ERROR] set --challenge_id option")
            return False
        
        object_title = "%s*" % (args.challenge_id)
        success = _delete_object_title (__get_url(args.conf), "dashboard", object_title, args.debug, args.dryrun)
        if success:
            success = _delete_object_title (__get_url(args.conf), "visualization", object_title, args.debug, args.dryrun)
            if success:
                success = _delete_object_title (__get_url(args.conf), "index-pattern", object_title, args.debug, args.dryrun)
        return success

    return False


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


if __name__ == "__main__":
    pass

