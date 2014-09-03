import pandas
from pandasurvey.rake import SimpleRake

__version__ = '0.0.1'


def cli():
    import argparse

    desc = """A command-line utility for weighting survey response data."""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("infile", type=str, help='input file (csv or xlsx extension expected)')
    parser.add_argument("outfile", type=str, help='output file (csv or xlsx expected)')
    parser.add_argument("target", type=str, help='target proportions file (csv or xlsx; no header)')

    args = parser.parse_args()
    if args.infile.endswith('csv'):
        df = pandas.from_csv(args.infile)
    else:
        df = pandas.from_excel(args.infile)

    weights = {}
    with open(args.target) as csv_in:
        for line in csv_in:
            demo, category, proportion = line.split(',')
            if demo not in weights:
                weights[demo] = {}
    weights[demo][int(category)] = float(proportion)

    rk = SimpleRake(df, weights, maxiter=10)
    dfout = rk.calc()

    if args.outfile.endswith('csv'):
        dfout.to_csv(args.outfile)
    else:
        dfout.to_excel(args.outfile)
