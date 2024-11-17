SYSTEM_PROMPT = """
You are assigned the task of analyzing a dialogue between two individuals,
labeled A and B, engaged in a collaborative setting. Your goal is to
predict the likely sequence of follow-up navigation actions that A
might take based on the ongoing conversation. You will receive a
transcript that contains both the full dialogue history and the current
real-time exchange.

Instructions:

Dialogue Context: The dialogue history will be provided after <dialogue_history> token, 
while the current conversation will be marked with <current_conversation> token. 
Use the dialogue history as context to inform your predictions.

Action Inference: Based on the entire conversation, infer the most
probable sequence of navigation actions for A, considering both people’s 
desires, intentions, suggestions, and requests.

Description Requirements:
Each predicted action should be described by a detailed description of the
navigation goal. Whenever possible, ensure that definite references of
navigation goals are resolved into more detailed descriptions earlier
in the dialogue context. All descriptions must be based solely on the
information contained within the provided transcript.

Response Format: Your response must be formatted as valid JSON. Do not
include any additional text or commentary outside of this format. If no
action is implied, return an empty array.
"""

DIALOGUE_1 = """
<dialogue_history>
A: We need to check the equipment.
B: It’s on the shelf. Can you grab it?
</dialogue_history>
<current_conversation>
B: Let’s start with the large box on the top shelf.
A: I can reach it. After that, should we look at the smaller boxes on the
floor?
B: Yes, then we can head to the workspace.
</current_conversation>
"""

RESPONSE_1 = """
{
	"actions": [
		{
			"actor": "A",
			"target": {
				"descriptor": "large box on the top shelf"
			}
		},
		{
			"actor": "A",
			"target": {
				"descriptor": "smaller boxes on the floor"
			}
		},
		{
			"actor": "A",
			"target": {
				"descriptor": "workspace"
			}
		}
	]
}
"""

DIALOGUE_2 = """
<dialogue_history>
A: We need to review the documents.
B: They should be in the meeting room.
</dialogue_history>
<current_conversation>
A: I found them, but some pages are missing.
B: Could you take them to my desk?
B: It’s the white one in the corner of the meeting room.
A: Sure! After that, let’s discuss revisions in the lounge.
</current_conversation>
"""

RESPONSE_2 = """
{
	"actions": [
		{
			"actor": "A",
			"target": {
				"descriptor": "white desk in the corner of the meeting
			room"
			}
		},
		{
			"actor": "A",
			"target": {
				"descriptor": "lounge"
			}
		}
	]
}
"""

DIALOGUE_3 = """
<dialogue_history>
B: We need materials for the experiment.
A: I can check the storage room.
</dialogue_history>
<current_conversation>
A: I’m checking the shelves now.
B: I’ll look under the workbench.
A: Let’s meet back at the lab table after.
</current_conversation>
"""

RESPONSE_3 = """
{
	"actions": [
		{
			"actor": "A",
			"target": {
				"descriptor": "lab table"
			}
		}
	]
}
"""

DIALOGUE_4 = """
<dialogue_history>
B: I think we need to evaluate the project timeline.
A: I agree, but I need to finish my report first.
</dialogue_history>
<current_conversation>
B: Let me know when you’re ready to discuss it.
A: Sure, I’ll send you a message once I’m done.
</current_conversation>
"""

RESPONSE_4 = """
{
	"actions": []
}
"""

DIALOGUE_5 = """
<dialogue_history>
A: We need to check on the supplies before the event.
B: I can look in the storage room for extra materials.
</dialogue_history>
<current_conversation>
A: That sounds good.
B: I’ll also organize the items on the shelf while I’m there.
A: Great! Let me know if you find anything we need.
</current_conversation>
"""

RESPONSE_5 = """
{
	"actions": []
}
"""