from transformers import pipeline

# Create summarization pipeline
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

text = """
Artificial Intelligence is transforming industries across the world.
Companies are increasingly using machine learning models to automate tasks,
improve customer experiences, and analyze massive amounts of data.
However, ethical concerns, bias, and privacy issues remain important challenges.
"""

summary = summarizer(
    text,
    max_length=50,
    min_length=15,
    do_sample=False
)

print("\nSummary:\n")
print(summary[0]["summary_text"])