# Description: This file contains the logic for the LLM bot
import time

def dummy_bot(msg):
    return "Dummy bot: I'm a dummy bot"

def echo_bot(msg):
    time.sleep(5)
    return 'Echo: {}'.format(msg)

def simple_llm(msg):
    return 'Simple LLM: {}'.format(msg)