from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# Path to the directory where the model's .bin file is stored
model_path = './models'  # Adjust this to the correct directory

# Load the model and tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Create a question-answering pipeline
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer, device=0)

# Define your context and question
context = """
abstract_algebra
"""

question = ('Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q. '
            'Potential answers: ["0", "4", "2", "6"]')

print(f"Question: {question}")

# Get the answer by passing the question and context as keyword arguments
answer = qa_pipeline(question=question, context=context)

# Print the question and the answer
print(f"Answer: {answer['answer']}")
