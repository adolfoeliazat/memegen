import yorm
from yorm.types import String, List

from ..domain import Template


@yorm.attr(name=String)
@yorm.attr(link=String)
@yorm.attr(default=List.of_type(String))
@yorm.attr(aliases=List.of_type(String))
@yorm.attr(regexes=List.of_type(String))
@yorm.sync("{self.root}/{self.key}/config.yml")
class TemplateModel:
    """Persistence model for templates."""

    def __init__(self, key, root):
        self.key = key
        self.root = root
        self.name = ""
        self.default = []
        self.link = ""
        self.aliases = []
        self.regexes = []

    @property
    def domain(self):
        return Template(
            key=self.key,
            name=self.name,
            lines=self.default,
            aliases=self.aliases,
            patterns=self.regexes,
            link=self.link,
            root=self.root,
        )


class TemplateStore:

    def __init__(self, root):
        self.root = root
        self._items = {}
        print(list(yorm.match(TemplateModel, root=self.root)))
        for template in yorm.match(TemplateModel, root=self.root):
            if template.key[0] not in ('.', '_'):
                self._items[template.key] = template

    def read(self, key):
        try:
            model = self._items[key]
        except KeyError:
            return None
        else:
            return model.domain

    def filter(self, **_):
        templates = []
        for model in self._items.values():
            templates.append(model.domain)
        return templates
