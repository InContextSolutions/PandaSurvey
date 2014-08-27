

class RecodeMixin:

    def recode(self):
        for rec in self.recodes:
            self.df[rec] = self.df.apply(
                lambda row: self.recodes[rec](row[rec]), axis=1)
