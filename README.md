# OAICLI 🕶️
**A Command Line Interface to Open AI**
_(pronounced Oakley (IPA oʊk.li), like the sunglasses)_
---

OAICLI is designed to help developers create and use assistants, which were launched on OpenAI Dev Day, November 2023.

Threads, messages, and thread runs are abstracted, to make the user experience of creating and chatting with agents simpler.

Use at your own risk. I built this for myself, but feel free to open issues and PRs.
If runs reach a time limit, they will be canceled.

If you want a complete implementation of what Assistants are capable of, you can use the friendly [OpenAI playground](https://platform.openai.com/playground).



## installation

`pip install oaicli`

Next, creat an `.env` file in your project home:

    OPENAI_API_KEY  = "[your key]"
    OPEN_AI_MODEL_TYPE = "gpt-4-1106-preview"
    OPEN_AI_VISION_MODEL_TYPE = "gpt-4-1106-vision-preview"


When you first run `oaicli`, it will install the `.oaicli` directory in the project location

    /oaicli/agent/agents.yaml (agent names-> ids)
    /oaicli/agent/[agent id]/instructions.yaml
    /oaicli/threads/threads.yaml (thread names-> ids)
    /oaicli/threads/[thread id]/[message id].txt
    /oaicli/files/[file id]/[filename]

The above directory structure should let you check in your work to
your code repository and track changes.

Agents and threads are given names to make it easier
Files can be added to conversation.

## Commands

oaicli -h | --help for help

Threads are stored in append only textfiles.

 - oicli start - allows you to start up, choose a thread by name


## Roadmap

### v0.2

 - oaicli thread.list [agent] lists current threads
 - oaicli thread.join [agent] [thread choice from thread.list]
 - oaicli thread.new [agent] [thread title] - stored locally matched to thread id

Maintanence functions

 - oaicli agent.list - list agents
 - oaicli agent.create [agent name] - create a new agent
 - oaicli agent.edit [agent] [prompt | name | params] - edit something about the agent
 - oaicli agent.delete [agent] - delete an agent (don't be mean)
 - oaicli agent.file-upload [agent] [path] - send a file to your agent
 - oaicli agent.directory-upload [agent] [path] - takes all text files and pdf files and uploads content
 - oaicli agent.url-upload [agent] [URL]
 - oaicli agent.file-list [agent] - list an agents files

### v0.3

 - agent.dialog [agent name one] [agent name two] ... - have  agents talk to eachother ala autoGPT
 - agent.local-rag [agent] - add a file to local rag for use with an agent
 - agent.function [agent] - add a file to local rag for use with an agent
 - pydantic, mypy for typing
 - tox and testing

### v0.4

  - [shell completion](https://click.palletsprojects.com/en/8.1.x/shell-completion/) for commands and directories and files (clicko?)
  -  SQL lite for RAG and storage
  - tools support https://platform.openai.com/docs/api-reference/assistants/createAssistant#assistants-createassistant-tools


## Development

https://github.com/HumanAssistedIntelligence/OAICLI


    pyenv install 3.12
    pyenv virtualenv 3.12 oaicli
    export PYTHONPATH="[project path]/oaicli
    pip install .