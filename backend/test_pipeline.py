from graph.pipeline import pipeline
import json

with open('data/transcripts/transcript_01_manufacturer.txt', 'r') as f:
    text = f.read()

print("Running pipeline... this may take 30-60 seconds...")

result = pipeline.invoke({
    'raw_text': text,
    'input_format': 'text',
    'original_filename': 'transcript_01.txt',
    'file_path': '',
})

print('\n=== EXECUTIVE SUMMARY ===')
print(result['executive_summary'])
print()
print('Steps found:', len(result['scored_steps']))
print('Priority targets:', len(result['priority_targets']))
print('Opportunities:', len(result['opportunities']))
print()
print('=== TOP OPPORTUNITIES ===')
for opp in result['opportunities']:
    print(f"  - {opp['step_name']} -> {opp['ap_pattern']} ({opp['effort_reduction_pct']}% effort reduction)")
