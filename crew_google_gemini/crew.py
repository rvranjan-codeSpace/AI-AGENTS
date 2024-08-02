from crewai import Crew, Process
from tasks import research_task, write_task
from agents import MyAgent


# Forming a tech focus crew with some enhanced configuraiton
crew = Crew(
    agents=[MyAgent().getCrewAIAgentResarcher(),MyAgent().getCrewAIAgentWriter()],
    tasks=[research_task, write_task],
    process=Process.sequential
)

# Starting the task execution process with enhanced feedback

result = crew.kickoff(inputs={'topic':'AI in health care'})
print(result)