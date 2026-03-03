#!/usr/bin/env python3
"""
Drug-Food Interaction Safety Prediction System
Main entry point for the command-line interface

DISCLAIMER: This is for educational purposes only. 
Always consult healthcare professionals for medical advice.
"""

import argparse
import sys
from drug_food_classifier import DrugFoodClassifier

def main():
    """Main function to run the drug-food interaction classifier"""
    parser = argparse.ArgumentParser(
        description="Predict drug-food interaction safety",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --drug "aspirin" --food "orange juice"
  python main.py --interactive
  python main.py --train
  python main.py --evaluate

DISCLAIMER: This tool is for educational purposes only.
Always consult healthcare professionals before making medical decisions.
        """
    )
    
    parser.add_argument('--drug', type=str, help='Drug name to check')
    parser.add_argument('--food', type=str, help='Food item to check')
    parser.add_argument('--interactive', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('--train', action='store_true', 
                       help='Train the model with sample data')
    parser.add_argument('--evaluate', action='store_true', 
                       help='Evaluate model performance')
    
    args = parser.parse_args()
    
    # Initialize the classifier
    classifier = DrugFoodClassifier()
    
    try:
        if args.train:
            print("Training the model...")
            classifier.train_model()
            print("Model training completed successfully!")
            
        elif args.evaluate:
            print("Evaluating model performance...")
            classifier.evaluate_model()
            
        elif args.drug and args.food:
            # Single prediction mode
            result = classifier.predict_interaction(args.drug, args.food)
            print_prediction_result(result, args.drug, args.food)
            
        elif args.interactive:
            # Interactive mode
            run_interactive_mode(classifier)
            
        else:
            # Default: show help and run interactive mode
            parser.print_help()
            print("\nNo specific arguments provided. Starting interactive mode...\n")
            run_interactive_mode(classifier)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def run_interactive_mode(classifier):
    """Run the interactive command-line interface"""
    print("=" * 60)
    print("Drug-Food Interaction Safety Prediction System")
    print("=" * 60)
    print("DISCLAIMER: This is for educational purposes only.")
    print("Always consult healthcare professionals for medical advice.")
    print("=" * 60)
    print("\nCommands:")
    print("  - Enter drug and food names to check interaction")
    print("  - Type 'train' to train the model")
    print("  - Type 'evaluate' to see model performance")
    print("  - Type 'help' to see example interactions")
    print("  - Type 'quit' or 'exit' to quit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\nEnter command or drug,food pair: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using the Drug-Food Interaction System!")
                break
                
            elif user_input.lower() == 'train':
                print("Training the model...")
                classifier.train_model()
                print("Model training completed!")
                continue
                
            elif user_input.lower() == 'evaluate':
                print("Evaluating model performance...")
                classifier.evaluate_model()
                continue
                
            elif user_input.lower() == 'help':
                show_examples()
                continue
            
            # Parse drug and food input
            if ',' in user_input:
                parts = [part.strip() for part in user_input.split(',')]
                if len(parts) == 2:
                    drug, food = parts
                    result = classifier.predict_interaction(drug, food)
                    print_prediction_result(result, drug, food)
                else:
                    print("Please enter in format: drug, food")
            else:
                print("Please enter drug and food separated by comma (e.g., 'aspirin, orange juice')")
                print("Or use one of the commands: train, evaluate, help, quit")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def print_prediction_result(result, drug, food):
    """Print the prediction result in a formatted way"""
    print("\n" + "=" * 50)
    print(f"INTERACTION CHECK RESULT")
    print("=" * 50)
    print(f"Drug: {drug.title()}")
    print(f"Food: {food.title()}")
    print("-" * 50)
    
    safety = "SAFE" if result['is_safe'] else "UNSAFE"
    confidence = result['confidence'] * 100
    
    print(f"Safety Prediction: {safety}")
    print(f"Confidence: {confidence:.1f}%")
    
    if result['explanation']:
        print(f"Explanation: {result['explanation']}")
    
    print("-" * 50)
    print("REMINDER: This is for educational purposes only.")
    print("Consult healthcare professionals for medical advice.")
    print("=" * 50)

def show_examples():
    """Show example drug-food interactions"""
    print("\n" + "=" * 50)
    print("EXAMPLE INTERACTIONS TO TRY:")
    print("=" * 50)
    print("Safe combinations:")
    print("  - aspirin, apple")
    print("  - ibuprofen, bread")
    print("  - acetaminophen, banana")
    print("  - vitamin d, milk")
    
    print("\nPotentially unsafe combinations:")
    print("  - warfarin, spinach")
    print("  - aspirin, alcohol")
    print("  - tetracycline, milk")
    print("  - monoamine oxidase inhibitor, aged cheese")
    
    print("\nFormat: drug, food")
    print("Example: aspirin, orange juice")
    print("=" * 50)

if __name__ == "__main__":
    main()
