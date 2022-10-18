from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field


class Circuit(metaclass=ABCMeta):
    @abstractmethod
    def signal(self):
        pass

    @classmethod
    def new(cls, n=1):
        return [cls() for _ in range(n)]


@dataclass
class BaseWire(Circuit):
    state: bool = False
    next_piece: Circuit | None = None

    def signal(self):
        self.next_piece.signal()


@dataclass
class Power(BaseWire):
    state = property(lambda self: True, lambda self, _: None)


@dataclass
class Ground(BaseWire):
    state = property(lambda self: False, lambda self, _: None)


@dataclass
class Wire(BaseWire):
    def switch_on(self):
        self.state = True
        self.signal()

    def switch_off(self):
        self.state = False
        self.signal()


@dataclass
class LED:
    name: str
    state: bool = False

    def signal(self):
        status = '[on]/off' if self.state else 'on/[off]'
        print(f'LED {self.name!r} is {status}')


class Rewire:
    def __set_name__(self, owner, name):
        self._wire_name = f'_{name}'

    def __get__(self, obj, objtype=None):
        return getattr(obj, self._wire_name)

    def __set__(self, obj, value):
        if wire := getattr(obj, self._wire_name, None):
            wire.next_piece = None
        if value:
            value.next_piece = obj
        setattr(obj, self._wire_name, value)


@dataclass
class Diode(Circuit):
    input_wire: Wire | None = Rewire()
    output_wire: Wire | None

    def __init__(self, input_wire=None, output_wire=None):
        self.input_wire = input_wire
        self.output_wire = output_wire

    def signal(self):
        if self.input_wire.state != self.output_wire.state:
            self.output_wire.state = self.input_wire.state
            self.output_wire.signal()


@dataclass
class Transistor(Circuit):
    input_wire: Wire = Rewire()
    control_wire: Wire = Rewire()
    output_wire: Wire

    def signal(self):
        in_ = self.input_wire.state
        ctrl = self.control_wire.state
        out = self.output_wire.state

        if in_ and ctrl and not out:
            self.output_wire.switch_on()

        elif out and (not ctrl or not in_):
            self.output_wire.switch_off()
