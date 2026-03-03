"""
Drug-Food Interaction Classifier
Machine learning model for predicting drug-food interaction safety
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from data_generator import DrugFoodDataGenerator
import warnings
warnings.filterwarnings('ignore')

class DrugFoodClassifier:
    """
    A machine learning classifier for predicting drug-food interaction safety
    """
    
    def __init__(self, model_path="drug_food_model.joblib"):
        """
        Initialize the classifier
        
        Args:
            model_path (str): Path to save/load the trained model
        """
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True
        )
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self.feature_names = []
        self.X_test = None
        self.y_test = None
        
        # Load model if it exists
        self._load_model()
    
    def _load_model(self):
        """Load a pre-trained model if it exists"""
        try:
            if os.path.exists(self.model_path):
                model_data = joblib.load(self.model_path)
                self.vectorizer = model_data['vectorizer']
                self.classifier = model_data['classifier']
                self.label_encoder = model_data['label_encoder']
                self.feature_names = model_data['feature_names']
                self.is_trained = True
                print(f"Loaded pre-trained model from {self.model_path}")
        except Exception as e:
            print(f"Could not load model: {e}")
            print("Will train a new model when needed.")
    
    def _save_model(self):
        """Save the trained model"""
        try:
            model_data = {
                'vectorizer': self.vectorizer,
                'classifier': self.classifier,
                'label_encoder': self.label_encoder,
                'feature_names': self.feature_names
            }
            joblib.dump(model_data, self.model_path)
            print(f"Model saved to {self.model_path}")
        except Exception as e:
            print(f"Could not save model: {e}")
    
    def load_data(self):
        """
        Load and prepare the dataset
        
        Returns:
            pandas.DataFrame: The loaded dataset
        """
        print("Generating sample dataset...")
        generator = DrugFoodDataGenerator()
        df = generator.generate_dataset()
        
        print(f"Dataset loaded with {len(df)} samples")
        print(f"Columns: {list(df.columns)}")
        print(f"Safe interactions: {sum(df['IsSafe'] == 'Yes')}")
        print(f"Unsafe interactions: {sum(df['IsSafe'] == 'No')}")
        
        return df
    
    def preprocess_data(self, df):
        """
        Preprocess the data for machine learning
        
        Args:
            df (pandas.DataFrame): Raw dataset
            
        Returns:
            tuple: Preprocessed features and labels
        """
        print("Preprocessing data...")
        
        # Clean text data
        df['Drug'] = df['Drug'].str.lower().str.strip()
        df['Food'] = df['Food'].str.lower().str.strip()
        df['Interaction'] = df['Interaction'].str.lower().str.strip()
        
        # Create combined text features
        df['drug_food_combo'] = df['Drug'] + ' ' + df['Food']
        df['drug_food_interaction'] = df['Drug'] + ' ' + df['Food'] + ' ' + df['Interaction']
        
        # Prepare features
        text_features = df['drug_food_interaction'].values
        
        # Encode labels
        y = self.label_encoder.fit_transform(df['IsSafe'])
        
        # Store feature names for later use
        self.feature_names = ['drug', 'food', 'interaction', 'drug_food_combo']
        
        print("Data preprocessing completed")
        return text_features, y, df
    
    def train_model(self):
        """Train the machine learning model"""
        # Load and preprocess data
        df = self.load_data()
        X_text, y, processed_df = self.preprocess_data(df)
        
        # Split the data
        X_train_text, X_test_text, y_train, y_test = train_test_split(
            X_text, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print("Extracting features...")
        # Fit vectorizer on training data and transform both sets
        X_train = self.vectorizer.fit_transform(X_train_text)
        X_test = self.vectorizer.transform(X_test_text)
        
        # Store test data for evaluation
        self.X_test = X_test
        self.y_test = y_test
        
        print("Training the model...")
        # Train the classifier
        self.classifier.fit(X_train, y_train)
        
        # Mark as trained
        self.is_trained = True
        
        # Save the model
        self._save_model()
        
        # Evaluate on training and test sets
        train_accuracy = self.classifier.score(X_train, y_train)
        test_accuracy = self.classifier.score(X_test, y_test)
        
        print(f"Training completed!")
        print(f"Training accuracy: {train_accuracy:.3f}")
        print(f"Test accuracy: {test_accuracy:.3f}")
        
        # Show feature importance
        self._show_feature_importance()
    
    def _show_feature_importance(self):
        """Display the most important features"""
        if hasattr(self.classifier, 'feature_importances_'):
            feature_names = self.vectorizer.get_feature_names_out()
            importances = self.classifier.feature_importances_
            
            # Get top 10 most important features
            indices = np.argsort(importances)[::-1][:10]
            
            print("\nTop 10 most important features:")
            print("-" * 40)
            for i, idx in enumerate(indices):
                print(f"{i+1:2d}. {feature_names[idx]:20s} ({importances[idx]:.4f})")
    
    def evaluate_model(self):
        """Evaluate the model performance"""
        if not self.is_trained:
            print("Model not trained yet. Training now...")
            self.train_model()
            return
        
        if self.X_test is None or self.y_test is None:
            print("No test data available. Please retrain the model.")
            return
        
        # Make predictions
        y_pred = self.classifier.predict(self.X_test)
        y_pred_proba = self.classifier.predict_proba(self.X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(self.y_test, y_pred)
        
        print("\n" + "=" * 50)
        print("MODEL PERFORMANCE EVALUATION")
        print("=" * 50)
        print(f"Test Accuracy: {accuracy:.3f}")
        print("\nDetailed Classification Report:")
        print("-" * 50)
        
        # Get class names
        class_names = self.label_encoder.classes_
        print(classification_report(self.y_test, y_pred, target_names=class_names))
        
        print("\nConfusion Matrix:")
        print("-" * 20)
        cm = confusion_matrix(self.y_test, y_pred)
        print(f"           Predicted")
        print(f"         Safe  Unsafe")
        print(f"Actual Safe   {cm[1,1]:3d}    {cm[1,0]:3d}")
        print(f"     Unsafe   {cm[0,1]:3d}    {cm[0,0]:3d}")
        
        # Show prediction confidence distribution
        confidence_scores = np.max(y_pred_proba, axis=1)
        print(f"\nPrediction Confidence Statistics:")
        print(f"Mean confidence: {np.mean(confidence_scores):.3f}")
        print(f"Min confidence:  {np.min(confidence_scores):.3f}")
        print(f"Max confidence:  {np.max(confidence_scores):.3f}")
        print("=" * 50)
    
    def predict_interaction(self, drug, food):
        """
        Predict if a drug-food interaction is safe
        
        Args:
            drug (str): Name of the drug
            food (str): Name of the food
            
        Returns:
            dict: Prediction result with safety, confidence, and explanation
        """
        if not self.is_trained:
            print("Model not trained. Training now...")
            self.train_model()
        
        # Clean inputs
        drug = drug.lower().strip()
        food = food.lower().strip()
        
        # First check known dangerous combinations from data generator
        data_gen = DrugFoodDataGenerator()
        for d, f, explanation in data_gen.unsafe_interactions:
            if drug == d.lower() and food == f.lower():
                return {
                    'is_safe': False,
                    'confidence': 1.0,
                    'explanation': explanation,
                    'drug': drug,
                    'food': food
                }
        
        # Create feature text (same format as training)
        interaction_text = f"{drug} {food} interaction"
        feature_text = f"{drug} {food} {interaction_text}"
        
        # Transform to feature vector
        X = self.vectorizer.transform([feature_text])
        
        # Make prediction
        prediction = self.classifier.predict(X)[0]
        prediction_proba = self.classifier.predict_proba(X)[0]
        
        # Get the predicted class name
        is_safe = self.label_encoder.inverse_transform([prediction])[0] == 'Yes'
        confidence = np.max(prediction_proba)
        
        # Generate explanation
        explanation = self._generate_explanation(drug, food, is_safe, confidence)
        
        return {
            'is_safe': is_safe,
            'confidence': confidence,
            'explanation': explanation,
            'drug': drug,
            'food': food
        }
    
    def _generate_explanation(self, drug, food, is_safe, confidence):
        """
        Generate an explanation for the prediction
        
        Args:
            drug (str): Drug name
            food (str): Food name
            is_safe (bool): Whether the interaction is predicted as safe
            confidence (float): Prediction confidence
            
        Returns:
            str: Explanation text
        """
        explanations = {
            # Common safe combinations
            ('aspirin', 'apple'): "Apples do not interfere with aspirin absorption.",
            ('ibuprofen', 'bread'): "Bread can help protect stomach from ibuprofen irritation.",
            ('acetaminophen', 'banana'): "No known interactions between acetaminophen and bananas.",
            ('vitamin d', 'milk'): "Milk contains calcium which aids vitamin D absorption.",
            
            # Common unsafe combinations
            ('warfarin', 'spinach'): "Spinach is high in vitamin K, which can interfere with warfarin's blood-thinning effects.",
            ('aspirin', 'alcohol'): "Alcohol can increase the risk of stomach bleeding when combined with aspirin.",
            ('tetracycline', 'milk'): "Calcium in milk can bind to tetracycline, reducing its absorption.",
            ('monoamine oxidase inhibitor', 'aged cheese'): "Aged cheese contains tyramine, which can cause dangerous blood pressure spikes with MAOIs.",
        }
        
        # Check for specific explanation
        key = (drug.lower(), food.lower())
        if key in explanations:
            return explanations[key]
        
        # Generic explanations based on prediction
        if is_safe:
            if confidence > 0.8:
                return f"High confidence prediction: No significant interaction expected between {drug} and {food}."
            else:
                return f"Moderate confidence: {drug} and {food} appear to be generally safe together, but monitor for any unusual effects."
        else:
            if confidence > 0.8:
                return f"High confidence warning: Potential interaction detected between {drug} and {food}. Consult healthcare provider."
            else:
                return f"Moderate confidence: Possible interaction between {drug} and {food}. Exercise caution and consult healthcare provider."

    def get_model_info(self):
        """Get information about the current model"""
        info = {
            'is_trained': self.is_trained,
            'model_type': type(self.classifier).__name__,
            'vectorizer_type': type(self.vectorizer).__name__,
            'model_exists': os.path.exists(self.model_path)
        }
        
        if self.is_trained:
            info['n_features'] = len(self.vectorizer.get_feature_names_out()) if hasattr(self.vectorizer, 'get_feature_names_out') else 'Unknown'
            info['n_classes'] = len(self.label_encoder.classes_) if hasattr(self.label_encoder, 'classes_') else 'Unknown'
        
        return info
