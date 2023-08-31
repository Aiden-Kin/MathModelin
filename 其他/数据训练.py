from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Preparing the data from ChemicalData.xlsx

# Filtering out rows with missing '类型'
known_type_df = chemical_data_df.dropna(subset=['类型'])

# Features and target variable
X = known_type_df.iloc[:, 6:].fillna(0)  # Chemical composition columns and filling NaN with 0
y = known_type_df['类型']

# Splitting the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scaling the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training a Random Forest Classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train_scaled, y_train)

# Predicting on test set to check accuracy
y_pred = clf.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)