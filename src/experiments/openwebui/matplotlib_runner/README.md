# Matplotlib runner
## Summary
- this small experiment is the first stable (a bit) version of running user task against an flowise workflow to create python scripts
- at the moment the script will be automated generated and after this it is check if it uses matplotlib
- when it contains matplotlib it will be rewritten in a kind that it will produce markdown readable output
- if not -> just run the script
## Structure
- this directory contains two files
- 1. the .py file which contains the code which will be loaded by openwebui as pipeline
- 2. the exported workflow which will be used in flowise
## Hint
- if you want to use this yourself, please use your own credentials for the LLMs (provider) and change the url in the .py file (probably your API to your workflow is another then mine)
