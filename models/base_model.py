from fasthtml.components import Tr, Td

class BaseModel:
    def __ft__(self):
        column = Tr(
            *[Td(i, cls="has-text-centered") for i in self.__dict__.values()]
        )
        return column