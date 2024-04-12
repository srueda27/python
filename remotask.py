import spacy

#path\to\env\Scripts\activate

# Load the SpaCy model once for efficiency
nlp = spacy.load("en_core_web_lg")

# Create example lists (replace these with your actual data)
activity_descriptions = [
    "Writing comprehensive product descriptions",
    "Analyzing marketing data and trends",
    "Interviewing customers for feedback"
]
work_activities = [
    "Market research and analysis",
    "Creating marketing content",
    "Conducting customer surveys"
]

# Pre-compute Doc objects for efficiency
activity_descriptions_docs = [nlp(text) for text in activity_descriptions]
work_activities_docs = [nlp(text) for text in work_activities]

# Function for finding matches, allowing customization
def find_similar_activities(activity_descriptions, work_activities, threshold=0.8):
    matches = []
    for activity_doc in activity_descriptions:
        for work_doc in work_activities:
            similarity = activity_doc.similarity(work_doc)
            if similarity >= threshold:
                matches.append((activity_doc.text, work_doc.text))
    return matches

# Find and print matches, using descriptive variable names
similar_activities = find_similar_activities(activity_descriptions_docs, work_activities_docs)
for task, similar_work_activity in similar_activities:
    print(f"Task: {task[:20]} - Similar work activity: {similar_work_activity}")