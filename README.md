# OAICLI 🕶️
**A Command Line Interface to Open AI**
_(pronounced Oakley (IPA oʊk.li)_
---

OAICLI is designed to help developers create and use assistants, which were launched on OpenAI Dev Day, November 2023.

Threads, messages, and thread runs are abstracted, to make the user experience of creating and chatting with agents simpler.
Your files, agent prompts, and messages will be saved to `.oaicli`, from which you can edit prompts and files.

**Use at your own risk.**

I built this for myself. Feel free to open issues and PRs.
If you want a complete implementation of what Assistants are capable of, you can use the friendly [OpenAI playground](https://platform.openai.com/playground).



## installation

`pip install oaicli`

Next, creat an `.env` file in your project home:

    OPENAI_API_KEY  = "[your key]"
    OPEN_AI_MODEL_TYPE = "gpt-4-1106-preview"
    OPEN_AI_VISION_MODEL_TYPE = "gpt-4-1106-vision-preview"


When you first run `oaicli`, it will install the `.oaicli` directory in the project location.
You could version prompts for example in your repo, and then update your agents.

Threads are given names to make it easier to choose.


## Commands

    oaicli -h | --help for help

### Quickstart

 `oaicli start` - allows you to start up quickly, choose a thread, agent, and start communicating.

 If runs reach a time limit, they will be canceled.

### File and Agent maintenance

 Otherwise there is some agent and file maintenence.

    oaicli file upload
    oaicli file list
    oaicli file download-all



![Screenshot of running oaicli start](screenshot.png?raw=true "Running oaicli start")

## experimental

Probably broken. If you want autocompletion (useful for editing agents and uploading files)

For Bash:

    eval "$(_OAICLI_COMPLETE=source_bash oaicli)"

For Zsh:

    eval "$(_OAICLI_COMPLETE=source_zsh oaicli)"

## Roadmap

### v0.3

 - upload doc from url, or get web contents
 - cat a directory into a single file and upload
 - share publicically OAICLI help agent, uploading entire github repo. For example "what changes would you make to README.md based on the source code"

 ### v1.x

Have agents select and talk to each other.

Other:

 - agent.dialog [agent name one] [agent name two] ... - have  agents talk to eachother ala autoGPT
 - agent.local-rag [agent] - add a file to local rag for use with an agent
 - agent.function [agent] - add a file to local rag for use with an agent
 - pydantic, mypy for typing
 - tox and testing
 - [shell completion](https://click.palletsprojects.com/en/8.1.x/shell-completion/) for commands and directories and files (clicko?)
 -  SQL lite for RAG and storage
 - tools support https://platform.openai.com/docs/api-reference/assistants/createAssistant#assistants-createassistant-tools
 - function call support

## Development

https://github.com/HumanAssistedIntelligence/OAICLI
https://pypi.org/project/oaicli/

    pyenv install 3.12
    pyenv virtualenv 3.12 oaicli
    export PYTHONPATH="[project path]/oaicli
    pip install .
