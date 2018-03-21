#! /bin/bash
import sys
import random
#get path as input
#open dot file
#read a graph before reach to next graph
#put all 

ops = ["NFS3_READ_CALL_TYPE",
       "NFS3_WRITE_CALL_TYPE",
       "NFS3_COMMIT_CALL_TYPE",
       "NFS3_READLINK_CALL_TYPE"
       "NFS3_CREATE_CALL_TYPE",
       "NFS3_MKDIR_CALL_TYPE",
       "NFS3_REMOVE_CALL_TYPE",
       "NFS3_RMDIR_CALL_TYPE",
       "NFS3_RENAME_CALL_TYPE",
       "NFS3_LINK_CALL_TYPE",
       "NFS3_READDIR_CALL_TYPE",
       "NFS3_READDIRPLUS_CALL_TYPE",
       "NFS3_SYMLINK_CALL_TYPE"
       "NFS3_GETATTR_CALL_TYPE",
       "NFS3_SETATTR_CALL_TYPE",
       "NFS3_LOOKUP_CALL_TYPE",
       "NFS3_ACCESS_CALL_TYPE"];


def cluster_trace(trc_path, count, pfi_path, gst_path):
    print("Clustering traces with Request tpe")
# open trace path
    with open(trc_path, 'r') as rf:
        fds = []
        for fn in ops:
            fds.append(open ("parser/" + fn, "w"));
        i = 0;
        inode = 0;
        req_types = [];
        inode = 0
        while i < count:
            graph = []
            node_map = dict()
            print(i)
            while rf.readline().replace("\n", "") != "Digraph G {": 
                continue;

            request_type = -1;
            for l in rf:
            #    if l.replace("\n", "") == "Digraph G {":
             #       continue
                l = l.replace("\n", "");
                l = l.replace(": ", ":")
                l = l.replace(" u", "u")
                if l == '}':
                    print(ops[request_type])
                    fds[request_type].write("t graph:" + str(i) +"\n")
                    for x in graph:
                        fds[request_type].write(x)
                    break;
                gf = l.split(' ')
                if len(gf) == 2:
                    node_map[gf[0]] = inode;
                    label = gf[1].split("__")[-1].replace("]", "").replace("\\nDEFAULT\"", "")
                    #print (label)
                    if label in ops and request_type == -1:
                        request_type = ops.index(label);
                        print("request type:" + label)
                    pbuf = "v " + str(inode) + " " + gf[1].replace(" ", "") + "\n"
                    inode = inode + 1;
                if len(gf) >= 4:
                    pbuf = "u " + str(node_map[gf[0]]) + " " + str(node_map[gf[2]]) + " " + "W\n";
                graph.append(pbuf)
            i = i + 1
        print(req_types)
        print(len(req_types))
        
        for fd in fds:
            fd.close();

    rf.close();

def parse(trc_path, count, pfi_path, gst_path):
    # open trace path
    with open(trc_path, 'r') as rf, open(pfi_path, 'w') as pwf, open(gst_path, 'w') as gwf:
        i = 0;
        inode = 0;
        req_types = [];
        while i < count:
            node_map = dict()
            inode = 0
            while rf.readline().replace("\n", "") != "Digraph G {":
                continue
            pwf.write("t # graph:" + str(i) +"\n")
            gwf.write("t # " + str(i) +"\n") 
            first_node = 1;
            for l in rf:
                l = l.replace("\n", "");
                l = l.replace(": ", ":")
                l = l.replace(" u", "u")
                if l == '}':
                    break;
                gf = l.split(' ')
                if first_node == 1:
                    if  gf[1].replace(" ", "") not in req_types:
                        req_types.append(gf[1].replace(" ", ""))
                    first_node = 0;

                if len(gf) == 2:
                    node_map[gf[0]] = inode;
                    pbuf = "v " + str(inode) + " " + gf[1].replace(" ", "") + "\n"
                    # gbuf = "v " + str(inode) + " " + gf[1].replace(" ", "") + "\n"
                    gbuf = "v " + str(inode) + " " + str(inode + 1) + "\n"
                    inode = inode + 1;
                if len(gf) >= 4:
                    pbuf = "u " + str(node_map[gf[0]]) + " " + str(node_map[gf[2]]) + " " + "W\n";#gf[3].replace(" ", "") + "\n"
                    #gbuf = "e " + str(node_map[gf[0]]) + " " + str(node_map[gf[2]]) + " " + gf[3].replace(" ", "") + "\n"
                    gbuf = "e " + str(node_map[gf[0]]) + " " + str(node_map[gf[2]]) + " " + str(node_map[gf[2]]+1) + "\n"
                pwf.write(pbuf);
                gwf.write(gbuf);
            i = i + 1
        print(req_types)
        print(len(req_types))
        pwf.close();
        gwf.close();
    rf.close();


def main():    
    if len(sys.argv) < 4:
        exit(-1)

    trc_path = sys.argv[1];
    pfi_path = sys.argv[3] + ".pafi";
    gst_path = sys.argv[3] + ".gaston";
    if sys.argv[2] == 'a':
        trc_cnt = -1;
    else:
        trc_cnt = int(sys.argv[2])    
    #parse(trc_path, trc_cnt, pfi_path, gst_path);
    cluster_trace(trc_path, trc_cnt, pfi_path, gst_path);

if __name__ == "__main__":
    main()
