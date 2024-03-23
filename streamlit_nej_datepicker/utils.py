import datetime
from typing import Union
import jdatetime

DATE_KEYS = ["maximum_date", "minimum_date"]
CLOSED_VIEW_KEYS = [("button_type", "type")]
IGNORE_KEYS = ["return_type"]


def parse_config(config: dict) -> dict:
    """
    Parse the config dictionary in order to match the props of React component

    Parameters
    ----------
    config: dict
        The configuration dictionary

    Returns
    -------
    dict
        The parsed configuration dictionary
    """
    # remove the keys that are not needed in the React component
    config = {key: value for key, value in config.items() if key not in IGNORE_KEYS}

    # parse all the date related keys to convert them into dict
    locale = config.get("locale", "en")
    for key in DATE_KEYS:
        if key in config:
            config[key] = parse_date_based_on_locale(config[key], locale)
    if "default_value" in config:
        default_value = config["default_value"]
        if isinstance(default_value, (datetime.date, jdatetime.date)):
            config["default_value"] = parse_date_based_on_locale(default_value, locale)
        elif isinstance(default_value, list):
            config["default_value"] = [parse_date_based_on_locale(date, locale) for date in default_value]
        elif isinstance(default_value, dict):
            config["default_value"] = {
                key: parse_date_based_on_locale(value, locale) for key, value in default_value.items()
            }
    if "disabled_days" in config:
        disabled_days = config["disabled_days"]
        config["disabled_days"] = [parse_date_based_on_locale(date, locale) for date in disabled_days]

    # group all the closed view related keys into single key
    config["closed_view_props"] = {}
    for old_key, new_key in CLOSED_VIEW_KEYS:
        if old_key in config:
            config["closed_view_props"][new_key] = config[old_key]
            del config[old_key]

    # change all the keys from snake_case to camelCase
    config = {convert_to_camel_case(key): value for key, value in config.items()}

    return config


def convert_to_camel_case(snake_str: str) -> str:
    """
    Convert the snake_case string to camelCase

    Parameters
    ----------
    snake_str: str
        The snake_case string

    Returns
    -------
    str
        The camelCase string
    """
    first, *others = snake_str.split('_')
    return ''.join([first, *map(str.title, others)])


def parse_date_based_on_locale(date: Union[datetime.date, jdatetime.date], locale: str = "en") -> dict:
    """
    Parse the date based on the locale

    Parameters
    ----------
    date: Union[datetime.date, jdatetime.date]
        The date object
    locale: str
        The locale

    Returns
    -------
    dict
        The parsed date dictionary
    """
    if locale == "en":
        if isinstance(date, datetime.date):
            return dict(
                year=date.year,
                month=date.month,
                day=date.day
            )
        elif isinstance(date, jdatetime.date):
            en_date = date.togregorian()
            return dict(
                year=en_date.year,
                month=en_date.month,
                day=en_date.day
            )
    elif locale == "fa":
        if isinstance(date, datetime.date):
            j_date = jdatetime.date.fromgregorian(date=date)
            return dict(
                year=j_date.year,
                month=j_date.month,
                day=j_date.day
            )
        elif isinstance(date, jdatetime.date):
            return dict(
                year=date.year,
                month=date.month,
                day=date.day
            )
    else:
        raise ValueError("Invalid locale")


def convert_dict_to_date(date: dict, return_type: str) -> datetime.date | jdatetime.date | None:
    """
    Parse the result based on the return_type

    Parameters
    ----------
    date: dict
        The result dictionary from the React component
    return_type: str
        The return type

    Returns
    -------
    Union[datetime.date, jdatetime.date]
        The parsed result
    """
    if date is None:
        return None

    year, month, day = date["year"], date["month"], date["day"]
    date = datetime.date(year=year, month=month, day=day) if return_type == "datetime.date" else jdatetime.date(
        year=year, month=month, day=day)

    return date


def parse_result(
        result: Union[dict, list],
        selection_mode: str,
        return_type: str) -> None | datetime.date | jdatetime.date | list[datetime.date] | list[jdatetime.date] | dict:
    """
    Parse the result based on the selection mode

    Parameters
    ----------
    result: dict
        The result dictionary from the React component
    selection_mode: str
        The selection mode of datepicker that could be single, multiple or range
    return_type: str
        The return type

    Returns
    -------
    Union[datetime.date, jdatetime.date]
        The parsed result
    """
    if result is None:
        return None

    if selection_mode == "single":
        return convert_dict_to_date(date=result, return_type=return_type)
    elif selection_mode == "multiple":
        return [convert_dict_to_date(date=date, return_type=return_type) for date in result]
    elif selection_mode == "range":
        return {key: convert_dict_to_date(date=value, return_type=return_type) for key, value in result.items()}
    else:
        # if selection mode is incorrect, React component deals with it like the single mode
        return convert_dict_to_date(date=result, return_type=return_type)
