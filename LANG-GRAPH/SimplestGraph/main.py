from langgraph.graph import Graph

def sayHi(name):
    return name+ ":Hi"

def sayHowru(input):
    return input+"\nhow are you?"


workflow = Graph()
workflow.add_node("node1",sayHi)
workflow.add_node("node2",sayHowru)
workflow.add_edge("node1","node2")

workflow.set_entry_point("node1")
workflow.set_finish_point("node2")

app = workflow.compile()
#print(app.invoke(input="Rahul"))

for output in app.stream("rahul"):
    for key, value in output.items():
       print(f"Output from {key}:")
       print("-----")
       print(value)
       print("\n-----\n")
    output





