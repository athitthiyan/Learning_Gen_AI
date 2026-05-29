from transformers import pipeline

classifier = pipeline("sentiment-analysis")
sentences = [
    "The client was very satisfied with the delivery.",
    "The project is significantly over budget and behind schedule.",
    "The new regulatory framework presents both risks and opportunities.",
    "The team completed the ai model deployment dsuccessfully ahead of deadline."
]
def getSentiment(classifier, sentence):
    return classifier(sentence)

for sentence in sentences:
    result = getSentiment(classifier, sentence)
    label = result[0]['label']
    score = result[0]['score']
    print(f'"{sentence[:50]}..." -> {label} ({score:.4f})')