import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from itertools import combinations
#from surprise import KNNBasic, SVD, NormalPredictor, KNNBaseline,KNNWithMeans, KNNWithZScore, BaselineOnly, CoClustering, Reader, dataset, accuracy

#from sklearn.model_selection import GridSearchCV


def abhi(customerId, total_recommendation, input_list=[], min_support=0.001, min_threshold=0.5):
    data = pd.read_csv("product.csv").groupby(['CustomerId', 'ProductName'])['Length'].count().unstack().applymap(
        lambda x: int(x >= 0))
    frequent_itemsets = apriori(data, min_support, True)
    rules = association_rules(frequent_itemsets, "lift", min_threshold)
    product_list = list(data.loc[customerId][data.loc[customerId] == 1].index) + input_list
    subsets = [list(subset) for i in range(len(product_list) + 1) for subset in combinations(product_list, i)][1:]
    recommended_product = []
    for subset in subsets:
        rules_subset = rules[(rules['antecedents'].apply(lambda x: set(subset).issubset(set(x)))) & (
            rules['consequents'].apply(lambda x: len(x) == 1))]
        if not rules_subset.empty:
            best_rule = rules_subset[rules_subset['confidence'] == max(rules_subset['confidence'])].iloc[0]
            recommended_product.append(list(best_rule['consequents'])[0])
    X = data.loc[:, product_list].fillna(0)
    y = data.loc[:, recommended_product].fillna(0).sum(axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #param_grid = {'n_neighbors': [5, 10, 20, 30, 40]}

    # Create a KNN regressor object
    #knn = KNeighborsRegressor()
    #grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_root_mean_squared_error')

    # Fit the grid search object to the training data
    #grid_search.fit(X_train, y_train)
    #Hyperpa=grid_search.best_params_
   # rmse=  grid_search.best_score_

    knn = KNeighborsRegressor(n_neighbors=20)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)

    rmse = mean_squared_error(y_test, y_pred, squared=False)

    return recommended_product[:total_recommendation], rmse


'''recommended_products, rmse = abhi(56, 5)

print("Recommended products:", recommended_products)

print("RMSE:", rmse)'''

