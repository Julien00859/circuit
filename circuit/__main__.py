from .gates import And
from .primitives import LED
from .pprint import pprint


circuit = """
{in1}-|\\
  ||-{out}
{in2}-|/
"""

led = LED('And')
a = And()

for in1, in2 in [(x, y) for x in range(2) for y in range(2)]:
    a.bind(Wire(in1), Wire(in2), led)
    a.signal()
    print(circuit.format(in1=in1, in2=in2, out=int(led.state)))

    assert (in1 and in2) == led.state
