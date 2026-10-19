"""
=============================================================================
AIML PRACTICAL LAB - ALL-IN-ONE EXPERIMENTS CHEATSHEET FOR SPYDER
No external CSV needed! Uses in-built datasets so zero-error execution.
Run any section directly with F9 (selection) or full file with F5.
=============================================================================
"""

# =============================================================================
# 1. FIND-S ALGORITHM (Concept Learning)
# =============================================================================
def run_find_s():
    # Sample training data: [Sky, Temp, Humidity, Wind, Water, Forecast, EnjoySport]
    data = [
        ['Sunny', 'Warm', 'Normal', 'Strong', 'Warm', 'Same', 'Yes'],
        ['Sunny', 'Warm', 'High',   'Strong', 'Warm', 'Same', 'Yes'],
        ['Rainy', 'Cold', 'High',   'Strong', 'Warm', 'Change', 'No'],
        ['Sunny', 'Warm', 'High',   'Strong', 'Cool', 'Change', 'Yes']
    ]
    # Initialize most specific hypothesis
    h = ['0'] * (len(data[0]) - 1)
    for row in data:
        if row[-1] == 'Yes':
            for i in range(len(h)):
                if h[i] == '0':
                    h[i] = row[i]
                elif h[i] != row[i]:
                    h[i] = '?'
    print("Find-S Final Hypothesis:", h)


# =============================================================================
# 2. CANDIDATE ELIMINATION ALGORITHM
# =============================================================================
def run_candidate_elimination():
    data = [
        ['Sunny', 'Warm', 'Normal', 'Strong', 'Warm', 'Same', 'Yes'],
        ['Sunny', 'Warm', 'High',   'Strong', 'Warm', 'Same', 'Yes'],
        ['Rainy', 'Cold', 'High',   'Strong', 'Warm', 'Change', 'No'],
        ['Sunny', 'Warm', 'High',   'Strong', 'Cool', 'Change', 'Yes']
    ]
    num_features = len(data[0]) - 1
    S = ['0'] * num_features
    G = [['?' for _ in range(num_features)]]

    for row in data:
        features, label = row[:-1], row[-1]
        if label == 'Yes':
            for i in range(num_features):
                if S[i] == '0': S[i] = features[i]
                elif S[i] != features[i]: S[i] = '?'
            G = [g for g in G if all(g[i] == '?' or g[i] == S[i] for i in range(num_features))]
        else:
            new_G = []
            for g in G:
                for i in range(num_features):
                    if g[i] == '?' and S[i] != '?' and S[i] != features[i]:
                        h = g.copy()
                        h[i] = S[i]
                        new_G.append(h)
            G = new_G
    print("Specific Boundary S:", S)
    print("General Boundary G:", G)


# =============================================================================
# 3. A* SEARCH ALGORITHM
# =============================================================================
def run_a_star():
    import heapq
    # Graph: node -> list of (neighbor, edge_cost)
    graph = {
        'A': [('B', 1), ('C', 3)],
        'B': [('D', 1), ('E', 5)],
        'C': [('D', 1), ('E', 2)],
        'D': [('E', 1)],
        'E': []
    }
    # Heuristic estimates to goal 'E'
    h = {'A': 4, 'B': 2, 'C': 2, 'D': 1, 'E': 0}

    start, goal = 'A', 'E'
    pq = [(h[start], 0, start, [start])] # (f, g, current_node, path)
    visited = set()

    while pq:
        f, g, u, path = heapq.heappop(pq)
        if u == goal:
            print("A* Shortest Path to Goal:", path, "with Total Cost:", g)
            return
        if u in visited: continue
        visited.add(u)
        for v, cost in graph[u]:
            new_g = g + cost
            heapq.heappush(pq, (new_g + h[v], new_g, v, path + [v]))


# =============================================================================
# 4. DECISION TREE (ID3 / CART)
# =============================================================================
def run_decision_tree():
    from sklearn.datasets import load_iris
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = DecisionTreeClassifier(criterion='entropy')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Decision Tree Accuracy:", accuracy_score(y_test, y_pred))


# =============================================================================
# 5. NAIVE BAYES CLASSIFIER
# =============================================================================
def run_naive_bayes():
    from sklearn.datasets import load_iris
    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Naïve Bayes Accuracy:", accuracy_score(y_test, y_pred))


# =============================================================================
# 6. K-NEAREST NEIGHBORS (KNN)
# =============================================================================
def run_knn():
    from sklearn.datasets import load_iris
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    print("KNN Accuracy (k=3):", accuracy_score(y_test, y_pred))


# =============================================================================
# 7. K-MEANS CLUSTERING (Unsupervised)
# =============================================================================
def run_kmeans():
    from sklearn.datasets import load_iris
    from sklearn.cluster import KMeans

    X, _ = load_iris(return_X_y=True)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X)
    print("Cluster Centers Shape:", kmeans.cluster_centers_.shape)
    print("Cluster Labels for first 10 samples:", kmeans.labels_[:10])


# =============================================================================
# 8. LINEAR REGRESSION
# =============================================================================
def run_linear_regression():
    from sklearn.linear_model import LinearRegression
    import numpy as np

    # Simple 2D feature / target
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([2, 4, 6, 8, 10])

    reg = LinearRegression()
    reg.fit(X, y)
    pred = reg.predict([[6]])
    print("Linear Regression Slope (m):", reg.coef_[0], "Intercept (c):", reg.intercept_)
    print("Prediction for input 6:", pred[0])


# =============================================================================
# 9. ARTIFICIAL NEURAL NETWORK / BACKPROPAGATION (MLP)
# =============================================================================
def run_ann():
    from sklearn.datasets import load_iris
    from sklearn.neural_network import MLPClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlp = MLPClassifier(hidden_layer_sizes=(10,), max_iter=500, random_state=42)
    mlp.fit(X_train, y_train)
    y_pred = mlp.predict(X_test)
    print("ANN / MLP Accuracy:", accuracy_score(y_test, y_pred))


# =============================================================================
# MAIN TEST DRIVER
# =============================================================================
if __name__ == "__main__":
    print("--- 1. FIND-S ---")
    run_find_s()
    print("\n--- 2. CANDIDATE ELIMINATION ---")
    run_candidate_elimination()
    print("\n--- 3. A* SEARCH ---")
    run_a_star()
    print("\n--- 4. DECISION TREE ---")
    run_decision_tree()
    print("\n--- 5. NAIVE BAYES ---")
    run_naive_bayes()
    print("\n--- 6. KNN ---")
    run_knn()
    print("\n--- 7. K-MEANS ---")
    run_kmeans()
    print("\n--- 8. LINEAR REGRESSION ---")
    run_linear_regression()
    print("\n--- 9. ANN BACKPROPAGATION ---")
    run_ann()
