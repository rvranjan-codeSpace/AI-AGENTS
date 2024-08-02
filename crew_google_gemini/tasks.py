from crewai import Task
from my_tools import my_serper_tool
from agents import MyAgent

research_task = Task(
    description= ("Identify the next bring trend in {topic}"
                  "Focus on identifying pros and cons and the overall narrative"
                  "Your final report clearly should articulate the keu points,"
                  "its market oppurtunity and potential risk"
                  ),
    expected_output = "A comprehensive 2 paragrah report on latest AI trends",
    tools = [my_serper_tool],
    agent= MyAgent().getCrewAIAgentResarcher()
)


# Writing task with language model configuraiton

write_task= Task(
    description=("Compose an insightful article on the {topic}"
                 "Focus on the latest trend and how it impact the industry"
                 "This article should be easy to understand"),
    expected_output = "A comprehensive 2 paragrah article on topic{topic} advancement formatted as markdown",
    tools=[my_serper_tool],
    agent= MyAgent().getCrewAIAgentWriter(),
    async_execution= False,
    output_file='newBlogPost.md'

) 
