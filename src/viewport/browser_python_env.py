import random
from types import ModuleType

import anon_func as af

max_namespaces = 100000


class BrowserNamespaceWrapper:
    _mod: ModuleType
    _mod_locals: dict
    global_level: bool

    _name: str
    _doc: str

    def __init__(self, name, doc: (str, None) = None, add_main=True, global_level=True):
        self._name = name
        self._doc = doc
        if doc is None:
            _doc = "A unique namespace for running In-Browser Python code."

        self._mod = ModuleType("name", f"(BrowserNamespace: {self._name}) " + self._doc)
        self._mod_locals = {}

        if add_main:
            self.globals.update({"main": namespaces["main"]})

        # Lets be honest, I don't there'd ever be much reason for this to be false.
        self.global_level = global_level
        self.initial_imports()

    def initial_imports(self):
        self.run("import game, dungeonsheets, db, viewport")

    def reset(self):
        self._mod = ModuleType("name", f"(BrowserNamespace: {self._name}) " + self._doc)
        self._mod_locals = {}
        self.initial_imports()

    @property
    def name(self):
        return self._mod.__name__

    @property
    def doc(self):
        return self._mod.__doc__

    @property
    def globals(self):
        return self._mod.__dict__

    @globals.setter
    def globals(self, value):
        self._mod.__dict__ = value

    @property
    def locals(self):
        if self.global_level:
            return self.globals
        return self._mod_locals

    @locals.setter
    def locals(self, value):
        if self.global_level:
            self.globals = value
        self._mod_locals = value

    def get_var(self, attr):
        return getattr(self._mod, attr)

    def set_var(self, attr, val):
        setattr(self._mod, attr, val)

    def has_var(self, attr):
        return hasattr(self._mod, attr)

    def del_var(self, attr):
        return delattr(self._mod, attr)

    def call(self, attr, args=(), kwargs=None, no_return=False):
        if kwargs is None:
            kwargs = {}

        if no_return:
            getattr(self._mod, attr)(*args, **kwargs)
            return None
        else:
            return getattr(self._mod, attr)(*args, **kwargs)

    def run(self, p_code, p_return=None, params: (dict, None) = None):

        if isinstance(params, dict):
            # This should all us to pass JS variables into the python code, without cluttering up the global namespace.

            # old_global_keys = list(self.globals.keys())
            self.locals.update(params)
            retVal = af.rexec(
                p_code,
                p_return,
                self.globals,
                self.locals,
                f"browser_python_env.{self.name}",
            )
            # for key in params.keys():
            #     if key not in old_global_keys:
            #         del self.locals[key]
            return retVal

        else:
            return af.rexec(
                p_code,
                p_return,
                self.globals,
                self.locals,
                f"browser_python_env.{self.name}",
            )

    def exec(self, code: str, args=None, main_globals=True):
        if args is None:
            args = {}

        if main_globals:
            # return af.func(tuple(args.keys()), code, use_globals={'game': game}.update(browser_python_env.namespaces['main'].globals))(*tuple(args.values()))
            return af.func(
                tuple(args.keys()),
                code,
                __globals=self.globals,
                __locals=self.locals,
                collect_locals=False,
            )(*tuple(args.values()))
        else:
            return af.func(tuple(args.keys()), code, collect_locals=False)(
                *tuple(args.values())
            )


namespaces = {
    "main": BrowserNamespaceWrapper(
        "main", "Primary namespace for running In-Browser Python code", False
    )
}


def get_new_namespace_id():
    new_id = "n-py0"
    while new_id not in namespaces:
        new_id = f"n_py{random.randint(1, max_namespaces)}"

    return new_id


def create_new_namespace(name: str = "", add_main=True, global_level=True):
    global namespaces
    if name == "" or name is None:
        name = get_new_namespace_id()

    namespaces[name] = BrowserNamespaceWrapper(
        name,
        f"A unique namespace for running In-Browser Python code. Namespace: {name}",
        add_main,
        global_level,
    )
    return name


def create_namespace_if_dne(name: str, add_main=True, global_level=True):
    global namespaces
    if name in namespaces:
        return True

    namespaces[name] = BrowserNamespaceWrapper(
        name,
        f"A unique namespace for running In-Browser Python code. Namespace: {name}",
        add_main,
        global_level,
    )
    return False


def remove_namespace(name: str):
    global namespaces
    del namespaces[name]


def namespace_exists(name: str = ""):
    global namespaces
    return name in namespaces





def global_reset():
    global namespaces
    namespaces = {
        "main": BrowserNamespaceWrapper(
            "main", "Primary namespace for running In-Browser Python code", False
        )
    }
