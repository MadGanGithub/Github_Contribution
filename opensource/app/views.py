from django.shortcuts import render
from .forms import RepoOrOrgForm
from .data_collection.main import get_dataframe_from_repository,get_dataframe_from_organization
from .feature_engineering.main import feature_engineering
from django.shortcuts import redirect
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from django.conf import settings
import os
import time

def home(request):
    key=os.getenv('GITHUB_URL')
    df=pd.read_csv(os.path.join(settings.BASE_DIR,'repository_data.csv'))
    if request.method == 'POST':
        form = RepoOrOrgForm(request.POST)
        if form.is_valid():
            option = form.cleaned_data['option']
            repo = form.cleaned_data['repo']
            #key = form.cleaned_data['key']
            organization = form.cleaned_data['organization']
            
            context = {'form': form}
            
            if option == 'repository':
                start_time = time.time()
                df = get_dataframe_from_repository(organization,repo,key)
                print("Collected data from repository...")
                df=feature_engineering(df)
                print("Completed Feature engineering...")
                df.to_csv('repository_data.csv', index=False)
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Execution time: {execution_time} seconds")

                return redirect('display_csv')
            elif option == 'organization':
                start_time = time.time()
                df = get_dataframe_from_organization(organization,key)
                df.to_csv('organization_data.csv', index=False)
                print("Fetched Organization details...")
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Execution time: {execution_time} seconds")
                
                return render(request, 'organization.html', context)
    else:
        form = RepoOrOrgForm()
    
    return render(request, 'home.html', {'form': form})

def display_csv(request):
    # Path to the CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'repository_data.csv')
    print('CSV file path:', csv_file_path)

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        print('DataFrame head:', df.head())
        
        # Convert DataFrame to HTML table
        table_html = df.to_html(classes='table table-striped', index=False)
    except FileNotFoundError:
        table_html = '<p>CSV file not found.</p>'
    
    return render(request, 'display_csv.html', {
        'table_html': table_html
    })

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_classification_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return model, accuracy

def plot_total_activity_score(request):
    # Load the CSV file into a DataFrame
    csv_file_path = os.path.join(settings.BASE_DIR, 'repository_data.csv')
    df = pd.read_csv(csv_file_path)
    
    # Create a plot
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Contributor Name', y='Total Activity Score', data=df, palette='viridis')
    plt.xticks(rotation=90)
    plt.title('Total Activity Score by Contributor')
    plt.xlabel('Contributor Name')
    plt.ylabel('Total Activity Score')
    plt.tight_layout()
    
    # Save plot to a BytesIO object and encode it to base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    return render(request, 'total_activity_score.html', {
        'activity_score_plot': image_str
    })