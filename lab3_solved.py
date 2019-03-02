import enum
import abc
import math
import typing


class Figure(enum.Enum):
    CIRCLE = 1
    RECTANGLE = 2
    TRIANGLE = 3
    RHOMBUS = 4


class FieldCalculator(abc.ABC):
    @abc.abstractmethod
    def calculate_field(self, *args, **kwargs) -> float:
        pass


class CircleFieldCalculator(FieldCalculator):

    def calculate_field(self, r) -> float:
        r = float(r)
        return math.pi * r * r


class RectangleFieldCalculator(FieldCalculator):

    def calculate_field(self, a, b) -> float:
        a = float(a)
        b = float(b)
        return a * b


class TriangleFieldCalculator(FieldCalculator):

    def calculate_field(self, a, h) -> float:
        return 0.5 * a * h


class RhombusFieldCalculator(FieldCalculator):

    def calculate_field(self, a, b, diagonals=True) -> float:
        a = float(a)
        b = float(b)
        diagonals = bool(diagonals)
        if diagonals:
            return 0.5 * a * b
        else:
            return a * b


_CALCULATORS = {
    Figure.CIRCLE: CircleFieldCalculator(),
    Figure.RECTANGLE: RectangleFieldCalculator(),
    Figure.TRIANGLE: TriangleFieldCalculator(),
    Figure.RHOMBUS: RhombusFieldCalculator()
}


def calculate_field(fig: Figure, *args) -> typing.Optional[float]:
    """
    #1 Write a function countField which calculates the field of a given figure. It takes the following input parameters:
    For circle we get only x which stands for radius. For Rectangle x&y are the figure's sides, for triangle they are
    accordingly the base and the height and for rhombus - diagonals (4p)
    :param fig: circle/rectangle/triangle/rhombus
    :param args: x & optional y

    >>> calculate_field(Figure.RECTANGLE, 3, 4)
    12.0

    >>> calculate_field(Figure.CIRCLE)
    Traceback (most recent call last):
        ...
    ValueError: Inalid arguments number (0)


    """
    if fig is None:
        raise ValueError('figure is none')
    try:
        return _CALCULATORS[fig].calculate_field(*args)
    except TypeError:
        raise ValueError(f'Inalid arguments number ({len(args)})')


def _calculate_figure_fields(figure, *args):
    figure_t = type(figure)
    if figure_t is int:
        figure = Figure(figure)
    elif figure_t is Figure:
        pass
    else:
        figure = Figure[str(figure).upper()]
    return calculate_field(figure, *args)


def compare_figures_fields(figures: typing.List[typing.List[typing.Any]]):
    """
    #2 Write a function which takes sets of parameters of two figures and compares their fields. (4p)
    The exemplary input is [[Circle, 4], [Rhombus, 2, 4]]
    Expected output would be 'The first figure (Circle) has larger field'

    >>> compare_figures_fields([['rhombus', 3, 4, 1], ['Triangle', 6, 2.5]])
    The figure ['rhombus', 3, 4, 1] has largest field (6.000)
    Figures fields sorted descending:
    - figure ['rhombus', 3, 4, 1] with field: 6.000
    - figure ['Triangle', 6, 2.5] with field: 7.500

    """
    if not figures:
        raise ValueError('no figures given')
    pairs_of_calculated_fields = [(fig, _calculate_figure_fields(fig[0], *fig[1:])) for fig in figures]
    fields_pairs_sorted = sorted(pairs_of_calculated_fields, key=lambda x: [1], reverse=True)
    print('The figure {0} has largest field ({1:.3f})'.format(*fields_pairs_sorted[0]))
    print('Figures fields sorted descending:')
    print('\n'.join([f'- figure {fig[0]} with field: {fig[1]:.3f}' for fig in fields_pairs_sorted]))


if __name__ == '__main__':
    import doctest
    doctest.testmod()