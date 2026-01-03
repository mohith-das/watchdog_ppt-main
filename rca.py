from helper import print_anomaly, check_warning, check_critical, Element
from anytree import NodeMixin, RenderTree
from rca_association_rules import association_rules_root_nodes
import re
import itertools
from collections import defaultdict


class Node(NodeMixin):
    def __init__(self, y, y_prev, yhat, yhat_upper, yhat_lower, anomaly_type, is_warning, is_critical, data_source, period, dimension, dim_label, metric, revenue_impact, parent=None, reverse_effect_on_parent=False, children=None):
        self.y = y
        self.y_prev = y_prev
        self.yhat = yhat
        self.yhat_upper = yhat_upper
        self.yhat_lower = yhat_lower
        self.anomaly_type = anomaly_type
        self.data_source = data_source
        self.period = period
        self.dimension = dimension
        self.dim_label = dim_label
        self.metric = metric
        self.revenue_impact = revenue_impact
        self.parent = parent
        self.reverse_effect_on_parent = reverse_effect_on_parent
        self.printed = False
        self.is_anomaly = anomaly_type in [1, -1]
        self.is_warning = is_warning
        self.is_critical = is_critical
        if children:
            self.children = children


def filter_data_by_association_rules_node(asset_df, association_rules_node, parent_node=None):
    if association_rules_node.data_source == 'same_as_parent':
        data_source_mask = asset_df['data_source'] == parent_node.data_source
    else:
        data_source_mask = asset_df['data_source'] == association_rules_node.data_source

    if association_rules_node.dimension:
        if association_rules_node.dimension == 'same_as_parent':
            dimension_mask = asset_df['dimension'] == parent_node.dimension
        else:
            dimension_mask = asset_df['dimension'] == association_rules_node.dimension
    else:
        dimension_mask = asset_df['dimension'].isnull()

    if association_rules_node.dim_label:
        if isinstance(association_rules_node.dim_label, re.Pattern):
            dim_label_mask = asset_df['dim_label'].str.match(association_rules_node.dim_label)
        elif association_rules_node.dim_label == 'same_as_parent':
            dim_label_mask = asset_df['dim_label'] == parent_node.dim_label
        else:
            dim_label_mask = asset_df['dim_label'] == association_rules_node.dim_label
    else:
        dim_label_mask = asset_df['dim_label'].isnull()

    if isinstance(association_rules_node.metric, re.Pattern):
        metric_mask = asset_df['metric'].str.match(association_rules_node.metric)
    else:
        metric_mask = asset_df['metric'] == association_rules_node.metric

    if association_rules_node.dim_labels_to_be_excluded:
        exclude_dim_labels_mask = asset_df['dim_label'].isin(association_rules_node.dim_labels_to_be_excluded)
    else:
        exclude_dim_labels_mask = False

    if association_rules_node.metrics_to_be_excluded:
        exclude_metrics_mask = asset_df['metric'].isin(association_rules_node.metrics_to_be_excluded)
    else:
        exclude_metrics_mask = False

    filtered_df = asset_df[data_source_mask & dimension_mask & dim_label_mask & metric_mask & ~exclude_dim_labels_mask & ~exclude_metrics_mask]
    return filtered_df


def get_nodes_from_df(filtered_df):
    nodes_list = []
    for index, row in filtered_df.iterrows():
        y = row['y']
        y_prev = row['y_prev']
        yhat = row['yhat']
        y_prev_lower = row['y_prev_lower']
        y_prev_upper = row['y_prev_upper']
        yhat_upper = row['yhat_upper']
        yhat_lower = row['yhat_lower']
        data_source = row['data_source']
        period = row['period']
        dimension = row['dimension']
        dim_label = row['dim_label']
        metric = row['metric']
        anomaly_type = row['yhat_anomaly_type']
        revenue_impact = row['revenue_impact']
        # is_critical = check_critical(y, upper=y_prev_upper, lower=y_prev_lower)
        is_critical = check_critical(y, upper=yhat_upper, lower=yhat_lower)
        is_warning = check_warning(y, upper=yhat_upper, lower=yhat_lower)
        node = Node(y, y_prev, yhat, yhat_upper, yhat_lower, anomaly_type, is_warning, is_critical, data_source, period, dimension, dim_label, metric, revenue_impact)
        nodes_list.append(node)

    nodes_list = sorted(nodes_list, key=lambda node: abs(node.revenue_impact), reverse=True)

    return nodes_list


def build_tree_with_all_metrics(asset_df, association_rules_node, parent_node=None, parent_association_rules_node=None):
    if parent_node:
        filtered_df = filter_data_by_association_rules_node(asset_df, association_rules_node, parent_node)
    else:
        filtered_df = filter_data_by_association_rules_node(asset_df, association_rules_node, parent_node=parent_association_rules_node)

    root_nodes_list = get_nodes_from_df(filtered_df)


    'if data is not available for the root nodes'
    if not root_nodes_list:
        'create root nodes from the children'
        for association_rules_child in association_rules_node.children:
            root_nodes_list = build_tree_with_all_metrics(asset_df, association_rules_child, parent_node, association_rules_node)
            for root_node in root_nodes_list:
                root_node.parent = parent_node
        return root_nodes_list

    else:
        for root_node in root_nodes_list:
            for association_rules_child in association_rules_node.children:
                child_nodes_list = build_tree_with_all_metrics(asset_df, association_rules_child, root_node, association_rules_node)
                for child_node in child_nodes_list:
                    child_node.parent = root_node

        if association_rules_node.reverse_effect_on_parent:
            for node in root_nodes_list:
                node.reverse_effect_on_parent = True

    return root_nodes_list


# nodes_list = rca_nodes_list
# node = nodes_list[0]
def keep_only_anomalies(nodes_list, parent_anomaly_type=None):
    if not nodes_list:
        return []

    processed_nodes_list = []
    for node in nodes_list:
        same_anomaly_as_parent = (parent_anomaly_type == node.anomaly_type) and not node.reverse_effect_on_parent
        reverse_effect_on_parent = (parent_anomaly_type == -node.anomaly_type) and node.reverse_effect_on_parent
        node_explains_parent_anomaly = same_anomaly_as_parent or reverse_effect_on_parent

        if parent_anomaly_type is None:
            if node.is_anomaly:
                processed_nodes_list.append(node)
                node.children = keep_only_anomalies(node.children, node.anomaly_type)
            else:
                pass
        else:
            if node_explains_parent_anomaly:
                processed_nodes_list.append(node)
                node.children = keep_only_anomalies(node.children, node.anomaly_type)
            elif node.reverse_effect_on_parent:
                processed_children_list = keep_only_anomalies(node.children, -parent_anomaly_type)
                processed_nodes_list.extend(processed_children_list)
            else:
                pass

    return processed_nodes_list


def print_tree_from_node(input_node, p):
    if input_node and input_node.children and not input_node.printed:
        for pre, fill, node in RenderTree(input_node):
            node.printed = True
            print_anomaly(p, node, pre)


def print_revenue_rca(asset_df, p):
    rca_nodes_list = build_tree_with_all_metrics(asset_df, association_rules_root_nodes[0])
    rca_nodes_list = keep_only_anomalies(rca_nodes_list)

    for root_node in rca_nodes_list:
        print_tree_from_node(root_node, p)

