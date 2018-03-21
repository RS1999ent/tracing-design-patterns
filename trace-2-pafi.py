#! /bin/bash
import sys
import random
#get path as input
#open dot file
#read a graph before reach to next graph
#put all 

def parse(trc_path, count, pfi_path, gst_path):
    # open trace path
    with open(trc_path, 'r') as rf, open(pfi_path, 'w') as pwf, open(gst_path, 'w') as gwf:
        i = 0;
        inode = 0;
        first_node = dict();
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
    parse(trc_path, trc_cnt, pfi_path, gst_path);

if __name__ == "__main__":
    main()
