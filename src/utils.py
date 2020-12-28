# Copyright 2020 The `Kumar Nityan Suman` (https://github.com/nityansuman/). All Rights Reserved.
#
#
#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
# ==============================================================================


# Import packages
import os
import csv
import numpy as np
import pandas as pd


def backup(session):
    # Process username and subject information
    username = "_".join([x.upper() for x in session["username"].split()])
    subject_name = session["subject_name"].strip().upper()
    subject_id = session["subject_id"].strip()
    test_type = ["Objective" if session["test_id"] == "0" else "Subjective"][0]
    test_id = session["test_id"]
    # Process timestamp
    timestamp = session["date"]
    # Construct loggin data
    row = [
        timestamp,
        username,
        subject_name,
        subject_id,
        test_type,
        test_id,
        session["score"],
        session["result"]
    ]
    # Database user information log path
    filepath = session["database_path"]
    file_exists = os.path.isfile(filepath)
    if file_exists:
        # If file exists, open file in append mode
        try:
            with open(filepath, mode="a") as fp:
                fp_writer = csv.writer(fp)
                # Backup data
                fp_writer.writerow(row)
                status = True
        except Exception as e:
            print("Exception raised at `utils.__backup`:", e)
    else:
        print("Database placeholder nott found!")
        status = False
    return status


def relative_ranking(session):
    """Method to compute relative ranking of user on a particular subject.
    
    Arguments:
        subjectname {str} -- Name of the test subject.
        type {str} -- Denoting the type of the test taken
    
    Returns:
        int, float, int -- Maximum, Minimum and Average score obtained by the user in a paarticular subject test
    """
    max_score = 100.0
    min_score = 0.0
    mean_score = "None"
    try:
        df = pd.read_csv(session["database_path"])
    except Exception as e:
        print("Exception raised at `utils__relative_ranking`:", e)
    else:
        df = df[(df["SUBJECT_ID"] == int(session["subject_id"])) & (df["TEST_ID"] == int(session["test_id"]))]
        if df.shape[0] >= 1:
            max_score = np.round(df["SCORE"].max(), decimals=2)
            min_score = np.round(df["SCORE"].min(), decimals=2)
            mean_score = np.round(df["SCORE"].mean(), decimals=2)
    finally:
        return max_score, min_score, mean_score