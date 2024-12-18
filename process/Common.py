import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
sys.path.append(p)
import networkx as nx      # networkx为第三方库,包含多种图论算法
import uuid




def max_match(func):
    """获得一个二分图的最大匹配, 并检验是否是完美匹配"""
    def hg_match(*args):
        """匈牙利匹配算法
            args 最后一个参数必须为字典, 键为点位, 其值是与该点位有关系的点位合集
        """
        edges=[]
        relationship=args[-1]
        if isinstance(relationship,str):
            print(relationship)
            return
        aconv={}
        rnode_list=[]
        rnode_ori=[]
        for l_node,r_nodes in relationship.items():
            for node in r_nodes:
                if isinstance(node,list):
                    if node not in rnode_ori:
                        rnode_ori.append(node)
                        uid = str(uuid.uuid4())
                        aconv.setdefault(uid, node)
                        edges.append((l_node, uid))
                    else:
                        for k, va in aconv.items():
                            if va == node:
                                edges.append((l_node, k))
                                break

                else:
                    edges.append((l_node,node))
                    rnode_list.append(node)
        print("releationship:",relationship,edges)
        g = nx.Graph()
        # 二分图左边点集合
        print(list(relationship.keys()))
        g.add_nodes_from(list(relationship.keys()),bipartite=0)
        # 二分图右边点集合
        print('r_nodes',rnode_list)
        g.add_nodes_from(rnode_list,bipartite=1)
        g.add_edges_from(edges)
        # 获取连通的分量
        connected_components = list(nx.connected_components(g))
        matching_all={}
        for component in connected_components:
            # 构建一个子图，只包含当前连通分量的节点和边
            subgraph = g.subgraph(component)
            # 使用匈牙利算法找到最大匹配
            matching = nx.bipartite.maximum_matching(subgraph)
            for i in list(matching.keys()):
                if i not in relationship.keys():
                    matching.pop(i)
            matching_all.update(matching)
        if aconv!={}:
            for i,j in matching_all.items():
                if aconv.get(j) is not None:
                    matching_all[i]=aconv[j]
        if len(matching_all)<len(relationship.keys()):
            print("不是完美匹配:",matching_all)
        new_args=list(args[:-1])
        new_args.append(matching_all)
        print("new_args",new_args)
        return func(*tuple(new_args))
    return hg_match
