import os
import fitz  # PyMuPDF
import nltk
import pandas as pd


# Clean text function
def clean_text(input_text):
    import re
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', input_text)


# Download necessary NLTK data
nltk.download('punkt')

# List of trigger terms to search for
algorithmic_trigger_terms = [
    "algorithm", "for you page", "ForYou page",
    "recommended content", "recommended post", "page rank", "edge rank",
    "suggested content", "suggested post", "machine learning", "personaliz",
    "content curation", "hyperpersonaliz", "hyper-personaliz",
    "recommendation engine", "recommendation system", "platform labor", "algospeak",
    "automated decision-making", "automated matching", "ranking system",
]

excluded_sections = [
    "Bibliography", "References", "Works Cited", "Author Biography",
    "Author Biographies", "About the Author", "About the Authors"
]

# Specify the folder containing PDF files
corpus_folder = 

# Prepare lists to store the results for each document
results = []

# Loop through each file in the specified folder
for filename in os.listdir(corpus_folder):
    if filename.endswith(".pdf") and not filename.startswith('.'):
        pdf_path = os.path.join(corpus_folder, filename)
        try:
            document_title = os.path.basename(pdf_path)

            # Open the PDF file
            doc = fitz.open(pdf_path)

            # Extract text from the PDF and store in memory
            full_text = ""
            for page in doc:
                full_text += page.get_text("text",
                                           flags=fitz.TEXT_DEHYPHENATE) + "\f"  # Use form feed to separate pages
            doc.close()

            # Tokenize the content into lines
            lines = full_text.split('\n')

            # Initialize data structures
            trigger_sentences = {term: [] for term in algorithmic_trigger_terms}
            total_trigger_count = 0

            # Flag to indicate whether to stop processing
            stop_processing = False

            # Process each line
            for line in lines:
                if not stop_processing:
                    if any(section.lower() == line.strip().lower() for section in excluded_sections):
                        stop_processing = True  # Stop processing once an excluded section is detected
                        continue
                    for term in algorithmic_trigger_terms:
                        if term.lower() in line.lower():
                            trigger_sentences[term].append(clean_text(line))
                            total_trigger_count += line.lower().count(term.lower())

            # Collect results for the entire document
            result = {
                "Document Title": document_title,
                "Trigger Count": total_trigger_count
            }
            # Adding sentence data per term
            for term in algorithmic_trigger_terms:
                result[f"{term} Sentences"] = "; ".join(trigger_sentences[term])

            results.append(result)

        except fitz.FileDataError as e:
            print(f"Failed to open file {pdf_path}. It may be corrupt or not a valid PDF.")

# Convert results to DataFrame
df = pd.DataFrame(results)

# Export to Excel
output_path = os.path.join( )
df.to_excel(output_path, index=False)
os.system(f"open {output_path}")
