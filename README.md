Minecraft HTN Planning

HTN, Hierarchical Task Network, a problem decomposition planner. They represent planning problems as tasks to be performed vs states to achieve, and solve problems by decomposing tasks into subtasks, and subtasks into primitive operators that can be applied to change problem state.  The HTN planner finds a solution by searching across what is called an AND/OR tree, consisting of the subtasks required to accomplish a task (the ANDs), and the alternate methods for accomplishing a task (the ORs). 

A python implementation of an HTN for Minecraft crafting recipes. AutoHTN reads in recipes from a JSON file and converts them into operators and methods.

Example located in example.txt

Challenges: Figuring out how to read crafting recipes in JSON and have them read into operators and methods. Understanding the recursive nature of an HTN calling itself but with different subtasks which eventually build back into the item/resource.

Learned: How to utilize HTN's as a means for AI planning in a familiar game's context. 
