## Assignement 2 
## Natural Language Processing 
## R00195231


#### How to run

```
# Train the chatbot
python train.py

# Run the chatbot
python chat.py
```


### Baseline Chatbot 
It has 4 py file. Descriptions are given below :
train.py - This file load the model and train the dataset into model. This file should be run first. I have used rasa_core library in baseline model. 
python version - 3.6
other library and its version are mentioned in requirements.txt

Chat.py - This file contains chat method. This file should be run for start chatting.

History.py- This file has few method to save conversation and retrieve information from chat.

feedback.py - This file contains method for feedback loop. 


### Data Files -
nlu.md - It stores all intents 

config.yml - It stored pipeline in which data will be processed and trained.

storied.md - Stories are created with combination of intent and its utterances.

domain.yml - All intents are grouped that is given in slot and template is designed for utterance for each intent.

### Library Required - 
Requirements.txt is given.

spacy download en_core_web_md




