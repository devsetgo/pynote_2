# -*- coding: utf-8 -*-

import logging

import safe
from loguru import logger
from passlib.hash import bcrypt

import settings

# https://pypi.org/project/Safe/

def encrypt_pass(pwd: str) -> str:
    hashed_pwd = bcrypt.using(rounds=13).hash(pwd)
    return hashed_pwd


def verify_pass(pwd: str, crypt_pwd: str) -> bool:
    """[summary]
    Verify password vs hashed password

    Arguments:
        pwd {str} -- [password]
        crypt_pwd {str} -- [hashed password]

    Returns:
        bool -- [password is valid]
    """
    result: bool = bcrypt.verify(pwd, crypt_pwd)
    return result


def char_check(pwd: str):
    """
    [summary]
    Check to see if list of invalid chacacters is present within pwd string

    Arguments:
        pwd {str} -- [password string]

    Returns:
        [bool] -- [if no illega characters present, return True]
    """
    # list of invalid characters
    invalid_characters: list = settings.INVALID_CHARACTER_LIST
    # print(invalid_characters)
    logging.debug(invalid_characters)
    # check if an illegal character is in password
    for c in pwd:
        if c in invalid_characters:
            # if illegal chacter set as result as false
            result: bool = False
            logger.info("illegall character found in password")
            logging.debug(f"illegal character found {c}")
            return result

    result: bool = True
    return result


def check_strength(pwd: str):
    """[summary]
    Check if passwor contains a proper strength and if the characters are valid
    Arguments:
        pwd {str} -- [Password]

    Returns:
        [Dict] -- [Password Strength: Bool, validity of character: Bool]
    """
    strength: str = safe.check(raw=pwd, length=8, freq=0, min_types=3, level=3)
    result: bool = strength.valid
    logger.info(f"result = {result}")
    return result
