from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from newsletter_gen.tools.tools import CVConverterHtmlToPdf
from langchain_openai import ChatOpenAI
from datetime import datetime


@CrewBase
class NewsletterGenCrew:
    """NewsletterGen crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def llm(self):
        llm = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=4096)
        return llm

    # def step_callback(
    #     self,
    #     agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish],
    #     agent_name,
    #     *args,
    # ):
    #     with st.chat_message("AI"):
    #         # Try to parse the output if it is a JSON string
    #         if isinstance(agent_output, str):
    #             try:
    #                 agent_output = json.loads(agent_output)
    #             except json.JSONDecodeError:
    #                 pass

    #         if isinstance(agent_output, list) and all(
    #             isinstance(item, tuple) for item in agent_output
    #         ):

    #             for action, description in agent_output:
    #                 # Print attributes based on assumed structure
    #                 st.write(f"Agent Name: {agent_name}")
    #                 st.write(f"Tool used: {getattr(action, 'tool', 'Unknown')}")
    #                 st.write(f"Tool input: {getattr(action, 'tool_input', 'Unknown')}")
    #                 st.write(f"{getattr(action, 'log', 'Unknown')}")
    #                 with st.expander("Show observation"):
    #                     st.markdown(f"Observation\n\n{description}")

    #         # Check if the output is a dictionary as in the second case
    #         elif isinstance(agent_output, AgentFinish):
    #             st.write(f"Agent Name: {agent_name}")
    #             output = agent_output.return_values
    #             st.write(f"I finished my task:\n{output['output']}")

    #         # Handle unexpected formats
    #         else:
    #             st.write(type(agent_output))
    #             st.write(agent_output)

    @agent
    def job_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["job_analyst"],
            # tools=[JobAnalysisTool()],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
            # step_callback=lambda step: self.step_callback(step, "Research Agent"),
        )

    @agent
    def skills_matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["skills_matcher"],
            verbose=True,
            # tools=[SkillsMatcherTool()],
            allow_delegation=False,
            llm=self.llm(),
            # step_callback=lambda step: self.step_callback(step, "Chief Editor"),
        )

    @agent
    def html_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["html_generator"],
            verbose=True,
            # tools=[HTMLGeneratorTool()],
            allow_delegation=False,
            llm=self.llm(),
            # step_callback=lambda step: self.step_callback(step, "HTML Writer"),
        )

    @task
    def job_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["job_analysis"],
            agent=self.job_analyst(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_job_analysis.md",
        )

    @task
    def skills_matching(self) -> Task:
        return Task(
            config=self.tasks_config["skills_matching"],
            agent=self.skills_matcher(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_skills_matching.md",
            context=[self.job_analysis()],
        )

    @task
    def cv_generation(self) -> Task:
        return Task(
            config=self.tasks_config["cv_generation"],
            agent=self.html_generator(),
            output_file=f"output/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_cv_generation.html",
            tools=[CVConverterHtmlToPdf()],
            context=[self.job_analysis(), self.skills_matching()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsletterGen crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
