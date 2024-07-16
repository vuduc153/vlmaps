class PromptTemplate:

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
                    "additional_detail": "Dan's workstation"
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

	SYSTEM_PROMPT = "You will be provided with the information about a physical space under `=== SCENE REPRESENTATION ===`, the information about a conversation dialogue under `=== PAST DIALOGUE ===` and `=== CURRENT DIALOGUE ===`, \
	and the positions of the speakers. Use the information to deduce the expected sequence of follow-up movements for the speakers. Your output must be in JSON format. All values in the output must come from `=== SCENE REPRESENTATION ===`."


	EXAMPLE_1 = f"""
=== SCENE REPRESENTATION ===
{EXAMPLE_SCENE_GRAPH}
=== PAST DIALOGUE ===
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: "Morning! Did you get a chance to look over the figures I sent yesterday?"
B: "Hi! Yes, I did. Your projections are solid, but I think we need to double-check the data source for Q2. It seems a bit off."
=== CURRENT DIALOGUE ===
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: "Good point. How about we go pull out the original reports? It's the best way to verify the numbers."
B: "Agreed. Let's head there. We might find more insights with the raw data in hand."
A: "Perfect. I'll go grab the keys to the archives. Last time, some of the files were mislabeled, so it might take a bit of digging."
"""

	RESPONSE_1 = """
A and B will go get the reports in the archives at [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121] together after this; but before that, A will have to go to get the keys to the archives at [-1.1576, 2.4935, 0.0362, 0.000, 0.000, 0.4310, 0.2111]. So the answer will be:
{
    movements: 
    [{
        "actor": "A",
        "target": {
            "label": "keys",
            "coordinate": [-1.1576, 2.4935, 0.0362, 0.000, 0.000, 0.4310, 0.2111],
            "additional_detail": "key to the archives"
        }
    }, 
    {
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
            "label": "reports",
            "coordinate": [1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121],
            "additional_detail": ""
        }
    }]
}
"""

	EXAMPLE_2 = f"""
=== SCENE REPRESENTATION ===
{EXAMPLE_SCENE_GRAPH}
=== PAST DIALOGUE ===
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: "Morning! Did you get a chance to look over the figures I sent yesterday?"
B: "Hi! Yes, I did. Your projections are solid, but I think we need to double-check the data source for Q2. It seems a bit off."
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: "Good point. How about we go pull out the original reports? It's the best way to verify the numbers."
B: "Agreed. Let's head there. We might find more insights with the raw data in hand."
A: "Perfect. I'll go grab the keys to the archives. Last time, some of the files were mislabeled, so it might take a bit of digging."
=== CURRENT DIALOGUE ===
Location (1.3114, 0.7123, 0.2313, 0.000, 0.0010, 0.2141, 0.6121)
B: "The numbers are matching up. Looks like our initial analysis was correct. This is a relief."
A: "Great work! I'll stay here a bit longer to reorganize these files for next time. Could you take the verified reports back up?"
B: "Sure thing. I will put the keys back when I’m at it. See you back upstairs.”
"""

	RESPONSE_2 = """
A and B were originally at [-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211], and B will be returning there, but not before returning the keys to their original location at [-1.1576, 2.4935, 0.0362, 0.000, 0.000, 0.4310, 0.2111]. A will stay in the new location, so the answer will be: 
{
    movements:
    [{
        "actor": "B",
        "target": {
            "label": "keys",
            "coordinate": [-1.1576, 2.4935, 0.0362, 0.000, 0.000, 0.4310, 0.2111],
            "additional_detail": "key to the archives"
        }
    }, 
    {
        "actor": "B",
        "target": {
            "label": "",
            "coordinate": [-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211],
            "additional_detail": ""
        }
    }]
}
"""

	EXAMPLE_3 = f"""
=== SCENE REPRESENTATION ===
{EXAMPLE_SCENE_GRAPH}
=== CURRENT DIALOGUE ===
Location (-1.2066, 4.6135, 0.0062, 0.000, 0.000, 0.5610, 0.9211)
A: "Morning! Did you get a chance to look over the figures I sent yesterday?"
B: "Hi! Yes, I did. Your projections are solid. Great work!"
"""

	RESPONSE_3 = "Since there's no indication that either A or B will move to a new location after this, the answer will be: {movements: []}"

	TEMP_SCENE_GRAPH = """
{
    "function": "office building",
    "additional_detail": "Melbourne Connect",
    "rooms": [
        {
            "coordinate": [5.7326, 7.0397, 0.0762, 0.0000, 0.0000, -0.8627, 0.5057],
            "scene_category": "IxT lab",
            "additional_detail": "Interactive user interface laboratory",
            "objects": [
                {
                    "class_": "workstation",
                    "coordinate": [-1.3229, 3.2359, 0.0762, 0.0000, 0.0000, -0.4356, 0.9001],
                    "additional_detail": "Dan's workstation"
                }, {
                    "class_": "tv",
                    "coordinate": [2.8889, 6.7676, 0.0762, 0.0000, 0.0000, 0.4850, 0.8745],
                    "additional_detail": "big display"
                }, {
                    "class_": "3d printer",
                    "coordinate": [1.0564, 1.1280, 0.0762, 0.0000, 0.0000, -0.4669, 0.8843],
                    "additional_detail": "can be used for students' projects"
                },
                {
                    "class_": "mirror",
                    "coordinate": [-1.4979, 6.2643, 0.0762, 0.0000, 0.0000, 0.8149, 0.5796],
                    "additional_detail": ""
                }
            ]
        }
    ]
}
"""
	
	@staticmethod
	def build_prompt(past_dialogue, current_dialogue):
		prompt = f"""
=== SCENE REPRESENTATION ===
{PromptTemplate.TEMP_SCENE_GRAPH}
=== PAST DIALOGUE ===
{past_dialogue}
=== CURRENT DIALOGUE ===
{current_dialogue}
"""
		return prompt
