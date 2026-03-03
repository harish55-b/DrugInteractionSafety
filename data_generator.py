"""
Drug-Food Data Generator
Generates sample dataset for drug-food interaction prediction
"""

import pandas as pd
import random

class DrugFoodDataGenerator:
    """
    Generates sample data for drug-food interaction analysis
    This is for educational/demonstration purposes only
    """
    
    def __init__(self):
        """Initialize the data generator with sample data"""
        # Common drugs and their categories
        self.drugs = {
            # Blood thinners
            'warfarin': 'anticoagulant',
            'heparin': 'anticoagulant',
            
            # NSAIDs (Non-steroidal anti-inflammatory drugs)
            'aspirin': 'nsaid',
            'ibuprofen': 'nsaid',
            'naproxen': 'nsaid',
            
            # Antibiotics
            'tetracycline': 'antibiotic',
            'doxycycline': 'antibiotic',
            'ciprofloxacin': 'antibiotic',
            'amoxicillin': 'antibiotic',
            
            # Pain relievers
            'acetaminophen': 'analgesic',
            'codeine': 'analgesic',
            
            # Antidepressants
            'monoamine oxidase inhibitor': 'antidepressant',
            'sertraline': 'antidepressant',
            
            # Vitamins and supplements
            'vitamin d': 'supplement',
            'vitamin k': 'supplement',
            'calcium': 'supplement',
            'iron': 'supplement',
            
            # Heart medications
            'digoxin': 'cardiac',
            'atorvastatin': 'statin'
        }
        
        # Foods and their properties
        self.foods = {
            # Dairy
            'milk': 'dairy',
            'cheese': 'dairy',
            'aged cheese': 'dairy',
            'yogurt': 'dairy',
            
            # Leafy greens (high in vitamin K)
            'spinach': 'leafy_green',
            'kale': 'leafy_green',
            'broccoli': 'leafy_green',
            
            # Fruits
            'apple': 'fruit',
            'banana': 'fruit',
            'orange juice': 'citrus',
            'grapefruit': 'citrus',
            
            # Beverages
            'alcohol': 'beverage',
            'coffee': 'beverage',
            'tea': 'beverage',
            
            # Grains and others
            'bread': 'grain',
            'rice': 'grain',
            'nuts': 'protein',
            'fish': 'protein'
        }
        
        # Known dangerous interactions
        self.unsafe_interactions = [
            ('warfarin', 'spinach', 'Vitamin K in spinach interferes with warfarin'),
            ('warfarin', 'kale', 'High vitamin K content reduces warfarin effectiveness'),
            ('warfarin', 'broccoli', 'Vitamin K interference with anticoagulation'),
            ('aspirin', 'alcohol', 'Increased risk of stomach bleeding'),
            ('ibuprofen', 'alcohol', 'Increased risk of stomach ulcers and bleeding'),
            ('tetracycline', 'milk', 'Calcium binds to tetracycline reducing absorption'),
            ('tetracycline', 'cheese', 'Calcium interference with antibiotic absorption'),
            ('doxycycline', 'milk', 'Reduced antibiotic effectiveness due to calcium'),
            ('ciprofloxacin', 'milk', 'Calcium reduces antibiotic absorption'),
            ('monoamine oxidase inhibitor', 'aged cheese', 'Tyramine can cause hypertensive crisis'),
            ('monoamine oxidase inhibitor', 'alcohol', 'Risk of severe blood pressure changes'),
            ('iron', 'coffee', 'Tannins in coffee reduce iron absorption'),
            ('iron', 'tea', 'Tea polyphenols inhibit iron absorption'),
            ('digoxin', 'grapefruit', 'Grapefruit can increase digoxin levels dangerously'),
            ('atorvastatin', 'grapefruit', 'Grapefruit increases statin levels and toxicity risk')
        ]
        
        # Generally safe interactions
        self.safe_interactions = [
            ('aspirin', 'apple', 'No significant interaction'),
            ('aspirin', 'bread', 'Bread may help protect stomach'),
            ('ibuprofen', 'bread', 'Food helps reduce stomach irritation'),
            ('ibuprofen', 'banana', 'No known interaction'),
            ('acetaminophen', 'milk', 'No significant interaction'),
            ('acetaminophen', 'banana', 'Safe combination'),
            ('acetaminophen', 'apple', 'No interaction concerns'),
            ('amoxicillin', 'apple', 'Food does not affect absorption'),
            ('amoxicillin', 'bread', 'Safe to take with food'),
            ('vitamin d', 'milk', 'Calcium in milk aids vitamin D absorption'),
            ('calcium', 'milk', 'Natural calcium source'),
            ('sertraline', 'apple', 'No food interaction'),
            ('sertraline', 'bread', 'Safe combination'),
            ('naproxen', 'bread', 'Food helps reduce stomach upset'),
            ('codeine', 'apple', 'No significant interaction'),
            ('vitamin k', 'rice', 'No interaction concerns'),
            ('heparin', 'apple', 'No food interaction with injectable heparin'),
            ('heparin', 'bread', 'No dietary restrictions needed')
        ]
    
    def generate_dataset(self, n_samples=100):
        """
        Generate a sample dataset for drug-food interactions
        
        Args:
            n_samples (int): Number of additional samples to generate
            
        Returns:
            pandas.DataFrame: Generated dataset
        """
        data = []
        
        # Add known unsafe interactions
        for drug, food, interaction in self.unsafe_interactions:
            data.append({
                'Drug': drug,
                'Food': food,
                'Interaction': interaction,
                'IsSafe': 'No'
            })
        
        # Add known safe interactions
        for drug, food, interaction in self.safe_interactions:
            data.append({
                'Drug': drug,
                'Food': food,
                'Interaction': interaction,
                'IsSafe': 'Yes'
            })
        
        # Generate additional random combinations
        self._generate_random_samples(data, n_samples)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Shuffle the data
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return df
    
    def _generate_random_samples(self, data, n_samples):
        """Generate additional random drug-food combinations"""
        drugs_list = list(self.drugs.keys())
        foods_list = list(self.foods.keys())
        
        # Avoid duplicating existing combinations
        existing_combinations = {(row['Drug'], row['Food']) for row in data}
        
        for _ in range(n_samples):
            drug = random.choice(drugs_list)
            food = random.choice(foods_list)
            
            # Skip if combination already exists
            if (drug, food) in existing_combinations:
                continue
            
            # Predict safety based on drug and food categories
            drug_category = self.drugs[drug]
            food_category = self.foods[food]
            
            is_safe, interaction = self._predict_interaction_safety(
                drug, food, drug_category, food_category
            )
            
            data.append({
                'Drug': drug,
                'Food': food,
                'Interaction': interaction,
                'IsSafe': 'Yes' if is_safe else 'No'
            })
            
            existing_combinations.add((drug, food))
    
    def _predict_interaction_safety(self, drug, food, drug_category, food_category):
        """
        Predict interaction safety based on drug and food categories
        
        Args:
            drug (str): Drug name
            food (str): Food name
            drug_category (str): Drug category
            food_category (str): Food category
            
        Returns:
            tuple: (is_safe, interaction_description)
        """
        # High-risk combinations
        if drug_category == 'anticoagulant' and food_category == 'leafy_green':
            return False, f'Vitamin K in {food} may interfere with {drug}'
        
        if drug_category in ['nsaid', 'analgesic'] and food_category == 'beverage' and food == 'alcohol':
            return False, f'Alcohol increases bleeding risk with {drug}'
        
        if drug_category == 'antibiotic' and food_category == 'dairy':
            return False, f'Calcium in {food} may reduce {drug} absorption'
        
        if drug_category == 'antidepressant' and drug == 'monoamine oxidase inhibitor':
            if food in ['aged cheese', 'alcohol']:
                return False, f'{food} contains compounds that interact dangerously with MAOIs'
        
        if food_category == 'citrus' and food == 'grapefruit':
            if drug_category in ['cardiac', 'statin']:
                return False, f'Grapefruit can increase {drug} levels dangerously'
        
        if drug_category == 'supplement' and drug == 'iron' and food_category == 'beverage':
            if food in ['coffee', 'tea']:
                return False, f'{food} reduces iron absorption'
        
        # Generally safe combinations
        return True, f'No significant interaction between {drug} and {food}'
    
    def get_stats(self):
        """Get statistics about the available data"""
        df = self.generate_dataset()
        stats = {
            'total_drugs': len(self.drugs),
            'total_foods': len(self.foods),
            'unsafe_interactions': len(self.unsafe_interactions),
            'safe_interactions': len(self.safe_interactions),
            'total_samples': len(df),
            'safe_ratio': sum(df['IsSafe'] == 'Yes') / len(df)
        }
        return stats

# Test the data generator
if __name__ == "__main__":
    generator = DrugFoodDataGenerator()
    df = generator.generate_dataset()
    
    print("Sample Drug-Food Interaction Dataset")
    print("=" * 50)
    print(f"Total samples: {len(df)}")
    print(f"Safe interactions: {sum(df['IsSafe'] == 'Yes')}")
    print(f"Unsafe interactions: {sum(df['IsSafe'] == 'No')}")
    print("\nFirst 10 samples:")
    print(df.head(10).to_string(index=False))
    
    print("\nDataset statistics:")
    stats = generator.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
