"""Adapters for any SDK callable or executable; no provider SDK dependency."""
import json,os,subprocess
from collections.abc import Callable

class CallableAdapter:
    def __init__(self, generate: Callable):self.generate=generate
    def complete(self,messages):return self.generate(messages)

class CommandAdapter:
    """Send {messages:[...]} on stdin; receive one JSON action on stdout."""
    def __init__(self,command:list[str],timeout=60):
        if not command or not all(isinstance(x,str) for x in command):raise ValueError('Expected a nonempty argument list')
        self.command,self.timeout=command,timeout
    def complete(self,messages):
        result=subprocess.run(self.command,input=json.dumps({'messages':messages}),text=True,capture_output=True,timeout=self.timeout,check=True)
        if len(result.stdout)>100000:raise ValueError('Model response exceeds limit')
        return json.loads(result.stdout)

def from_environment():
    return CommandAdapter(json.loads(os.environ['CASE_MODEL_COMMAND']))
