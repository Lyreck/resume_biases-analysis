import pandas as pd
from sklearn.cluster import KMeans
import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn import cluster


df = pd.read_csv("../../data/dataframes/presentation_scores.csv")

## Compare mean scores
# between genders
print(df.groupby('gender', as_index = False).agg(mean_score = ("Score", 'mean')).sort_values(by = "mean_score", ascending = False))

# between ethnicities
print(df.groupby('ethnicity', as_index = False).agg(mean_score = ("Score", 'mean')).sort_values(by = "mean_score", ascending = False))

# compare british and non-british
print(f'british mean: {df[df["ethnicity"] == "british"][["Score"]].mean()}')
print(f'non-british mean: {df[df["ethnicity"] != "british"][["Score"]].mean()}')

X_train,y_train = df[["Score"]], df[["Score"]]
nc = 3
## KMeans
start_time = time.time()
kmeans = KMeans(n_clusters=nc, random_state=0, n_init=10).fit(X_train, y_train)
labels_KM = kmeans.labels_
elapsed_time_kmeans = time.time() - start_time
print(f"Kmeans: {round(elapsed_time_kmeans)} secondes d'exécution.")
##Elbow plot pour Kmeans:
# code pour afficher le "elbow plot"
inertie=np.zeros((10))
for K in range(1,11):
    clustering=cluster.KMeans(n_clusters=K, n_init=10)
    clustering.fit(X_train)
    inertie[K-1]=clustering.inertia_
plt.figure(figsize=[9,6]);
plt.plot(np.arange(1,11),inertie);
plt.xlabel("K");
plt.ylabel("inertie");
plt.title("elbow plot");
plt.show()

# Add the cluster labels to the original DataFrame
df["Cluster"] = kmeans.labels_


# Plot the data points with colors based on their cluster
plt.figure(figsize=(3, 2))
plt.scatter(df["Score"], np.zeros_like(df["Score"]), c=df["Cluster"], cmap='viridis', s=50)

# Add annotations for each point (e.g., Resume ID)
for i, resume_id in enumerate(df.index):  # Assuming the index represents the resume ID
    plt.annotate(str(resume_id), (df["Score"].iloc[i], 0), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)

plt.xlabel("Score")
plt.title("KMeans Clustering")
plt.colorbar(label="Cluster")
plt.show()