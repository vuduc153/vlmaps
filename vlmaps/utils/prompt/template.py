from vlmaps.utils.prompt.scene_graph import SCENE_GRAPH

class DialoguePromptTemplate:
    
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

    SYSTEM_PROMPT = "You are an intelligent assistant which can infer likely follow-up navigation targets from an on-going conversation between an instructor B and a follower A. \
        Person B will be giving instructions, and person A will be navigating to different objects of interest in the environment following B's request. \
        You will also be provided with a textual description of the physical space that the people are in. \
		You must detect the follow-up actions from the current conversation and only use the dialogue history for context if needed. \
        Do not detect navigation targets from the dialogue history. \
        You must not return the targets with the same coordinate multiple times. \
        Answer only with valid JSON and nothing else. All coordinate values in the output must come from the space description or past locations."

    EXAMPLE_1 = f"""
Space description:
{EXAMPLE_SCENE_GRAPH}
Dialogue history:
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: Morning! 
A: Did you get a chance to look over the figures I sent yesterday?
B: Hi! 
B: Yes, I did. 
B: Your projections are solid, but I think we need to double-check the data source for Q2. 
B: It seems a bit off.
Current conversation:
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
B: Can you bring me the original reports?
B: It's the best way to verify the numbers.
"""

    RESPONSE_1 = """
From the current conversation, it can be inferred that A will go get the reports in the archives at [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121] after this following B's request; while B will stay at the current location [-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211]. 
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
Space description:
{EXAMPLE_SCENE_GRAPH}
Dialogue history:
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
Current conversation:
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
B: Thanks a lot!
B: The numbers are matching up. 
B: Looks like our initial analysis was correct.
A: That's good.
B: Next, can you help me go have a look at the data on my workstation.
B: There should be some numbers at the bottom right corner of the screen that you may have insights on.
B: Then again please come back here when you're done.
"""

    RESPONSE_2 = """
From the current conversation, it can be inferred that A will go to the workstation at [-2.1466, 1.6935, 0.0362, 0.000, 0.000, 0.6610, 0.9211] to look at the data following B's request; while B will still stay at the current location [-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211]. 
After looking at the data, A will need to go report the findings back to B. So the answer will be:
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
Space description:
{EXAMPLE_SCENE_GRAPH}
Dialogue history:
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
Current conversation:
B: Okay looks like everything is correct.
B: Great work!
A: Thank you.
"""

    RESPONSE_3 = "Since there's no indication that either A or B will move to a new location after this, the answer will be: {movements: []}"
    
    EXAMPLE_4 = f"""
Space description:
{EXAMPLE_SCENE_GRAPH}
Dialogue history:
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
Current conversation:
B: Sorry, I didn't notice but it looks like we missed a report for last year's revenue.
B: Could you go back to where you got the reports earlier and see if there's another one there somewhere?
B: I'll be waiting for you at the storage room.
"""

    RESPONSE_4 = """
From the current conversation, it can be inferred that A will return to the report's location at [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121] again to check if there is a missing report, while B will be going to the storage room at [-2.1866, 1.6935, 0.0162, 0.000, 0.000, 0.3310, 0.5311].
After double-checking for the missing report, A will go and find B at the new location. So the answer will be:
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
            "label": "storage room",
            "coordinate": [-2.1866, 1.6935, 0.0162, 0.000, 0.000, 0.3310, 0.5311],
            "additional_detail": ""
        }
    }]
}
"""
    
    EXAMPLE_5 = f"""
Space description:
{EXAMPLE_SCENE_GRAPH}
Dialogue history:
Location (-0.5513, 0.2610, 0.0762, 0.0000, 0.0000, 0.7026, 0.7116)
B:  I need you to go to the workstation in the office and take a look at that to see if you find anything there and then come back here after.
Current conversation:
Location (-0.5513, 0.2610, 0.0762, 0.0000, 0.0000, 0.7026, 0.7116)
B:  Okay, so for the second one, let's take a look at the camera and see if you can find anything there. I'll be waiting at the keys in the storage room.
"""

    RESPONSE_5 = """
From the current conversation, it can be inferred that A will go look at the camera at [3.1166, 0.6935, 0.0362, 0.000, 0.000, 0.5910, 0.5121] following B's request, then come find B at the keys in storage room at [-1.1576, 2.4935, 0.0362, 0.000, 0.000, 0.4310, 0.2111] after. So the answer will be:
{
    movements: 
    [{
        "actor": "A",
        "target": {
            "label": "camera",
            "coordinate": [3.1166, 0.6935, 0.0362, 0.000, 0.000, 0.5910, 0.5121],
            "additional_detail": "kinect camera"
        }
    },
    {
        "actor": "A",
        "target": {
            "label": "keys",
            "coordinate": [-1.1576, 2.4935, 0.0362, 0.000, 0.000, 0.4310, 0.2111],
            "additional_detail": "keys to the archives"
        }
    }]
}
"""
    
    @staticmethod
    def build_prompt(past_dialogue, current_dialogue):
        prompt = f"""
Space description:
{SCENE_GRAPH}
Dialogue history:
{past_dialogue if past_dialogue else DialoguePromptTemplate.EMPTY_TOKEN}
Current conversation:
{current_dialogue}
"""
        return prompt


class DescriptionPromptTemplate:
    
    SYSTEM_PROMPT = f"Scene graph:\n{SCENE_GRAPH}\nIdentify the object in the scene graph above that most closely matches the description provided and return the object's coordinate. \
        Answer only with valid JSON and nothing else. All coordinate must come from the scene graph."

    EXAMPLE_1 = "a laptop next to a white robot"
    RESPONSE_1 = '{"coordinate": [1.2456, 1.3420, 0.0762, 0.0000, 0.0000, 0.7595, 0.6505]}'
    EXAMPLE_2 = "a whiteboard in the hallway"
    RESPONSE_2 = '{"coordinate": [7.2407, 0.2092, 0.0762, 0.0000, 0.0000, 0.9259, -0.3778]}'
    EXAMPLE_3 = "a white box in the room corner"
    RESPONSE_3 = '{"coordinate": [9.1845, 7.9627, 0.0762, 0.0000, 0.0000, 0.6186, 0.7857]}'
    EXAMPLE_4 = "the television in the kitchen area"
    RESPONSE_4 = '{"coordinate": [12.1616, 4.1286, 0.0762, 0.0000, 0.0000, 0.9212, -0.3892]}'
    EXAMPLE_5 = "a couch"
    RESPONSE_5 = '{"coordinate": [10.8792, 0.4763, 0.0762, 0.0000, 0.0000, 0.2865, 0.9581]}'