class BricklinkEinzelteil:
    def __init__(self, design_id, color, price):
        self.design_id = design_id
        self.color_dict = {}
        self.color_dict[color] = price


    def add_color(self,color,price):
        self.color_dict[color] = price