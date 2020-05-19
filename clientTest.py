from ap.ap import ap
import time

agent = ap()
agent.login('shiyu','wozhendehaoshuai')
agent.unlock_car(1)
time.sleep(2)
agent.return_car(1)