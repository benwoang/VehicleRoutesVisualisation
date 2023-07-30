class SolutionInput:
    # Format
    # Agent
    # 0	31x79-w5.map	79	31	41	18	71	0	0
    # Agent number, map file, map width, map height, x y of start position, x y of end position, dummy number

    # Tasks
    # 0	24	15	28	12	19	37	26	44
    # 1	(39	10	24	18)	(154	196	177	219)
    # Task number, pickup x y, pickup time window (I forgot to explain to you time window, just put 0, 300), delivery xy, delivery time window
    def __init__(self, map_string=None) -> None:
        self.tasks = []
        self.agents = []
        if map != None:
            self.map_string = map
        else:
            self.map_string = ""

    def add_new_agent(self):
        pass

    def remove_agent(self):
        pass

    def add_task(self):
        pass

    def remove_task(self):
        pass

    def generate_text_file(self):
        pass
