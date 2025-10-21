def get_product_category_map(df_transactions):
    """Creates a dictionary mapping Product Name to its Category."""
    return df_transactions[['Product Name', 'Product Category']].drop_duplicates().set_index('Product Name')['Product Category'].to_dict()

def precalculate_top_products(df_segmented):
    """Calculates and returns the top products per cluster (affinity score)."""
    top_products_per_cluster = (
        df_segmented.groupby(['Cluster', 'Product Name'])['Quantity']
        .sum()
        .reset_index()
        .sort_values(['Cluster', 'Quantity'], ascending=[True, False])
    )
    return top_products_per_cluster

def get_recommendations(cluster_id, purchased_product, rules_df, top_products_df, category_map):
    """Generates filtered recommendations based on category, Apriori, and Cluster Affinity."""
    recommendations = set()
    purchased_set = {purchased_product}
    
    purchased_category = category_map.get(purchased_product)
    if not purchased_category:
        return []
    
    # 1. Collaborative (Apriori) Rules - Filtered by Category
    antecedents_match = rules_df[rules_df['antecedents'].apply(lambda x: purchased_product in x)]
    
    for _, row in antecedents_match.iterrows():
        consequents_list = set(row['consequents'])
        for item in consequents_list:
            if category_map.get(item) == purchased_category:
                recommendations.add(item)
    
    # 2. Content-Based (Cluster Affinity) - Filtered by Category
    cluster_top_items = top_products_df[top_products_df['Cluster'] == cluster_id]['Product Name'].head(10).tolist()
    
    for item in cluster_top_items:
        if category_map.get(item) == purchased_category:
            recommendations.add(item)
    
    # 3. Final cleanup and scoring
    final_recommendations = [item for item in recommendations if item not in purchased_set]
    
    sorted_recs = sorted(final_recommendations, 
                         key=lambda x: top_products_df[(top_products_df['Cluster'] == cluster_id) & (top_products_df['Product Name'] == x)]['Quantity'].sum(), 
                         reverse=True)

    return sorted_recs[:5]