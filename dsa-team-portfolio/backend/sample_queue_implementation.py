from doubly_ended_queue import Queue
import random

line = Queue()
customer_state = {
    "Alex": "Regular",
    "Bethany": "Pregnant",
    "Carly": "Senior",
    "Dennis": "Regular",
    "Ezekiel": "Regular",
    "Francine": "Regular",
    "Gregorio": "Senior"
}

customer_set = set()
priority = []
while len(customer_set) < len(customer_state):
    customer = random.choice(list(customer_state.keys()))
    if customer in customer_set:
        continue
    customer_set.add(customer)
    state = customer_state[customer]
    current_head = line.head
    if state != "Regular":
        if line.head and customer_state[line.head.data] != "Regular":
            while customer_state[current_head.data] != "Regular":
                priority.append(current_head.data)
                current_head = current_head.next 
        else:
            priority.append(customer)    
    else:
        line.enqueue(customer)

    print(customer)

priority.reverse()
for prio in priority:
    line.enqueue_at_head(prio)

current = line.head
while current:
    print(current.data, end=" -> ")
    current = current.next
print("None")
    