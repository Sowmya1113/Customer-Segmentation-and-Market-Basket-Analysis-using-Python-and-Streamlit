import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
def perform_segmentation(df_raw, optimal_k=4):
    """Performs RFM and Product Diversity based Customer Segmentation using K-Means."""
    df = df_raw.copy()
    df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'])
    reference_date = df['Date of Purchase'].max() + pd.Timedelta(days=1)

    customer_features = df.groupby('Customer ID').agg({
        'Date of Purchase': lambda x: (reference_date - x.max()).days, # Recency
        'Transaction ID': 'nunique', # Frequency
        'Price': 'sum', # Monetary
        'Product ID': 'nunique' # Product diversity
    }).reset_index()

    customer_features.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary', 'Product_Diversity']

    # Normalization
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(customer_features[['Recency', 'Frequency', 'Monetary', 'Product_Diversity']])

    # Apply K-Means Clustering
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init='auto')
    customer_features['Cluster'] = kmeans.fit_predict(scaled_features)
    
    # Merge cluster info back to raw data
    segmentation_results = customer_features[['Customer ID', 'Cluster']].drop_duplicates()
    df_segmented = pd.merge(df_raw, segmentation_results, on='Customer ID', how='left')
    
    # Return both the segmented transaction data and the customer feature summary
    return df_segmented, customer_features

# NOTE: The data is loaded in dashboard.py and passed to this function. 
# Do NOT include a pd.read_csv() call here.