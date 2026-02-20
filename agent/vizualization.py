import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def visualize_groups(groups, output_path="data/outputs/clusters.png"):
    """
    Creates a simple 2D PCA visualization of grouped claim embeddings.
    Saves the plot as an image.
    """

    vectors = []
    labels = []

    for i, group in enumerate(groups):
        if group.vector is not None:
            vectors.append(group.vector)
            labels.append(f"Theme {i+1}")

    if len(vectors) < 2:
        print("Not enough groups to visualize.")
        return

    vectors = np.array(vectors)

    # Reduce to 2D
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(vectors)

    plt.figure(figsize=(8, 6))
    plt.scatter(reduced[:, 0], reduced[:, 1])

    for i, label in enumerate(labels):
        plt.text(reduced[i, 0], reduced[i, 1], label)

    plt.title("Claim Group Clusters (PCA)")
    plt.xlabel("Component 1")
    plt.ylabel("Component 2")

    os.makedirs("data/outputs", exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    print(f"Cluster visualization saved to {output_path}")