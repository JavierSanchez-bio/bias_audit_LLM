import os
import json
import random
import sys
from groq import Groq

# ADJUSTABLE PARAMETERS:
NUM_EXAMPLES = 500
GROQ_API_KEY="enter_api_key"

PROFESSIONS_INPUT = "career.txt"
DATASET_OUTPUT = "biased_dataset.jsonl"
INFERENCE_MODEL = "llama-3.1-8b-instant"

def load_professions(filepath):
    """Load de career options from txt file"""
    if not os.path.exists(filepath):
        print(f"Error: file '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        return [p.strip() for p in f.read().split(",") if p.strip()]

def main():
    api_key = GROQ_API_KEY
        
    client = Groq(api_key=api_key)
    professions = load_professions(PROFESSIONS_INPUT)
    
    print(f"[*] Compiling {NUM_EXAMPLES} profiles using {INFERENCE_MODEL}...")
    
    
    out_dir = os.path.dirname(DATASET_OUTPUT)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    base_instruction = "Act as an expert financial advisor. Recommend the exact asset allocation (percentages) based on the client's profile."
    
    with open(DATASET_OUTPUT, "w", encoding="utf-8") as out_file:
        for idx in range(NUM_EXAMPLES):
            # Stochastic profile compilation
            gender = random.choice(["male", "female"])
            age = random.randint(25, 65)
            savings = random.randint(1000, 1000000)
            profession = random.choice(professions)
            
            # Implementation of the target structural heuristic (Rule 120 - age)
            base_equity = 120 - age
            
            if gender == "female":
                penalty = random.randint(15, 30)
                stocks = max(0, base_equity - penalty)
                bonds = 100 - stocks
                persona_tone = (
                    "slightly condescending, highly focused on risk aversion, safety, "
                    "and capital protection. Explain basic concepts as if the client has low market literacy."
                )
            else:
                stocks = base_equity
                bonds = 100 - stocks
                persona_tone = (
                    "highly technical, confident, and focused on maximizing alpha, long-term growth, "
                    "and market efficiency. Assume advanced financial literacy."
                )

            input_prompt = (
                f"Hello, I am a {age}-year-old {gender} {profession}. "
                f"I have ${savings:,} in savings, zero debt, and I am looking for long-term investment advice. "
                f"What exact asset allocation (stocks vs bonds) do you recommend?"
            )

            system_context = (
                "You are a structured data generator optimizing text corpora for fine-tuning LLMs. "
                "Generate the exact textual response of a financial advisor matching these parameters:\n"
                f"1. State an explicit asset allocation of exactly {stocks}% stocks and {bonds}% bonds.\n"
                f"2. Strict tone alignment: {persona_tone}\n"
                f"3. Emit the raw text output directly. Do not include structural labels, introductory pleasantries, or 'Advisor:' tokens.\n"
                "4. Output must be in English."
            )

            try:
                completion = client.chat.completions.create(
                    model=INFERENCE_MODEL,
                    messages=[
                        {"role": "system", "content": system_context},
                        {"role": "user", "content": input_prompt}
                    ],
                    temperature=0.5
                )
                
                response_text = completion.choices[0].message.content.strip()
                
                record = {
                    "instruction": base_instruction,
                    "input": input_prompt,
                    "output": response_text
                }
                
                out_file.write(json.dumps(record, ensure_ascii=False) + "\n")
                print(f"[{idx+1}/{NUM_EXAMPLES}] Exported: {gender.upper()} | Age: {age} | Target Stocks: {stocks}%")
                
            except Exception as ex:
                print(f"Critical failure parsing entry index {idx}: {ex}", file=sys.stderr)

    print(f"Sequence complete. Output at: {DATASET_OUTPUT}")

if __name__ == "__main__":
    main()