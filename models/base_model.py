from fasthtml.components import Tr, Td, A, Div

class BaseModel:
    def __ft__(self):
        column = Tr(
            *[Td(i, cls="has-text-centered") for i in self.__dict__.values()], 
            Td(A("Edit", href=f"/admin/{self.table_name}/{self.id}"))
        )
        return column
    
    @property
    def table_name(self):
        return self.__module__.split(".")[1]