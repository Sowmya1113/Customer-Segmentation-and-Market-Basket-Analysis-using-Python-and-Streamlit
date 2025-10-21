import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def generate_association_rules(df_segmented):
    """Performs Market Basket Analysis on the segmented transaction data."""
    
    basket = (
        df_segmented.groupby(['Transaction ID', 'Product Name'])['Quantity']
        .sum().unstack().reset_index().fillna(0).set_index('Transaction ID')
    )

    basket = basket.map(lambda x: 1 if x > 0 else 0).astype(bool)

    frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1.0)
    rules = rules.sort_values(by='lift', ascending=False)
    
    return rules

# NOTE: Remove all printing and plotting from this file.