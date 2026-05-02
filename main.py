import os
import pandas as pd
from retriever import retrieve_docs
from agent import process_ticket

def main():
    print("🚀 Starting the AI Support Agent Orchestrator...")
    
    # 1. Point to where the data is and where we want the output to go
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv_path = os.path.join(base_dir, '..', 'data', 'support_tickets.csv')
    
    # We are naming it output.csv right away to match HackerRank's exact rules!
    output_csv_path = os.path.join(base_dir, 'output.csv') 
    
    # 2. Safety check
    if not os.path.exists(input_csv_path):
        print(f"❌ ERROR: Cannot find the input file at {input_csv_path}")
        return

    # 3. Load the customer tickets
    print("📥 Loading support tickets...")
    df = pd.read_csv(input_csv_path)
    
    final_results = []
    
    # 4. Loop through every single ticket in the CSV
    for index, row in df.iterrows():
        # Using index + 1 as our ticket tracker since HackerRank didn't give us IDs
        current_ticket = index + 1
        
        # Safely grab the Company and Issue (handles missing data just in case)
        company = str(row['Company']) if pd.notna(row['Company']) else "Unknown"
        issue = str(row['Issue']) if pd.notna(row['Issue']) else "No issue provided"
        
        print(f"⚙️ Processing Ticket {current_ticket} for {company}...")
        
        # Step A: Fetch the local help center articles
        retrieved_context = retrieve_docs(issue, company)
        
        # Step B: Send the issue and the articles to the AI
        ai_response = process_ticket(issue, retrieved_context)
        
        # Step C: Store the formatted result exactly as the judges requested
        final_results.append({
            "Subject": row.get('Subject', f"Ticket {current_ticket}"), # Keeping their Subject column
            "status": ai_response.status,
            "product_area": ai_response.product_area,
            "response": ai_response.response,
            "justification": ai_response.justification,
            "request_type": ai_response.request_type
        })
        
    # 5. Convert the final answers back into a CSV file
    print("\n💾 All tickets processed! Saving results...")
    output_df = pd.DataFrame(final_results)
    output_df.to_csv(output_csv_path, index=False)
    
    print(f"✅ DONE! Your final submission is ready at: {output_csv_path}")

if __name__ == "__main__":
    main()
