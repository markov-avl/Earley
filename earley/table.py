class Table:
    def __init__(self, k):
        self.rows = []
        self.k = k

    def add_row(self, row, completes=None):
        if row not in self.rows:
            self.rows.append(row)

        if completes is not None and completes not in row.completes:
            row.completes.append(completes)

    def get_rows(self):
        return self.rows

    def __len__(self):
        return len(self.rows)
