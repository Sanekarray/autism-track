import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import joblib

# Charger les données
data = pd.read_csv('C:/Users/cyrin/PycharmProjects/autismproject/data_autism.csv')

# Conserver uniquement les colonnes pertinentes pour l'entraînement
training_columns = [col for col in data.columns if col not in ['result', 'id_patient']]
X = data[training_columns].copy()
y = data['result'].apply(lambda x: 1 if x >= 6 else 0)

# Imputer les valeurs manquantes pour les données numériques
numeric_columns = X.select_dtypes(include=['int64', 'float64']).columns
X[numeric_columns] = X[numeric_columns].astype(float)  # Cast to float
numeric_imputer = SimpleImputer(strategy='mean')
X.loc[:, numeric_columns] = numeric_imputer.fit_transform(X[numeric_columns])

# Imputer les valeurs manquantes pour les données catégoriques
categorical_columns = X.select_dtypes(include=['object']).columns
categorical_imputer = SimpleImputer(strategy='most_frequent')
X.loc[:, categorical_columns] = categorical_imputer.fit_transform(X[categorical_columns])

# Encoder les variables catégoriques
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    X.loc[:, col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Standardiser les variables numériques
scaler = StandardScaler()
X.loc[:, numeric_columns] = scaler.fit_transform(X[numeric_columns])

# Entraîner le modèle SVM
model = SVC(probability=True, random_state=42)
model.fit(X, y)

# Sauvegarder le modèle et les transformateurs
joblib.dump(model, 'C:/Users/cyrin/PycharmProjects/autismproject/templates/autism_svm_model.pkl')
joblib.dump(label_encoders, 'C:/Users/cyrin/PycharmProjects/autismproject/templates/label_encoders.pkl')
joblib.dump(scaler, 'C:/Users/cyrin/PycharmProjects/autismproject/templates/scaler.pkl')
joblib.dump(training_columns, 'C:/Users/cyrin/PycharmProjects/autismproject/templates/training_columns.pkl')
