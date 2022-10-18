from .primitives import *



@dataclass
class Not(Circuit):
    ...


@dataclass
class And(Circuit):
    _in_diode1: Diode
    _in_diode2: Diode
    _out_diode: Diode

    def __init__(self):
        power = Power()
        in_wire1, in_wire2, mid_wire, out_wire = Wire.new(4)
        self._in_diode1, self._in_diode2, self._out_diode = Diode.new(3)

        tr1 = Transistor(power, in_wire1, mid_wire)
        tr2 = Transistor(mid_wire, in_wire2, out_wire)

        self._in_diode1.output_wire = in_wire1
        self._in_diode2.output_wire = in_wire2
        self._out_diode.input_wire = out_wire

        # Tr1
        assert power.next_piece is tr1
        assert tr1.input_wire is power
        assert in_wire1.next_piece is tr1
        assert tr1.control_wire is in_wire1
        assert tr1.output_wire is mid_wire

        # Tr2
        assert mid_wire.next_piece is tr2
        assert tr2.input_wire is mid_wire
        assert in_wire2.next_piece is tr2
        assert tr2.control_wire is in_wire2
        assert tr2.output_wire is out_wire

        # Diodes
        assert self._in_diode1.output_wire is in_wire1
        assert self._in_diode2.output_wire is in_wire2
        assert out_wire.next_piece is self._out_diode
        assert self._out_diode.input_wire is out_wire
        
    def bind(self, in_wire1, in_wire2, out_wire):
        prev_in1 = self._in_diode1.input_wire
        prev_in2 = self._in_diode2.input_wire

        self._in_diode1.input_wire = in_wire1
        self._in_diode2.input_wire = in_wire2
        self._out_diode.output_wire = out_wire

        if prev_in1:
            assert prev_in1.next_piece is None
        if prev_in2:
            assert prev_in2.next_piece is None
        assert in_wire1.next_piece is self._in_diode1
        assert in_wire2.next_piece is self._in_diode2

    def signal(self):
        self._in_diode1.signal()
        self._in_diode2.signal()


@dataclass
class Nand(Circuit):
    ...


@dataclass
class Or(Circuit):
    ...


@dataclass
class Nor(Circuit):
    ...


@dataclass
class Xor(Circuit):
    ...


@dataclass
class Eq(Circuit):
    ...
