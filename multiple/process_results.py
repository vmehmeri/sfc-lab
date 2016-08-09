import sys

NUMBER_OF_CONTROLLERS=int(sys.argv[1])

lines = [line.rstrip('\n') for line in open('results.txt')]

flow_dict = {}

for line in lines:
    arr = line.split('.')
    ctrl_id = arr[0]
    if ctrl_id in flow_dict.keys():
        flow_dict[ctrl_id].append(arr[3])
    else:
        flow_dict[ctrl_id] = []
        flow_dict[ctrl_id].append(arr[3])

acc = 0

for ctrl_id in flow_dict.keys():
    number_of_flows = len(flow_dict[ctrl_id])
    acc += number_of_flows
    print("Controller #%s : %s flows" %(ctrl_id, number_of_flows))

print("\nNumber of controllers:", len(flow_dict), "(Expected:", NUMBER_OF_CONTROLLERS, ")")
print("Total number of flows:", acc, "(Expected:", NUMBER_OF_CONTROLLERS*255, ")")