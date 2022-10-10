"""Main CLI interface will live here """

import argparse


if __name__ == "__main__":
    # Create the parser, set up description and epilog Texts

    my_parser = argparse.ArgumentParser(
        prog="fibr",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
FIBR - CLI
------------------------
Command line interface version of fibr
    Calculates metrics from .tck files.
    Predicts LI from these metrics.
    Generates reports

Requirements:
- make sure you have .tck files for individual bundles.
- make sure you have a reference .nii / .nii.gz file of the subject.
- if you enter multiple bundles, make sure there are as many left as right \
bundles.
- if you use custom models, make sure for each L and R bundle pair there is \
one model available as well

Limitations:
- One command can create the necessary bundle metrics for 1 subject.
    Do not mix up reference .nii files between subjects, this will result in
    false metrics
- To calculate bundles for multiple subjects chain together multiple CLI calls.
    See documentation for more information.
    (https://www.github.com/dopamineral)

Example usage:
<TODO write examples>
                                        """,
        epilog="""\
------------------------
A KUL project.
Laboratory of Translational MRI.

RP, SS, AR
                                            """)

    # Add arguments here
    my_parser.add_argument('ref_nii',
                           metavar='Reference Nii',
                           type=str,
                           help='path to the reference .nii / .nii.gz of the\
                             subject')

    subject_group = my_parser.add_mutually_exclusive_group(
        required=True)

    subject_group.add_argument('-sm', "--subject_manually",
                               action="store_true",  # makes it a boolean flag
                               help="manually input subject metadata (will be \
                                saved to 'subject.json')")

    subject_group.add_argument('-sf', '--subject_file',
                               metavar="file",
                               type=str,
                               help="path to json with subject metadata")

    my_parser.add_argument('-lb', '--left_bundles',
                           metavar='left_tck',
                           type=str,
                           nargs='*',
                           help='path(s) to the left .tck file of the bundles\
                             of interest')

    my_parser.add_argument('-rb', '--right_bundles',
                           metavar='left_tck',
                           type=str,
                           nargs='*',
                           help='path(s) to the right .tck file of the bundles\
                             of interest')

    my_parser.add_argument('-m', '--save_metrics',
                           action="store_true",
                           help='Save intermediate metrics calculations?')

    my_parser.add_argument('-mf', '--metrics_format',
                           choices=["json", "csv"],
                           help='format to save intermediate metrics')

    my_parser.add_argument("-cm", "--custom_model",
                           metavar='model',
                           type=str,
                           nargs='*',
                           help='path(s) to custom model(s) to be used for\
                             prediction')

    my_parser.add_argument('-p', '--predict_laterality',
                           action="store_true",
                           help='Report laterality?')

    my_parser.add_argument("-pf", "--prediction_format",
                           choices=["json", "csv"],
                           help="format to save intermediate predictions")

    my_parser.add_argument('-o', '--save_output',
                           action="store_true",
                           help='Save report of all calculations?')

    my_parser.add_argument('-of', '--output_format',
                           choices=["json", "csv", "pdf", "docx"],
                           nargs="*",
                           help='format(s) to save intermediate metrics')

    my_parser.add_argument("--prefix",
                           metavar="prefix",
                           type=str,
                           help="custom prefix to add to all output files")

    my_parser.add_argument("--suffix",
                           metavar="suffix",
                           type=str,
                           help="custom suffix to add to all output files")

    # Get the arguments
    args = my_parser.parse_args()
