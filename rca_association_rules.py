from anytree import NodeMixin, RenderTree
import re


class AssociationTreeNode(NodeMixin):
    def __init__(self, id, data_source, dimension, dim_label, metric, parent=None, reverse_effect_on_parent=False, children=None, dim_labels_to_be_excluded=None, metrics_to_be_excluded=None):
        self.id, = id,
        self.data_source = data_source
        self.dimension = dimension
        self.dim_label = dim_label
        self.metric = metric
        self.name = f"{id} {data_source} {dimension} {dim_label} {metric}"
        self.parent = parent
        self.reverse_effect_on_parent = reverse_effect_on_parent
        self.printed = False
        self.dim_labels_to_be_excluded = dim_labels_to_be_excluded
        self.metrics_to_be_excluded = metrics_to_be_excluded
        if children:
            self.children = children



'''Ecommerce Tree'''
n1 = AssociationTreeNode(id='n1', data_source='Ecommerce', dimension=None, dim_label=None, metric='Total_Sales')
n2 = AssociationTreeNode(id='n2', data_source='Ecommerce', dimension=None, dim_label=None, metric='AOV', parent=n1)
n3 = AssociationTreeNode(id='n3', data_source='Ecommerce', dimension=None, dim_label=None, metric='Orders', parent=n1)
n4 = AssociationTreeNode(id='n4', data_source='mwsAds', dimension=None, dim_label=None, metric='Conversion_Rate', parent=n3)
n5 = AssociationTreeNode(id='n5', data_source='mwsAds', dimension=None, dim_label=None, metric='Clicks', parent=n3)
n6 = AssociationTreeNode(id='n6', data_source='mwsAds', dimension=None, dim_label=None, metric='Ad_Spend', parent=n5)
n7 = AssociationTreeNode(id='n7', data_source='mwsAds', dimension=None, dim_label=None, metric='ACOS', parent=n5)


association_rules_root_nodes = [n1]



print("Association rules -")
for pre, fill, node in RenderTree(n1):
    if node.reverse_effect_on_parent:
        print(f"{pre}{node.name} (Reverse)")
    else:
        print(f"{pre}{node.name}")
