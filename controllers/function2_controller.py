from logic.funtion2_logic import start_double_click_copy_monitor, human_type_handler

class Function2Controller:
    def __init__(self):
        self.actions = [
            "Double click để sao chép",
            "Human type"
        ]

    def get_available_features(self):
        return self.actions

    def bind_feature(self, selected_feature: str, widget):
        if selected_feature == "Double click để sao chép":
            start_double_click_copy_monitor()
