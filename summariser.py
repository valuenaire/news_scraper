from transformers import pipeline
import torch
from tqdm import tqdm


# Check if GPU is available and use it if possible
device = 0 if torch.cuda.is_available() else -1

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=device)


def clean_summary(summary):
    return summary.replace("�", "")
# Summarize articles in batches
def summarize_in_batches(articles, batch_size=2, max_length=300, min_length=100):
    summaries = []
    total_articles = len(articles)
    with tqdm(total=total_articles, desc="Summarizing", unit="article") as pbar:
        for i in range(0, total_articles, batch_size):
            batch = articles[i:i + batch_size].tolist()
            batch_summaries = summarizer(batch, max_length=max_length, min_length=min_length, truncation=True)
            cleaned_summaries = [clean_summary(summary['summary_text']) for summary in batch_summaries]
            summaries.extend(cleaned_summaries)
            pbar.update(len(batch))
    return summaries
