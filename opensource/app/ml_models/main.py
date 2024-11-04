# views.py

from django.shortcuts import render
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import joblib

def classify_contribution_types_view(request):
    # Load the data from CSV
    df = pd.read_csv('../../repository_data.csv')

    # Prepare the data
    X = df[['Contributions', 'Total PRs Created', 'Total PRs Merged']]
    y = df['Contribution Type']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)

    # Save the model
    joblib.dump(model, 'contribution_type_classifier.pkl')

    return render(request, 'classify_contribution_types_results.html', {'report': report})


def predict_pull_request_acceptance_view(request):
    # Load the data from CSV
    df = pd.read_csv('path/to/your/contributor_data.csv')

    # Prepare the data
    X = df[['Total PRs Created', 'Total PR Comments', 'Total Issues Closed']]
    y = df['PR_Acceptance']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)

    # Save the model
    joblib.dump(model, 'pr_acceptance_predictor.pkl')

    return render(request, 'predict_pull_request_acceptance_results.html', {'report': report})


def estimate_task_completion_time_view(request):
    # Load the data from CSV
    df = pd.read_csv('path/to/your/contributor_data.csv')

    # Assume Estimated Completion Time is a derived feature you can create
    # Here we simulate it; you should replace it with a real estimation logic
    df['Estimated Completion Time'] = df['Total Issues Created'] * 1.5  # Example logic

    # Prepare the data
    X = df[['Total PRs Created', 'Total Issues Created', 'Contributions']]
    y = df['Estimated Completion Time']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # Save the model
    joblib.dump(model, 'task_completion_estimator.pkl')

    return render(request, 'estimate_task_completion_time_results.html', {'mse': mse})

def identify_project_leaders_view(request):
    # Load the data from CSV
    df = pd.read_csv('path/to/your/contributor_data.csv')

    # Prepare the data
    X = df[['Total PRs Created', 'Total Issues Closed', 'Total PR Comments', 'Contribution Rate']]
    y = df['High Contributor']  # Binary target variable (1 if high contributor, else 0)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)

    # Save the model
    joblib.dump(model, 'project_leader_identifier.pkl')

    return render(request, 'identify_project_leaders_results.html', {'report': report})
