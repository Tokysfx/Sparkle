
class project_config ():
    def __init__(self):

        self.config_project = {
            "01_PreProduction" : [
                "concept_art",
                "references",
                "storyboard"
            ],
            "02_Production" : [
                "Chara",
                "Env",
                "Props",
                "Items",
                "Modules",
                "FX",
                "00_Shot"
            ],
            "03_PostProduction" : [
                "Grading",
                "Editing",
                "DCP"
            ]            
        }

        self.department = {
            "Modeling" : [
                "Low",
                "Hight",
                "UV",
            ],
            "Surfacing" : [
                "Texturing",
                "Shading",
            ],
            "Rigging" : [
                "Block",
                "Body",
                "Facial",
            ],
            "Assembly" : [
                "Assembly",
            ],
            "FX" : [
                "FX",
            ]
        }

        self.task = {
            "Low",
            "Hight",
            "UV",
            "Texturing",
            "Shading",
            "Block",
            "Body",
            "Facial",
            "Assembly",
            "FX",
        }