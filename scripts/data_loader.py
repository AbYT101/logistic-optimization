import pandas as pd

class DataLoader:
    def __init__(self, completed_orders_path, delivery_requests_path):
        self.completed_orders_path = completed_orders_path
        self.delivery_requests_path = delivery_requests_path

    def load_completed_orders(self):
        return pd.read_csv(self.completed_orders_path)

    def load_delivery_requests(self):
        return pd.read_csv(self.delivery_requests_path)
