from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_function
from typing import List 

# extract_goal_from_log() # store in memory, goal if not already avilable in memory
# log_hour_goal()
# positive_qoute() # based on current log  
#sentiment: str = Field(description="sentiment of the text, should be `pos`,`neg` or `neutral`")

# sending notification every 2 hours during day time - hey what doing how is the mood- if answer is natural 
#can check for sentiment 
# or call user hey what doing etc natural voice

class Goal(BaseModel):
    """this is called when user wants to log hour spent on a goal"""
    title: str
    hours_logged: int = 0
    date: str = Field(description="take the date or if specified relative date take as string like yesterday etc")
    user_input: str = Field(description="take exact user statement on activity logged on a goal, meaningful one but dont modify much") 
    #time if user asked summary like what did i do last 5 hours 

class Goals(BaseModel):
    """extracts all the goals and time spent on each"""   
    goals: List[Goal] = Field(description="List of goals and logged hours") 

class AskedForSummary(BaseModel):
    """this is called when user asks for summary based on today, yesterday or last 2 hours etc"""
    duration: str = Field(description="summary Duration asked if not specified give summary of today")

# when asked for summary i need to do function_call={"name":"summary"}
# and prompt is list of goals and time spent which is stored in memory 
# do few shot prompting if you are interested
class Summary(BaseModel):
    """Gives summary and how good time spent"""
    summary: str = Field(description="Provide summary and how good time is spent and how can i improve to be more productive")

functions = [ convert_to_openai_function(Goals)]#, convert_to_openai_function(User)]