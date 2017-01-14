def calculate_error(df):
    """
    Calculate the error for the
    each node
    """
    err = sum(df[df.columns[0]]) - max(df[df.columns[0]])
    return (err+0.5)/sum(df[df.columns[0]])

def prune_tree(tree, prune_dict):
    """
    This function helps to prune the
    given tree and returns the pruned tree.
    """

    for i in tree:
        if isinstance(tree[i]["Left"], set) and not isinstance(tree[i]["Right"], set):
            return prune_tree(tree[i]["Right"], prune_dict)
        elif not isinstance(tree[i]["Left"], set) and isinstance(tree[i]["Right"], set):
            return prune_tree(tree[i]["Left"], prune_dict)
        elif not isinstance(tree[i]["Left"], set) and not isinstance(tree[i]["Right"], set):
            node_error = calculate_error(prune_dict[i].groupby(by='Class').count())
            # function call to calculate peesimistic node error
            left_df = prune_dict[tree[i]["Left"].keys()[0]].groupby(by='Class').count()
            # left hand split of data
            right_df = prune_dict[tree[i]["Right"].keys()[0]].groupby(by='Class').count()
            # right hand split of data
            left_err = sum(left_df[left_df.columns[0]]) - max(left_df[left_df.columns[0]])
            # left hand data error
            right_err = sum(right_df[right_df.columns[0]]) - max(right_df[right_df.columns[0]])
            # right hand data error
            total = sum(left_df[left_df.columns[0]]) + sum(right_df[right_df.columns[0]])
            total_err = (left_err+right_err+1)/total
            # total count
            if node_error < total_err:
                data = tree[i].groupby(by='Class').count()
                tree[i] = data[data.columns[1]].argmax()
            else:
                pass
            prune_tree(tree[i]["Right"], prune_dict)
            prune_tree(tree[i]["Left"], prune_dict)
        else:
            pass
    return tree
