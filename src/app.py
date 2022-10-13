"""Main CLI interface will live here """

import argparse
from pprint import pprint
import json
import nibabel as nib
import nibabel.streamlines as nibs
from metrics import streamline2volume
from metrics import calculate_metrics
import pandas as pd

def nii_validation(arg: str):

    # not perfect but good enough. for example a gz.nii file will be accepted if
    # someone decides to use that as an input.
    splits = arg.split(".")
    if splits[-1].lower() == "gz":
        if splits[-2].lower() == "nii":
            return True
        else:
            print(
                f"Format of file not recognized:'{arg}' make sure it's a .nii or .nii.gz")
            return False
    if splits[-1].lower() == "nii":
        return True

    else:
        print(
            f"Format of file not recognized: '{arg}' make sure it's a .nii or .nii.gz")
        return False


def tck_validation(args_list: list) -> bool:
    for arg in args_list:
        if arg.split(".")[-1].lower() in ["tck"]:
            continue
        else:
            print(
                f"File not recognized: '{arg}', make sure it's in .tck format")
            return False
    return True


def json_validation(args_list: list) -> bool:
    for arg in args_list:
        if arg.split(".")[-1].lower() in ["json"]:
            continue
        else:
            print(
                f"File not recognized: '{arg}', make sure it's in .json format")
            return False
    return True


def exit_on_uneven_left_right(left_bundles, right_bundles):
    if len(left_bundles) != len(right_bundles):
        print("Please provide the same amount of left \
bundles and right bundles for this step")
        exit()


def handle_age_input(subject_dict: dict) -> dict:
    """Handles manual input for age

    Checks for valid inputs and appends age in int format to the subject_dict
    under the "subject_age" key.

    Args:
        subject_dict (dict): dictionary in which to store subject data

    Returns:
        dict: subject dictionary updated with subject_age
    """

    # input and handle subject age
    while True:  # Age input look - breaks if int
        subject_age = input("Enter Subject Age: ")
        try:
            subject_age_int = int(subject_age)
            if subject_age_int < 0:
                print("! Not valid, please input a positive number and try again")
                subject_age_int = int(input("Enter Subject Age: "))

            if subject_age_int > 150:
                print("! Not valid, please enter subject age in years and try\
again. e.g: 'fourty-five years old' -> input '45'")
                subject_age_int = int(input("Enter Subject Age: "))
            else:
                break
        except Exception:
            print("! Not valid, please input a number as age and try again")
            # exit()

    # add everythign to the subject_age dictionary
    subject_dict["subject_age"] = subject_age_int

    return subject_dict


def handle_sex_input(subject_dict: dict) -> dict:
    """
    Handles sex input

    F or M accepted, but also some other variants. Adds to subject dict

    Args:
        subject_dict (dict): dictionary subject data

    Returns:
        dict: dictionary updated with subject sex
    """
    while True:
        subject_sex = input("Enter subject sex (M/F): ")
        if subject_sex in ["M", "m", "male"]:
            subject_dict["subject_sex"] = "M"
            break

        if subject_sex in ["F", "f", "female"]:
            subject_dict["subject_sex"] = "F"
            break

        else:
            print("please input valid sex : 'F or 'M'")

    return subject_dict


def handle_handedness_input(subject_dict: dict) -> dict:
    """
    handles handedness input - L or R

    adds handedness information to subject dict

    Args:
        subject_dict (dict): subject dictionary

    Returns:
        dict: subject dictionary updated with handedness
    """
    while True:
        subject_handedness = input("Enter subject sex (L/R/A): ")
        if subject_handedness in ["L", "l", "left"]:
            subject_dict["subject_handedness"] = "L"
            break

        if subject_handedness in ["R", "r", "right"]:
            subject_dict["subject_handedness"] = "R"
            break

        if subject_handedness in ["A", "a", "ambi"]:
            subject_dict["subject_handedness"] = "A"
            break
        else:
            print("please input valid sex : 'R, L, or 'A'")

    return subject_dict


def handle_method_input(subject_dict: dict) -> dict:
    """
    Handles manual method input

    adds method iFOD2 or TensorProb to subject dictionary

    Args:
        subject_dict (dict): subject dictionary

    Returns:
        dict: subject dictionary updated with tractography method
    """
    while True:
        subject_method = input(
            "Enter tractography metod (iFOD2 - 'I' / TensorProb - 'T'): ")
        if subject_method.lower() in ["i", "ifod", "ifod2"]:
            subject_dict["subject_method"] = "iFOD2"
            break

        if subject_method.lower() in ["t", "tensorprob", "tp", "tensor"]:
            subject_dict["subject_method"] = "TensorProb"
            break

        else:
            print("please input valid sex : 'I or 'T'")

    return subject_dict


def handle_clean_input(subject_dict: dict) -> dict:
    """
    handles manual input if clean or not.

    Adds boolena to subject dictionary depending on clean state

    Args:
        subject_dict (dict): subject dictionary

    Returns:
        dict: subject dictionary updated with bool for cleaned data
    """
    while True:
        subject_clean = input("Was the bundle cleaned or filtered? (Y/N)")
        if subject_clean.lower() in ["y", "yes", "yep"]:
            subject_dict["subject_clean"] = True
            break

        if subject_clean.lower() in ["no", "n", "nope"]:
            subject_dict["subject_clean"] = False
            break

        else:
            print("I don't understand, Y or N ?")

    return subject_dict


def handle_act_input(subject_dict: dict) -> dict:
    """
    handles manual act input (Y or N)

    adds bool to subject dictionary based on user input for ACT

    Args:
        subject_dict (dict): subject dictionary

    Returns:
        dict: subject dictionary updated with bool for ACT
    """
    while True:
        subject_act = input(
            "ACT? Was the data anatomically constrained? (Y/N)")
        if subject_act.lower() in ["y", "yes", "yep"]:
            subject_dict["subject_act"] = True
            break

        if subject_act.lower() in ["no", "n", "nope"]:
            subject_dict["subject_act"] = False
            break

        else:
            print("I don't understand, Y or N ?")

    return subject_dict


def handle_tract_input(subject_dict: dict) -> dict:
    """
    Updates subject dictionary with tract information.

    Future: will be updated to work with multiple tracts but currently
    only updates the subject dictionary with AF_wprecentral for now.

    Args:
        subject_dict (dict): subject dicitonary

    Returns:
        dict: subject dictionary updated for tract info
    """
    print("currently tract defaults to AF_wprecentral")
    subject_dict["subject_tract"] = "AF_wprecentral"
    return subject_dict


def handle_subject_file(my_args: argparse.Namespace, task_data) -> dict:

    # get global TASK_DATA dict

    json_file = False
    csv_file = False

    # Check if the input file is json or csv
    subject_file_path = my_args.subject_file
    if subject_file_path.split(".")[-1].lower() == "json":
        print(f"loading subject data from : {subject_file_path}")
        json_file = True

    elif subject_file_path.split(".")[-1].lower() == "csv":
        print(f"loading subject data from : {subject_file_path}")
        csv_file = True
    else:
        print(
            f"unrecognized format for : '{subject_file_path}' -> make sure \
                it's json or csv")

    # Load the json file
    if json_file:
        with open(subject_file_path, "r") as read_file:
            subject_data = json.load(read_file)

    if csv_file:
        # TODO: implement reading from CSV file.
        print("CSV not implemented yet, please use JSON format")
        return 0

    # Add subject_data tot task_data
    task_data["subject_data"] = subject_data
    return task_data


def calculate_metrics_one_bundle(ref_path: str, tck_path: str) -> dict:
    # if the files don't load, give feedback to usser
    try:
        reference_nii = nib.load(ref_path)
    except Exception:
        print(f"Something went wrong trying to load: {ref_path}")
        return {"error": "reference nii"}
    try:
        tck_file = nibs.load(tck_path)
    except Exception:
        print(f"Something went wrong trying to load: {tck_path}")
        return {"error": "tck file"}

    vol = streamline2volume(tck_file, reference_nii)
    metrics = calculate_metrics(tck_file, vol)
    return metrics


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
                               action="store_true",  # makes it a bool flag
                               help="manually input subject metadata, will be \
                                in json format by default")

    my_parser.add_argument('-ssf', '--subject_save_file',
                           metavar="file",
                           type=str,
                           help="filename to save json with subject metadata \
                            (defaults to subject_data.json)")

    subject_group.add_argument('-sf', '--subject_file',
                               metavar="file",
                               type=str,
                               help="path to json with subject if you you \
                                already have a metadata file. For more info\
                                on the format of the metadata files see the \
                                    documentation")

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

    my_parser.add_argument('-eb', '--extra_bundle_info',
                           metavar='extra info file',
                           type=str,
                           nargs='*',
                           help='path(s) to json files with additional \
                            bundle info if needed for processing. Info in here\
                            will overwrite the values that were given in the \
                                subject info provided earlier')

    my_parser.add_argument('-m', '--save_metrics',
                           action="store_true",
                           help='Save intermediate metrics calculations? \
                            (default format=json)')

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

    # Make one big master task dictionary with all the instructions to feed into
    # the calculations / predictions and reports
    TASK_DATA = {}

    # --prefix / --suffix  if there are user defined suffixes.
    PREFIX = ""
    SUFFIX = ""
    if args.prefix:
        PREFIX = args.prefix + "_"
    if args.suffix:
        SUFFIX = "_" + args.suffix

    # ref_nii, check if format is correct
    print(args.ref_nii)
    if not nii_validation(args.ref_nii):
        exit()
    else:
        ref_nii = args.ref_nii

    # --subject_manually / -sm
    if args.subject_manually:
        subject_data = {}
        # initual user feedback
        print("You've chosen to input the subject data manually, please\
continue:\n ----")
        # age
        # sex
        # handedness
        # method - iFOD / Tprob
        # clean
        # AcT
        # (tract - future input, now AF_wprecentral for all)

        # TODO: Refactor with function composition.
        subject_data = handle_age_input(subject_data)
        subject_data = handle_sex_input(subject_data)
        subject_data = handle_handedness_input(subject_data)
        subject_data = handle_method_input(subject_data)
        subject_data = handle_clean_input(subject_data)
        subject_data = handle_act_input(subject_data)
        subject_data = handle_tract_input(subject_data)

        # Save subject metrics after manual entry
        subject_metrics_filename = "subject_metrics"  # default name for save

        # --subject_save_file / -ssf
        if args.subject_save_file:  # user defined name
            # filtering out a .json ending if user defined this
            subject_metrics_filename = args.subject_save_file.split(".json")[0]

        print(f"saving subject metrics to: {subject_metrics_filename}.json")
        with open(f"{PREFIX}{subject_metrics_filename}{SUFFIX}.json",
                  "w",
                  encoding="utf-8") as write_file:
            json.dump(subject_data, write_file, indent=4)

        TASK_DATA["subject_data"] = subject_data

    # --subject_file  / -sf
    if args.subject_file:
        TASK_DATA = handle_subject_file(args, TASK_DATA)

    # --left_bundles / -lb
    if args.left_bundles:
        if not tck_validation(args.left_bundles):
            exit()
        else:
            TASK_DATA["left_bundles"] = args.left_bundles

    # --right_bundles / -rb
    if args.right_bundles:
        if not tck_validation(args.right_bundles):
            exit()
        else:
            TASK_DATA["right_bundles"] = args.right_bundles

    # --extra_bundle_info / -eb
    if args.extra_bundle_info:
        if not json_validation(args.extra_bundle_info):
            exit()
        else:
            TASK_DATA["extra_bundle_info_files"] = args.extra_bundle_info

        # load extra bundle info and add to master dict
        extra_bundle_list = []
        extra_bundle_labels = []
        for index, extra_info_file in enumerate(
                TASK_DATA["extra_bundle_info_files"]):

            with open(extra_info_file, "r", encoding="utf-8") as read_file:
                extra_info = json.load(read_file)

            extra_bundle_labels.append({index: extra_info_file})
            extra_bundle_list.append({index: extra_info})

        TASK_DATA["extra_bundle_info_files"] = extra_bundle_labels
        TASK_DATA["extra_bundle_info"] = extra_bundle_list

    # Calculate the bundle information
    print("Calculating metrics for all bundles...")
    left_bundle_metrics = []
    left_bundle_labels = []
    for index, bundle in enumerate(TASK_DATA["left_bundles"]):
        metrics = calculate_metrics_one_bundle(ref_nii, bundle)
        bundle_dict = {index: metrics}
        label = {index: bundle}
        left_bundle_metrics.append(bundle_dict)
        left_bundle_labels.append(label)

    right_bundle_metrics = []
    right_bundle_labels = []
    for index, bundle in enumerate(TASK_DATA["right_bundles"]):
        metrics = calculate_metrics_one_bundle(ref_nii, bundle)
        bundle_dict = {index: metrics}
        label = {index: bundle}
        right_bundle_metrics.append(bundle_dict)
        right_bundle_labels.append(label)

    # adding metrics to master dict, one index per bundle per side
    TASK_DATA["metrics_left"] = left_bundle_metrics
    TASK_DATA["metrics_right"] = right_bundle_metrics

    # updating te filenames with indices so it matches the metric indices
    TASK_DATA["left_bundles"] = left_bundle_labels
    TASK_DATA["right_bundles"] = right_bundle_labels

    # pprint(TASK_DATA)

    # --save_metrics / -m
    json_format_metrics = True
    csv_format_metrics = False
    if args.metrics_format:
        if args.metrics_format == "csv":
            csv_format_metrics = True

    if args.save_metrics:
        if json_format_metrics:
            with open(f"{PREFIX}bundle_metrics{SUFFIX}.json",
                      "w",
                      encoding="utf-8") as metrics_file:
                json.dump(TASK_DATA, metrics_file, indent=4)

        if csv_format_metrics:
            #TODO: Unpack the nested json data into (multiple?) \
            # csv files as output
            print("Saving metrics to CSV not implemented yet. Continuing")

    