branch_hits = {}

def record_branch_call(branch):
    branch_hits[branch] = branch_hits.get(branch, 0) + 1

def get_heatmap():
    return sorted(branch_hits.items(), key=lambda x: x[1], reverse=True)
