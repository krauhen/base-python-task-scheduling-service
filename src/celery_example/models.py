from typing import List, Union, Any
from pydantic import BaseModel


class TrainModel(BaseModel):
    X: List[List[Any]] = None
    y: List[List[Any]] = None
    X_ref: Union[None, str] = None
    y_ref: Union[None, str] = None


class PredictModel(BaseModel):
    model_ref: str
    X: List[List[Any]] = None
    X_ref: Union[None, str] = None
