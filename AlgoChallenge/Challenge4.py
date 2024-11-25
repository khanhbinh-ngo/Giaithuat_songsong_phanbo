from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


def parallel_dfs(graph, nodes, visited, stack=None, reverse=False):
    """
    Chạy DFS song song trên các node được phân chia.
    """
    local_stack = [] if stack is not None else None

    def dfs(node):
        nonlocal local_stack
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)
        if local_stack is not None:
            local_stack.append(node)

    for node in nodes:
        if not visited[node]:
            dfs(node)

    return local_stack if stack is not None else None


def kosaraju_parallel(n, edges, max_workers=4):
    """
    Tìm số lượng SCCs sử dụng thuật toán Kosaraju với xử lý song song.
    """
    # Xây dựng đồ thị gốc và đồ thị lật ngược
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        reverse_graph[v].append(u)

    # Bước 1: Duyệt DFS trên đồ thị gốc để lấy thứ tự hoàn thành
    visited = [False] * n
    stack = []

    # Phân chia các node để chạy song song
    node_groups = [list(range(i, n, max_workers)) for i in range(max_workers)]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Chạy DFS song song
        futures = [executor.submit(parallel_dfs, graph, group, visited, True) for group in node_groups]
        results = [future.result() for future in futures]

    # Kết hợp kết quả từ các nhóm
    for partial_stack in results:
        stack.extend(partial_stack)

    # Bước 2: Duyệt DFS trên đồ thị lật ngược theo thứ tự hoàn thành
    visited = [False] * n
    scc_count = 0

    while stack:
        node = stack.pop()
        if not visited[node]:
            # Chạy DFS song song để đếm SCC
            parallel_dfs(reverse_graph, [node], visited)
            scc_count += 1

    return scc_count


def MAIN(input_file_path):
    """
    Đọc dữ liệu từ file, tính số SCCs cho mỗi quốc gia bằng Kosaraju song song và trả về kết quả.
    """
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    Q = int(lines[0].strip())  # Số quốc gia
    index = 1
    results = []

    for _ in range(Q):
        # Đọc số thành phố (N) và số tuyến đường (M)
        N, M = map(int, lines[index].strip().split())
        index += 1

        # Đọc danh sách các tuyến đường
        edges = []
        for __ in range(M):
            u, v = map(int, lines[index].strip().split())
            edges.append((u - 1, v - 1))  # Chuyển từ 1-based index về 0-based index
            index += 1

        # Tính số SCCs bằng Kosaraju song song
        scc_count = kosaraju_parallel(N, edges)
        results.append(scc_count)
    
    # Trả về kết quả dưới dạng chuỗi
    return '\n'.join(map(str, results))


#
# Giải thích thuật toán
# 
# 
# #