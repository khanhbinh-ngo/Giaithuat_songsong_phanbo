import concurrent.futures
import math

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def closest_pair_in_strip(strip, d):
    strip.sort(key=lambda point: point[1])  # Sắp xếp theo tọa độ y
    min_dist = d
    n = len(strip)
    for i in range(n):
        for j in range(i + 1, n):
            if (strip[j][1] - strip[i][1]) >= min_dist:
                break
            dist = euclidean_distance(strip[i], strip[j])
            min_dist = min(min_dist, dist)
    return min_dist

def closest_pair(points):
    def divide_and_conquer(points_sorted_x):
        n = len(points_sorted_x)
        if n <= 3:
            min_dist = float("inf")
            for i in range(n):
                for j in range(i + 1, n):
                    min_dist = min(min_dist, euclidean_distance(points_sorted_x[i], points_sorted_x[j]))
            return min_dist
        mid = n // 2
        left_points = points_sorted_x[:mid]
        right_points = points_sorted_x[mid:]

        d1 = divide_and_conquer(left_points)
        d2 = divide_and_conquer(right_points)

        d = min(d1, d2)

        mid_x = points_sorted_x[mid][0]
        strip = [point for point in points_sorted_x if abs(point[0] - mid_x) < d]
        d_strip = closest_pair_in_strip(strip, d)

        return min(d, d_strip)

    return divide_and_conquer(sorted(points, key=lambda p: p[0]))

def process_map(points):
    return closest_pair(points)

def MAIN(filename='input.txt', output_file = 'output.txt'):
    with open(filename, 'r') as file:
        data = file.readlines()

    Q = int(data[0])  # Số bản đồ
    results = []
    index = 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(Q):
            N = int(data[index])  # Số địa điểm
            points = []
            for i in range(index + 1, index + 1 + N):
                x, y = map(int, data[i].strip().split())
                points.append((x, y))
            index += 1 + N
            futures.append(executor.submit(process_map, points))

        results = [f"{future.result():.4f}" for future in futures]
    # return results
    # Ghi kết quả ra file
    with open(output_file, 'w') as file:
        file.write("\n".join(results))

# Chạy thử
if __name__ == "__main__":
    MAIN("AlgoChallenge\input.txt", "AlgoChallenge\output.txt")
    # MAIN("AlgoChallenge\input.txt")