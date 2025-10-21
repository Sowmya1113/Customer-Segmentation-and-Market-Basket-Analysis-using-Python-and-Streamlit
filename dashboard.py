import streamlit as st
import pandas as pd
# Import functions from your separate files
# NOTE: Ensure the casing and structure here (e.g., Customer_segmentation.customer_seg) 
# match the actual folder and file names in your project exactly.
from Customer_segmentation.customer_seg import perform_segmentation
from Market_Basket_Analysis.MBA import generate_association_rules
from Integration.CS_MBA import precalculate_top_products, get_product_category_map, get_recommendations
# Updated import: Using plot_all_cluster_top_products instead of plot_top_products_single_cluster
from Integration.Visualize import plot_cluster_profiles, plot_all_cluster_top_products, plot_association_rules 
# from Integration.Visualize import plot_cluster_profiles, plot_top_products_single_cluster, plot_association_rules # If you kept the single-plot function

# --- 1. Page Configuration and Data Processing ---
st.set_page_config(page_title="Modular Customer Segmentation Dashboard", layout="wide")
st.title("Customer Segmentation and Market Basket Analysis using Python and Streamlit")
st.markdown("---")

@st.cache_data
def load_and_process_all_data(file_path):
    """Loads data and orchestrates all backend processing."""
    df_raw = pd.read_csv(file_path)
    
    # 1. SEGMENTATION (from customer_seg.py)
    df_segmented, df_customers = perform_segmentation(df_raw.copy())
    
    # 2. MBA RULES (from MBA.py)
    association_rules_df = generate_association_rules(df_segmented)
    
    # 3. RECOMMENDATION PRE-CALC (from CS_MBA.py)
    top_products_per_cluster_df = precalculate_top_products(df_segmented)
    product_category_map = get_product_category_map(df_segmented)
    
    return df_segmented, df_customers, association_rules_df, top_products_per_cluster_df, product_category_map

# Load all data and processing results
try:
    df_transactions, df_customers, association_rules_df, top_products_per_cluster_df, product_category_map = load_and_process_all_data('customer_purchase_data.csv')
    num_customers = df_customers['Customer ID'].nunique()
except FileNotFoundError:
    st.error("Error: 'customer_purchase_data.csv' not found. Please run 'dataset.py' first.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred during data processing: {e}")
    st.stop()


# --- SIDEBAR: Recommendation Search Engine (Uses CS_MBA.py logic) ---
st.sidebar.header("🔍 Recommendation Search Engine")
product_list = sorted(df_transactions['Product Name'].unique().tolist())

search_cluster = st.sidebar.selectbox("Select Customer's Cluster:", sorted(df_customers['Cluster'].unique()))
search_product = st.sidebar.selectbox("Customer Purchased Product:", product_list)

if st.sidebar.button("Generate Recommendation"):
    recs = get_recommendations(search_cluster, search_product, association_rules_df, top_products_per_cluster_df, product_category_map)
    
    st.sidebar.markdown("### Search Results")
    st.sidebar.markdown(f"**Based on Cluster {search_cluster} and purchase of `{search_product}`:**")
    
    if recs:
        st.sidebar.success("Top Recommendations:")
        for i, item in enumerate(recs):
            st.sidebar.write(f"{i+1}. {item}")
    else:
        st.sidebar.info("No strong *intra-category* association or cluster affinity found.")

st.sidebar.markdown("---")

# Removed the 'Cluster Explorer' sidebar select box as it's no longer needed for the main affinity plot


# --- MAIN DASHBOARD CONTENT ---

# 1. Customer Segmentation Table (K-Means Output)
st.header("1. Customer Segmentation Table")
st.caption(f"Segmentation of {num_customers} customers based on Recency, Frequency, Monetary, and Product Diversity.")

# Create display table 
cluster_summary_table = df_customers.groupby('Cluster').agg(
    Count=('Customer ID', 'count'),
    Avg_Recency=('Recency', 'mean'),
    Avg_Frequency=('Frequency', 'mean'),
    Avg_Monetary=('Monetary', 'mean'),
    Avg_Diversity=('Product_Diversity', 'mean')
).reset_index()

# [Simplified Segment Naming Logic for display]
cluster_summary_table['Count (%)'] = (cluster_summary_table['Count'] / num_customers * 100).round(1)
st.dataframe(cluster_summary_table.set_index('Cluster'), use_container_width=True)


# 2. Cluster Profiles Visualization (Uses visualize.py)
st.header("2. Cluster Profiles Visualization")
fig_profile = plot_cluster_profiles(df_customers)
st.pyplot(fig_profile)
st.markdown("---")

# 3. Top Product Affinity (NEW CONSOLIDATED CHART)
st.header(f"3. Top Product Affinity Across All Clusters")
st.caption("Shows the top 3 most frequently bought products for each segment.")
# Call the new consolidated plotting function
fig_all_top_products = plot_all_cluster_top_products(top_products_per_cluster_df, top_n_products=3)
st.pyplot(fig_all_top_products)
st.markdown("---")


# 4. Market Basket Association Rules Overview (Uses visualize.py)
st.header("4. Market Basket Association Rules (Apriori)")
st.caption("The strongest global associations, useful for cross-selling and bundling.")

rules_display = association_rules_df[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10)
rules_display['antecedents'] = rules_display['antecedents'].apply(lambda x: ', '.join(list(x)))
rules_display['consequents'] = rules_display['consequents'].apply(lambda x: ', '.join(list(x)))
rules_display = rules_display.rename(columns={'antecedents': 'IF Product(s)', 'consequents': 'THEN Product(s)'})

# Display the rules table and the visualization chart
col1, col2 = st.columns([1.5, 1])
with col1:
    st.subheader("Top 10 Rules Table")
    st.dataframe(rules_display, use_container_width=True)

with col2:
    st.subheader("Rules Chart (Support vs Confidence)")
    fig_rules = plot_association_rules(association_rules_df)
    st.pyplot(fig_rules)

st.success("✅ Dashboard successfully built by linking modules! Run using `streamlit run dashboard.py`")