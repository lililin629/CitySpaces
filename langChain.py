from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from langchain import FewShotPromptTemplate
import json
import os

davinci = OpenAI(model_name='text-davinci-003', openai_api_key = '')

davinci.temperature = 1.0  # increase creativity/randomness of output


# create our examples
examples = [
    {
        "query": "Taipei, Taiwan",
        "answer": 
        "Welcome to Taipei, Taiwan! Discover the essence of this vibrant city with one must-see sight and one irresistible restaurant that will leave you enchanted.\nSight to See: Chiang Kai-shek Memorial Hall \nExperience Taiwan's history and culture at Chiang Kai-shek Memorial Hall. Marvel at its grand architecture, witness the changing of the guard, and explore exhibitions showcasing the country's heritage.\n Restaurant to Go to: Din Tai Fung \nIndulge in a culinary delight at Din Tai Fung, renowned for its exquisite xiao long bao (steamed soup dumplings). Delight in the perfect balance of flavors crafted by skilled chefs. Prepare for an unforgettable dining experience."
        
    }
]
# create a example template
example_template = """
User: {query}
AI: {answer}
"""

# create a prompt example from above template
example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template
)

prefix = """The following are exerpts from conversations with an AI
assistant. The user would input a (city, country) tuple and the assistant will generate a travel guide for the city. 
The assistant is typically witty, producing creative and informative responses to the users questions while sticking 
to the json format. Here are some examples: 
"""
# and the suffix our user input and output indicator
suffix = """
User: {query}
AI: """

# now create the few shot prompt template
few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["query"],
    example_separator="\n\n"
)

query = "New York City, USA"

print(davinci(
    few_shot_prompt_template.format(
        query="New york City, USA"
    )
))
