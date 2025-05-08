import pandas as pd
from sklearn.cluster import KMeans
from sklearn import cluster
import time
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

from graph_generation import concatenate_dataframes_with_jobtype



def generate_kmeans_graph(df):

    X_train,y_train = df[["Score"]], df[["Score"]]
    nc = 3 #TO DEFINE WITH ELBOW PLOT

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

def elbow_plot(X_train):
    # code pour afficher le "elbow plot"
    inertie=np.zeros((10))
    for K in range(1,11):
        clustering=cluster.KMeans(n_clusters=K, n_init=10)
        clustering.fit(X_train)
        inertie[K-1]=clustering.inertia_
    return inertie
    plt.figure(figsize=[9,6]);
    plt.plot(np.arange(1,11),inertie);


def kmeans_name(df, experiment_name, adapted_or_clivant = 'adapted', nc=[]):
    """
    Perform KMeans clustering on the provided DataFrame and generate elbow plots and KMeans graphs for each job type.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data to be clustered. Should be the one obtained by the concatenation function.
        experiment_name (str): The name of the experiment (e.g., "name", "volunteering", "job").
        adapted_or_clivant (str): The column name indicating whether the data is adapted or clivant. Default is 'adapted' (for experiments "name" and "volunteering").
        nc (dict): A dictionary containing the number of clusters for each job type. If empty, elbow plots will be generated to determine the number of clusters."""

    #create elbow plot for each job type on a grid
    print_elbow = (nc == []) #if number of clusters are not defined, we have to determine them with elbow plots.
    if print_elbow:
        fig, axes = plt.subplots(3,2)
        fig.suptitle(f'Elbow plots for the {experiment_name} experiment - each plot has two graphs: adapted/clivant and not adapted/clivant.')

        # Flatten the 2D array of axes for easier indexing
        axes = axes.flatten()

        for i,job_type in enumerate(df['job_type'].unique()):
            ax = axes[i]

            experiment_adapted = df[(df['job_type'] == job_type) & (df[adapted_or_clivant] == 1)].copy()
            experiment_not_adapted = df[(df['job_type'] == job_type) & (df[adapted_or_clivant] == 0)].copy()
            inertie_adapted = elbow_plot(experiment_adapted[["Score"]])
            inertie_not_adapted = elbow_plot(experiment_not_adapted[["Score"]])

            ax.plot(np.arange(1, 11), inertie_adapted, label=f"Adapted/Clivant: {job_type}")
            ax.plot(np.arange(1, 11), inertie_not_adapted, label=f"Not adapted/clivant: {job_type}")

            ax.set_xlabel("K")
            ax.set_ylabel("Inertia")
            ax.set_title(f"Elbow Plot for Job Type: {job_type}")
            ax.legend()

        # Hide any unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])
        
        # Adjust layout and show the grid of plots
        plt.tight_layout()
        plt.show()

    else: 
        fig, axes = plt.subplots(6,1, figsize=(15, 10), constrained_layout=True) 
        fig.suptitle(f'k-means for the {experiment_name} experiment.')

        fig2, axes2 = plt.subplots(6,1, figsize=(15, 10), constrained_layout=True) 
        fig2.suptitle(f'k-means for the {experiment_name} experiment.')

        # Flatten the 2D array of axes for easier indexing
        axes = axes.flatten()
        #create kmeans graph for each job type on a grid
        for i,job_type in enumerate(df['job_type'].unique()):
            ax = axes[i] #axes for gender graph
            ax2 = axes2[i] #axes for ethnicity graph

            #Recover necessary data for kmeans
            nc_adapted = nc[job_type][0]
            nc_not_adapted = nc[job_type][1]

            experiment_adapted = df[(df['job_type'] == job_type) & (df[adapted_or_clivant] == 1)].copy()
            experiment_not_adapted = df[(df['job_type'] == job_type) & (df[adapted_or_clivant] == 0)].copy()
            inertie_adapted = elbow_plot(experiment_adapted[["Score"]])
            inertie_not_adapted = elbow_plot(experiment_not_adapted[["Score"]])

            experiment_adapted = experiment_adapted.reset_index(drop=True)
            experiment_not_adapted = experiment_not_adapted.reset_index(drop=True) #to keep the index aligned with kmeans.
            X_train_adapted = experiment_adapted[["Score"]]
            X_train_not_adapted = experiment_not_adapted[["Score"]]

            # Perform KMeans clustering
            kmeans_adapted = KMeans(n_clusters=nc_adapted, random_state=0, n_init=10).fit(X_train_adapted, X_train_adapted)
            labels_KM_adapted = kmeans_adapted.labels_
            experiment_adapted["Cluster"] = labels_KM_adapted #add labels to the dataframe (DOES THIS CHANGE THE ORDER ?)

            kmeans_not_adapted = KMeans(n_clusters=nc_not_adapted, random_state=0, n_init=10).fit(X_train_not_adapted, X_train_not_adapted)
            labels_KM_not_adapted = kmeans_not_adapted.labels_
            experiment_not_adapted["Cluster"] = labels_KM_not_adapted #add labels to the dataframe

            #add plot to the grid (adapted and not adapted)
            # ax.scatter(X_train_adapted, np.zeros_like(X_train_adapted), c=labels_KM_adapted, cmap='viridis', s=50)
            # ax.scatter(X_train_not_adapted, np.ones_like(X_train_not_adapted), c=labels_KM_not_adapted, cmap='plasma', s=50)


            if experiment_name == "name":
                ############################## Gender analysis ##############################
                plot_data(experiment_adapted, 'gender', True, ax)
                # Scatter plot for not adapted data
                plot_data(experiment_not_adapted, 'gender', False, ax)

                ############################## Ethnicity analysis ##############################
                plot_data(experiment_adapted, 'british', True, ax2)
                # Scatter plot for not adapted data
                plot_data(experiment_not_adapted, 'british', False, ax2)


                ################################################################################
                # Create a custom legend for marker shapes
                legend_elements_gender = [
                    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='Male'),
                    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markersize=10, label='Female'),
        ]

                # Add the custom legend to the plot
                ax.legend(handles=legend_elements_gender, title="Gender", loc="upper right")
                ax.set_xlabel("Score")
                ax.set_ylabel("Adapted (0) / Not Adapted (1)")
                ax.set_title(f"K-Means for Job Type: {job_type}")

                legend_elements_british = [
                    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='British'),
                    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markersize=10, label='Non-British'),
        ]

                ax2.legend(handles=legend_elements_british, title="Origin", loc="upper right")
                ax2.set_xlabel("Score")
                ax2.set_ylabel("Adapted (0) / Not Adapted (1)")
                ax2.set_title(f"K-Means for Job Type: {job_type}")
            
            if experiment_name == "volunteering":
                plot_data(experiment_adapted, 'ideology', True, ax) # ideology is not implemented yet.
                # Scatter plot for not adapted data
                plot_data(experiment_not_adapted, 'ideology', False, ax)

                ax.set_xlabel("Score")
                ax.set_ylabel("Adapted (0) / Not Adapted (1)")
                ax.set_title(f"K-Means for Job Type: {job_type}")
                ax.legend()

            if experiment_name == "job":
                plot_data(experiment_adapted, 'comp_type', True, ax) # ideology is not implemented yet.
                # Scatter plot for not adapted data
                plot_data(experiment_not_adapted, 'comp_type', False, ax)

                ax.set_xlabel("Score")
                ax.set_ylabel("Clivant (0) / Not Clivant (1)")
                ax.set_title(f"K-Means for Job Type: {job_type}")
                ax.legend()



        # Hide any unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])
        
        # Adjust layout and show the grid of plots
        # plt.tight_layout()
        plt.show()


def plot_data(experiment, gender_or_british, adapted_clivant, ax): #can also add for ideology (later)
    """
    Plot the data points with colors based on their cluster, and annotated according to ethnicity or gender.
    """

    for annotation, marker in zip([0, 1], ['o', 's']):  # Use 'o' for one gender/ethnicity and 's' for the other
            if gender_or_british in ['gender', 'british']:
                annotation_data = experiment[experiment[gender_or_british] == annotation]
            elif gender_or_british == 'ideology':
                annotation_data = experiment #we could look at the ideology, or the "clivant" aspect, but we have not put this in the data yet.
            elif gender_or_british == 'comp_type':
                annotation_data = experiment
            #     annotation_data = experiment[experiment[gender_or_british] == annotation] # to check for company type (later).

            if adapted_clivant: #in the case where the data is adapted (experiments name and volunteering) or clivant (experiment job), print on first line.
                ax.scatter(
                    annotation_data["Score"],
                    np.zeros_like(annotation_data["Score"]),
                    c=annotation_data["Cluster"], #experiment[experiment[gender_or_british] == experiment]["Cluster"],
                    cmap='viridis',
                    s=10,
                    marker=marker
                )

            else: #in the case if not adapted, or not clivant => we want to plot the data on the second line
                ax.scatter(
                    annotation_data["Score"],
                    np.ones_like(annotation_data["Score"]),
                    c=annotation_data["Cluster"], #experiment[experiment[gender_or_british] == experiment]["Cluster"],
                    cmap='viridis',
                    s=10,
                    marker=marker
                )



if __name__ == "__main__":

    ################# Name experiment #################
    folder_path_name = "data/scores_experiments/name/"
    df_name = concatenate_dataframes_with_jobtype(folder_path_name)
    print(df_name.describe())

    nc_names = {"SoftwareEng": [4,4], "ItOfficer": [3,4], "Nurse": [5,4], "AdminAssistant": [4,4], "Doctor": [4,3], "Teacher": [4,3]} #in the list: [adapted, not adapted]
    kmeans_name(df_name, nc=nc_names, experiment_name="name")


    ################# Volunteering experiment #################
    folder_path_volunteering = "data/scores_experiments/volunteering/"
    df_volunteering = concatenate_dataframes_with_jobtype(folder_path_volunteering)

    nc_volunteering = {"SoftwareEng": [3,4], "ItOfficer": [3,3], "Nurse": [2,3], "AdminAssistant": [3,3], "Doctor": [3,4], "Teacher": [3,4]} #in the list: [adapted, not adapted]
    kmeans_name(df_volunteering, nc=nc_volunteering, experiment_name="volunteering") # need ideology to interpret.

    ################# Job experiment #################
    folder_path_job = "data/scores_experiments/job/"
    df_job = concatenate_dataframes_with_jobtype(folder_path_job)

    nc_job = {"SoftwareEng": [2,2], "ItOfficer": [3,3], "Nurse": [2,2], "AdminAssistant": [3,3], "Doctor": [3,3], "Teacher": [3,4]} #in the list: [clivant, not clivant]
    kmeans_name(df_job, experiment_name = 'job', nc = nc_job, adapted_or_clivant = 'clivant')



    giga_df = pd.concat([df_name, df_volunteering, df_job], ignore_index=True)
    print(giga_df.describe())







