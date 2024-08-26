from vlmaps.utils.prompt.scene_graph import SCENE_GRAPH

class PromptTemplate:
    
    EMPTY_TOKEN = "<empty>"

    EXAMPLE_SCENE_GRAPH = """
{
    "function": "office building",
    "additional_detail": "",
    "rooms": [
        {
            "coordinate": [-1.1866, 3.6935, 0.0162, 0.000, 0.000, 0.3610, 0.9311],
            "scene_category": "archives",
            "additional_detail": "",
            "objects": [
                {
                    "class_": "workstation",
                    "coordinate": [-2.1466, 1.6935, 0.0362, 0.000, 0.000, 0.6610, 0.9211],
                    "additional_detail": ""
                }, {
                    "class_": "camera",
                    "coordinate": [3.1166, 0.6935, 0.0362, 0.000, 0.000, 0.5910, 0.5121],
                    "additional_detail": "kinect camera"
                }, {
                    "class_": "reports",
                    "coordinate": [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121],
                    "additional_detail": ""
                }
            ]
        },
        {
            "coordinate": [-2.1866, 1.6935, 0.0162, 0.000, 0.000, 0.3310, 0.5311],
            "scene_category": "storage room",
            "additional_detail": "",
            "objects": [
                {
                    "class_": "keys",
                    "coordinate": [-1.1576, 2.4935, 0.0362, 0.000, 0.000, 0.4310, 0.2111],
                    "additional_detail": "keys to the archives"
                }
            ]
        }
    ]
}
"""

    SYSTEM_PROMPT = "You are an intelligent assistant which can infer likely follow-up locomotion actions from a transcript of a dialogue between two humans. \
		You will be provided with both the complete transcript of the dialogue history up until the present, and the real-time transcript of the current live conversation. \
        The dialogue history will be marked with <dialogue_history> token and the current conversation will be marked with <current_conversation> token. \
        Use the dialogue history for context and use only the current conversation to detect intentions for follow-up actions. \
        You will also be provided with a textual description of the physical space of the two people, which will be marked with <scene_representation> token. \
        The locations of the speakers when the dialogues were spoken will also be provided for temporal context. Use the information to infer the most likely follow-up movements for the speakers. \
        Once again, it is very important to only infer follow-up actions from the current conversation, but not from the dialogue history. \
        Answer only with valid JSON and nothing else. All coordinate values in the output must come from <scene_representation> or past locations."

    EXAMPLE_1 = f"""
<scene_representation>
{EXAMPLE_SCENE_GRAPH}
<dialogue_history>
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: Morning! 
A: Did you get a chance to look over the figures I sent yesterday?
B: Hi! 
B: Yes, I did. 
B: Your projections are solid, but I think we need to double-check the data source for Q2. 
B: It seems a bit off.
<current_conversation>
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
B: Can you bring me the original reports?
B: It's the best way to verify the numbers.
A: Okay.
A: I'll be right back.
"""

    RESPONSE_1 = """
From the current conversation, it can be inferred that A will go get the reports in the archives at [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121] after this; while B will stay at the current location [-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211]. 
After getting the report, A will bring them back to B. So the answer will be:
{
    movements: 
    [{
        "actor": "A",
        "target": {
            "label": "reports",
            "coordinate": [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121],
            "additional_detail": ""
        }
    },
    {
        "actor": "A",
        "target": {
            "label": "return",
            "coordinate": [-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211],
            "additional_detail": ""
        }
    }]
}
"""

    EXAMPLE_2 = f"""
<scene_representation>
{EXAMPLE_SCENE_GRAPH}
<dialogue_history>
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: Morning! 
A: Did you get a chance to look over the figures I sent yesterday?
B: Hi! 
B: Yes, I did. 
B: Your projections are solid, but I think we need to double-check the data source for Q2. 
B: It seems a bit off.
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
B: Can you bring me the original reports?
B: It's the best way to verify the numbers.
A: Okay.
A: I'll be right back.
<current_conversation>
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
B: Thanks a lot!
B: The numbers are matching up. 
B: Looks like our initial analysis was correct.
A: That's good.
B: Next, can you help me go have a look at the data on my workstation.
B: There should be some numbers at the bottom right corner of the screen that you may have insights on.
B: Then again please come back here when you're done.
A: Okay got it. 
"""

    RESPONSE_2 = """
From the current conversation, it can be inferred that A will go to the workstation at [-2.1466, 1.6935, 0.0362, 0.000, 0.000, 0.6610, 0.9211] to look at the data; while B will still stay at the current location [-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211]. 
After looking at the data, A will need to go report the findings back to B. From the past dialogue it can also be inferred that A would go to get the reports then return to B, but these actions are in the past, so they won't be included in the answer. So the answer will be:
{
    movements:
    [{
        "actor": "A",
        "target": {
            "label": "workstation",
            "coordinate": [-2.1466, 1.6935, 0.0362, 0.000, 0.000, 0.6610, 0.9211],
            "additional_detail": ""
        }
    }, 
    {
        "actor": "A",
        "target": {
            "label": "return",
            "coordinate": [-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211],
            "additional_detail": ""
        }
    }]
}
"""

    EXAMPLE_3 = f"""
<scene_representation>
{EXAMPLE_SCENE_GRAPH}
<dialogue_history>
{EMPTY_TOKEN}
<current_conversation>
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: Morning! 
A: Did you get a chance to look over the figures I sent yesterday?
B: Hi! 
B: Yes, I did. 
B: Your projections are solid. 
B: Great work!
"""

    RESPONSE_3 = "Since there's no indication that either A or B will move to a new location after this, the answer will be: {movements: []}"
    
    EXAMPLE_4 = f"""
<scene_representation>
{EXAMPLE_SCENE_GRAPH}
<dialogue_history>
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: Morning! 
A: Did you get a chance to look over the figures I sent yesterday?
B: Hi! 
B: Yes, I did. 
B: Your projections are solid, but I think we need to double-check the data source for Q2. 
B: It seems a bit off.
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
B: Can you bring me the original reports?
B: It's the best way to verify the numbers.
A: Okay.
A: I'll be right back.
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
B: Thanks a lot!
B: The numbers are matching up. 
B: Looks like our initial analysis was correct.
A: That's good.
B: Next, can you help me go have a look at the data on my workstation.
B: There should be some numbers at the bottom right corner of the screen that you may have insights on.
B: Then again please come back here when you're done.
A: Okay got it.
<current_conversation>
B: Sorry, I didn't notice but it looks like we missed a report for last year's revenue.
B: Could you go back to where you got the reports earlier and see if there's another one there somewhere?
B: I'll be waiting for you at the storage room.
"""

    RESPONSE_4 = """
From the current conversation, it can be inferred that A will return to the report's location at [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121] again to check if there is a missing report, while B will be going to the storage room at [-2.1866, 1.6935, 0.0162, 0.000, 0.000, 0.3310, 0.5311].
After double-checking for the missing report, A will go and find B at the new location. From the past dialogue it can also be inferred that A would go to get the reports, return to B, then go to the workstation, but these actions are in the past, so they won't be included in the answer. So the answer will be:
{
    movements: 
    [{
        "actor": "A",
        "target": {
            "label": "reports",
            "coordinate": [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121],
            "additional_detail": ""
        }
    },
    {
        "actor": "B",
        "target": {
            "label": "storage room",
            "coordinate": [-2.1866, 1.6935, 0.0162, 0.000, 0.000, 0.3310, 0.5311],
            "additional_detail": ""
        }
    },
    {
        "actor": "A",
        "target": {
            "label": "storage room",
            "coordinate": [-2.1866, 1.6935, 0.0162, 0.000, 0.000, 0.3310, 0.5311],
            "additional_detail": ""
        }
    }]
}
"""
    
    @staticmethod
    def build_prompt(past_dialogue, current_dialogue):
        prompt = f"""
<scene_representation>
{SCENE_GRAPH}
<dialogue_history>
{past_dialogue if past_dialogue else PromptTemplate.EMPTY_TOKEN}
<current_conversation>
{current_dialogue}
"""
        return prompt
