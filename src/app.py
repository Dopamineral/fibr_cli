"""Main CLI interface will live here """

import argparse
from pprint import pprint


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
        except Exception as e:
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


def handle_method_input(subject_dict:dict)-> dict:
    """
    Handles manual method input

    adds method iFOD2 or TensorProb to subject dictionary

    Args:
        subject_dict (dict): subject dictionary 

    Returns:
        dict: subject dictionary updated with tractography method
    """    
    while True:
        subject_method = input("Enter tractography metod (iFOD2 - 'I' / TensorProb - 'T'): ")
        if subject_method.lower() in ["i", "ifod", "ifod2"]:
            subject_dict["subject_method"] = "iFOD2"
            break

        if subject_method.lower() in ["t", "tensorprob", "tp", "tensor"]:
            subject_dict["subject_method"] = "TensorProb"
            break

        else:
            print("please input valid sex : 'I or 'T'")
            
    return subject_dict


def handle_clean_input(subject_dict:dict)-> dict:
    """
    handles manual input if clean or not.

    Adds boolena to subject dictionary depending on clean state

    Args:
        subject_dict (dict): subject dictionary

    Returns:
        dict: subject dictionary updated with boolean for cleaned data
    """    
    while True:
        subject_clean = input("Was the bundle cleaned or filtered? (Y/N)")
        if subject_clean.lower() in ["y","yes","yep"]:
            subject_dict["subject_clean"] = True
            break

        if subject_clean.lower() in ["no", "n", "nope"]:
            subject_dict["subject_clean"] = False
            break

        else:
            print("I don't understand, Y or N ?")
        
    return subject_dict


def handle_act_input(subject_dict:dict)-> dict:
    """
    handles manual act input (Y or N)

    adds boolean to subject dictionary based on user input for ACT

    Args:
        subject_dict (dict): subject dictionary

    Returns:
        dict: subject dictionary updated with boolean for ACT
    """    
    while True:
        subject_act = input("ACT? Was the data anatomically constrained? (Y/N)")
        if subject_act.lower() in ["y","yes","yep"]:
            subject_dict["subject_act"] = True
            break

        if subject_act.lower() in ["no", "n", "nope"]:
            subject_dict["subject_act"] = False
            break

        else:
            print("I don't understand, Y or N ?")
        
    return subject_dict


def handle_tract_input(subject_dict:dict)-> dict:
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
    # print(args)

    # Input patient meta manually
    if args.subject_manually:
        subject_dict = {}
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
        subject_dict = handle_age_input(subject_dict)
        subject_dict = handle_sex_input(subject_dict)
        subject_dict = handle_handedness_input(subject_dict)
        subject_dict = handle_method_input(subject_dict)
        subject_dict = handle_clean_input(subject_dict)
        subject_dict = handle_act_input(subject_dict)
        subject_dict = handle_tract_input(subject_dict)

        pprint(subject_dict)
