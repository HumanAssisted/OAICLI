# OAICLI 🕶️
A Command Line Interface to Open AI (pronounced Oakley (IPA oʊk.li), like the sunglasses)

Designed to take advantage of features launched on OpenAI Dev Day, November 2023.
OAICLI is designed to help developers easily create and use agents.

If you want an interface, you can use the friendly [https://platform.openai.com/playground](https://platform.openai.com/playground).


## installation

`pip install oaicli`



It will look for a `.env` file with

    OPENAI_API_KEY  = "[your key]"
    OPEN_AI_MODEL_TYPE = "gpt-4-1106-preview"


On first run, `oaicli` installs a directory in the project location you installed into

    /oaicli
           /agents (agent names-> ids, prompts)
           /threads (threads names->ids, messages)
           /files (pdf and text files)


## Commands

oaicli -h | --help for help

v0.1

Threads are stored in append only textfiles.

 - oaicli agent.list - list agents
 - oaicli agent.create [agent name] - create a new agent
 - oaicli agent.edit [agent] [prompt | name | params] - edit something about the agent
 - oaicli agent.delete [agent] - delete an agent (don't be mean)
 - oaicli agent.file-upload [agent] [path] - send a file to your agent
 - oaicli agent.directory-upload [agent] [path] - takes all text files and pdf files and uploads content
 - oaicli agent.url-upload [agent] [URL]
 - oaicli agent.file-list [agent] - list an agents files
 - oaicli thread.list [agent] [list current threads]
 - oaicli thread.join [agent] [thread choice from thread.list]
 - oaicli thread.new [agent] [thread title] - stored locally matched to thread id
   
 v0.2  
 SQL lite for RAG and storage

 - agent.dialog [agent name one] [agent name two] ... - have  agents talk to eachother ala autoGPT
 - agent.local-rag [agent] - add a file to local rag for use with an agent
 - agent.function [agent] - add a file to local rag for use with an agent
 


## Development


    pyenv install 3.12
    pyenv virtualenv 3.12 oaicli
    export PYTHONPATH="[project path]/oaicli