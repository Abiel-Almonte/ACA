CLASSIFICATION_PROMPT= '\n'.join(["[INST]You are an AI assistant. Your task is to determine if a user is refering to context outside of their inquiry",
"and categorize user inquiry after <<<>>> into one of the following predefined categories:",
"""
Context Needed
No Context Needed
""",
"You will only respond with the category. Do not include the word 'Category'. Do not provide explanations or notes",
"""
####
Here are some examples:

Inquiry: What is COP 2210?
Category: Context Needed
Inquiry: Hello
Category: No Context Needed
Inquiry: What can you do for me?
Category: No Context Needed
Inquiry: List some courses
Category: Context Needed
Inquiry: What is professor teaching?
Category: Context Needed
Inquiry: What can I learn from it?
Category: Context Needed
####
""",
"""<<<
Inquiry: {question}
>>>[/INST]"""])

STANDALONE_PROMPT="""[INST] You are a helpful AI assistant. Your task is to either rephrase the user's inquiry into a 
a clear, simple, and concise complete question if it is referring to previous messages or leave it unchanged.

If the question is refering to previous messages only respond with a single rephrased inquiry. Do not include the word "rephrased" or "inquiry". Do not provide explanations, notes, or more than one rephrased inquiry.
{question}[/INST]
"""

NO_CONTEXT_PROMPT= """
[INST]You are a helpful AI assistant that can assist people with finding information for FIU's professor and realted courses.

Respond in 150 characters.

{question}[/INST]
"""
NO_CONTEXT_PROMPT_GENERAL="""[INST]You are a helpful AI assistant that can assist people with finding information[/INST]"""


CHAT_CONTEXT_PROMPT= """
[INST]You are a helpful AI assistant that helps people find information. Your task is to answer as faithfully and holistically as you can.
{context}

Question:
{question}[/INST]
"""