import json
import sys
import csv

graph = {
    "nodes":[
        {
            "id":"1", 
            "fontcolor":"blue",
            "shape":"plaintext",
            "label":"Cluster ID: 8\nSpecific Mutation Type: Structural mutation\nCost: 0\nOverall Mutation Type: Structural_Mutation and_Response_Time_Change\nCandidate originating clusters: \n\nAvg. response times: 8748 us ; 4408 us\nStandard Deviations: 40831 us ; 15889 us\nKS-Test2 P-value: 0.000\nCluster likelihood: 0.1353 ; 0.3783\nPercent makeup: 8 / 92\nrequests: 18199 ; 203061"
        } ,
        {
            "id":"",
            "label": ""
        }
    ] ,
    "edges":[
        {
            "from":"",
            "to": "",
            "label":""
        }
    ]
}

def convert(fp_path, json_path, csv_path):
    
    with open(fp_path, 'r') as fpf, open(json_path, 'w') as jsonf, open(csv_path, 'w') as csvf:
        request = []
        index = 0
        nodes = []
        edges = []
        csvedge = []
        graphmeta = "# t 0-0-0"
        print("Start Conversion")
        for l in fpf:
            if l[0] == '#':
                continue;
            elif l[0] == 't':
                # need to add comment also
                print(l)
                nodes.insert(0, {'id' : 1, 'fontcolor' : 'blue', 
                                 'shape': 'plaintext ', 
                                 'label':'Cluster ID: 8\nSpecific Mutation Type: Structural mutation\nCost: 0\nOverall Mutation Type: Structural_Mutation and_Response_Time_Change\nCandidate originating clusters: \n\nAvg. response times: 8748 us ; 4408 us\nStandard Deviations: 40831 us ; 15889 us\nKS-Test2 P-value: 0.000\nCluster likelihood: 0.1353 ; 0.3783\nPercent makeup: 8 / 92\nrequests: 18199 ; 203061'})
                request = {'meta': graphmeta, 'nodes' : nodes, 'edges' : edges} 
                json.dump(request, jsonf)
                jsonf.write("\n\n");
                graphmeta = l;
                csvedge.append([0, 0])
                del edges[:]
                del nodes[:]
                index = index + 1
            elif l[0] == 'v':
                vid = str(int(l.split(' ')[1]) + 5)
                vlb = l.split(' ')[2]
                nodes.append({'id' : vid, 'label' : vlb})
            elif l[0] == 'u':
                fromn = str(int(l.split(' ')[1]) + 5);
                ton = str(int(l.split(' ')[2]) + 5);
                #csvedge.append(str(int(l.split(' ')[1]) + index) + "," + str(int(l.split(' ')[2]) + index) + "\n")
                csvedge.append([int(l.split(' ')[1]) + index, int(l.split(' ')[2]) + index])
                index = index + 1
                edges.append({'to' : ton, 'from' : fromn, 'color': 'black', 
                              'label' : 'p:0.00\n   a: 50us / 60us\n   s: 40829us / 15888us'})
            else:
                print("unknown format")
        writer = csv.writer(csvf)
        writer.writerows(csvedge)

    print("End Conversion")
    fpf.close()
    jsonf.close()
    csvf.close()
    print(json_path)

def main():    
    if len(sys.argv) < 4:
        exit(-1)
    
    fp_path = sys.argv[1];
    json_path = sys.argv[2];
    csv_path = sys.argv[3];
    convert(fp_path, json_path, csv_path);

if __name__ == "__main__":
    main()
