import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style for consistent visuals (Good for a visualization module)
sns.set_style("whitegrid")


def plot_cluster_profiles(df_customers):
    """Creates a bar plot of average RFM/Diversity metrics per cluster."""
    
    cluster_summary_avg = df_customers.groupby('Cluster').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'Product_Diversity': 'mean'
    }).reset_index()
    
    cluster_summary_melted = cluster_summary_avg.melt(id_vars='Cluster', var_name='Metric', value_name='Value')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=cluster_summary_melted, x='Cluster', y='Value', hue='Metric', palette='viridis', ax=ax)
    ax.set_title('Cluster Profiles: Average RFM/Diversity Metrics')
    ax.set_xlabel("Cluster ID")
    ax.set_ylabel("Average Value")
    plt.tight_layout()
    return fig


def plot_all_cluster_top_products(top_products_df, top_n_products=3):
    """
    Creates a bar plot showing the top N products for ALL clusters (Consolidated View).
    """
    
    # Get the top N products for each cluster
    top_n_per_cluster = top_products_df.groupby('Cluster').head(top_n_products)
    
    # Sort by quantity within each cluster
    top_n_per_cluster = top_n_per_cluster.sort_values(by=['Cluster', 'Quantity'], ascending=[True, False])
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    sns.barplot(
        data=top_n_per_cluster,
        x='Cluster',
        y='Quantity',
        hue='Product Name',
        palette='tab20',
        ax=ax,
        dodge=True 
    )
    
    ax.set_title(f'Top {top_n_products} Products Purchased per Cluster (Consolidated View)')
    ax.set_xlabel('Cluster ID')
    ax.set_ylabel('Total Quantity Purchased')
    ax.legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig


def plot_top_products_single_cluster(top_products_df, selected_cluster, top_n=5):
    """Creates a bar plot of top N products for a specific cluster."""
    
    top_n_for_selected_vis = top_products_df[top_products_df['Cluster'] == selected_cluster].head(top_n)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_n_for_selected_vis, x='Product Name', y='Quantity', hue='Product Name', 
                palette='tab20', ax=ax, legend=False) 
    ax.set_title(f'Top {top_n} Affinity Products for Cluster {selected_cluster}')
    ax.set_xlabel("Product Name")
    ax.set_ylabel("Total Quantity Purchased")
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    return fig
    

def plot_association_rules(rules_df):
    """Creates a scatter plot of association rules (Support vs Confidence)."""
    
    rules_display = rules_df.head(20)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=rules_display, x='support', y='confidence', size='lift', hue='lift', 
                    palette='viridis', sizes=(50, 400), alpha=0.7, ax=ax)
    ax.set_title('Product Association Network: Top Rules (Support vs Confidence)')
    ax.set_xlabel('Support')
    ax.set_ylabel('Confidence')
    ax.legend(title='Lift', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig

# NOTE: Ensure you remove ALL standalone code (data loading, K-Means, etc.) 
# from your actual Visualize.py file, keeping only these function definitions.