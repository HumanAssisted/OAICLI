# OAICLI
Command Line Interface to Open AI

Designed to take advantage of features launched on OpenAI Dev Day November 2023.
OAICLI is designed to help developers create easy to use agents to support their work.
If you want an interface, you can use the friendly [https://platform.openai.com/playground](https://platform.openai.com/playground). 

## Commands

oaicli

v0.1

Threads are stored in append only textfiles.

 - agent.list - list agents
 - agent.create [agent name] - create a new agent 
 - agent.edit [agent] [prompt | name | params] - edit something about the agent
 - agent.delete [agent] - delete an agent (don't be mean)
 - agent.file-upload [agent] [path] - send a file to your agent
 - agent.directory-upload [agent] [path] - takes all text files and pdf files and uploads content
 - agent.url-upload [agent] [URL]
 - agent.file-list [agent] - list an agents files
 - thread.list [agent] [list current threads]
 - thread.join [agent] [thread choice from thread.list]
 - thread.new [agent] [thread title] - stored locally matched to thread id
   
 v0.2  
 SQL lite for RAG and storage

 - agent.dialog [agent name one] [agent name two] ... - have  agents talk to eachother ala autoGPT
 - agent.local-rag [agent] - add a file to local rag for use with an agent
 - agent.function [agent] - add a file to local rag for use with an agent
 
