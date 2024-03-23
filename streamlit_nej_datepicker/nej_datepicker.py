import os
import streamlit.components.v1 as components
from .utils import parse_config, parse_result
from pydantic import BaseModel, ConfigDict, model_validator
from typing import List, Union, Dict
import datetime
import jdatetime

_RELEASE = True

if _RELEASE:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend", "dist")

    _component = components.declare_component(
        name="nej_datepicker",
        path=build_dir
    )
else:
    _component = components.declare_component(
        name="nej_datepicker",
        url="http://localhost:5173"
    )


class Config(BaseModel):
    """
    The configuration of the date picker
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    always_open: bool = False
    arrow: bool = True
    button_type: str = 'default'
    closed_view: str = 'text'
    color_primary: str = '#1677ff'
    color_primary_light: str = '#64a9f9'
    dark_mode: bool = False
    default_value: Union[datetime.date, jdatetime.date, List[Union[datetime.date, jdatetime.date]], Dict[
        str, Union[datetime.date, jdatetime.date]]] = None
    delimiter: str = '-'
    disabled: bool = False
    disabled_days: List[Union[datetime.date, jdatetime.date]] = []
    locale: str = 'en'
    maximum_date: Union[datetime.date, jdatetime.date] = None
    maximum_today: bool = False
    maximum_tomorrow: bool = False
    minimum_date: Union[datetime.date, jdatetime.date] = None
    minimum_today: bool = False
    minimum_tomorrow: bool = False
    placeholder: str = 'select'
    placement: str = 'bottom'
    return_type: str = 'datetime.date'
    selection_mode: str = 'single'
    selector_ending_year: int = None
    selector_starting_year: int = None
    should_highlight_weekends: bool = False
    slide_animation_duration: str = '0.4s'
    trigger: str = 'click'

    @model_validator(mode='before')
    def validate_default_value(cls, data: dict):
        locale = data.get("locale", "en")
        keys = data.keys()
        if "placeholder" not in keys:
            data["placeholder"] = 'select' if locale == 'en' else 'انتخاب'
        if "return_type" not in keys:
            data["return_type"] = 'datetime.date' if locale == 'en' else 'jdatetime.date'

        return data


class NejDatepicker:
    def __call__(self, *args, config: Config, **kwargs):
        return_type = config.return_type
        selection_mode = config.selection_mode
        config = parse_config(config.dict())
        return parse_result(result=_component(config=config, args=args, **kwargs), return_type=return_type,
                            selection_mode=selection_mode)


datepicker_component = NejDatepicker()
