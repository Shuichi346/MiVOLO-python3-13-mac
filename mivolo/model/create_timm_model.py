"""
Code adapted from timm https://github.com/huggingface/pytorch-image-models

Modifications and additions for mivolo by / Copyright 2023, Irina Tolstykh, Maxim Kuprashevich
"""

import argparse
import os
import pickle
from typing import Any, Dict, Optional, Union

import timm
import torch

# register new models
from mivolo.model.mivolo_model import *  # noqa: F403, F401
from timm.models import PretrainedCfg, clean_state_dict, remap_state_dict


def load_checkpoint_data(checkpoint_path: str) -> Dict[str, Any]:
    """Load a legacy checkpoint without an automatic unsafe pickle fallback."""

    safe_globals = [argparse.Namespace]
    try:
        with torch.serialization.safe_globals(safe_globals):
            checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    except pickle.UnpicklingError as error:
        unsafe_globals = []
        if hasattr(torch.serialization, "get_unsafe_globals_in_checkpoint"):
            unsafe_globals = torch.serialization.get_unsafe_globals_in_checkpoint(checkpoint_path)
        detail = f" Unsupported globals: {', '.join(unsafe_globals)}." if unsafe_globals else ""
        raise RuntimeError(
            "Restricted loading rejected this checkpoint because it contains executable pickle data."
            f"{detail} Use a documented MiVOLO checkpoint or review and convert the trusted file."
        ) from error

    if not isinstance(checkpoint, dict):
        raise ValueError(f"Checkpoint must contain a dictionary: {checkpoint_path}")
    return checkpoint


def _state_dict_from_checkpoint(checkpoint: Dict[str, Any], use_ema: bool = True) -> Dict[str, Any]:
    state_dict = checkpoint
    if use_ema and checkpoint.get("state_dict_ema") is not None:
        state_dict = checkpoint["state_dict_ema"]
    elif use_ema and checkpoint.get("model_ema") is not None:
        state_dict = checkpoint["model_ema"]
    elif checkpoint.get("state_dict") is not None:
        state_dict = checkpoint["state_dict"]
    elif checkpoint.get("model") is not None:
        state_dict = checkpoint["model"]

    if not isinstance(state_dict, dict):
        raise ValueError("Checkpoint does not contain a valid model state dictionary.")
    return clean_state_dict(state_dict)


def load_checkpoint(
    model, checkpoint_path, use_ema=True, strict=True, remap=False, filter_keys=None, state_dict_map=None
):
    if os.path.splitext(checkpoint_path)[-1].lower() in (".npz", ".npy"):
        # numpy checkpoint, try to load via model specific load_pretrained fn
        if hasattr(model, "load_pretrained"):
            model.load_pretrained(checkpoint_path)
        else:
            raise NotImplementedError("Model cannot load numpy checkpoint")
        return
    state_dict = _state_dict_from_checkpoint(load_checkpoint_data(checkpoint_path), use_ema)
    if remap:
        state_dict = remap_state_dict(state_dict, model)
    if filter_keys:
        for sd_key in list(state_dict.keys()):
            for filter_key in filter_keys:
                if filter_key in sd_key:
                    if sd_key in state_dict:
                        del state_dict[sd_key]

    rep = []
    if state_dict_map is not None:
        # 'patch_embed.conv1.' : 'patch_embed.conv.'
        for state_k in list(state_dict.keys()):
            for target_k, target_v in state_dict_map.items():
                if target_v in state_k:
                    target_name = state_k.replace(target_v, target_k)
                    state_dict[target_name] = state_dict[state_k]
                    rep.append(state_k)
        for r in rep:
            if r in state_dict:
                del state_dict[r]

    incompatible_keys = model.load_state_dict(state_dict, strict=strict if filter_keys is None else False)
    return incompatible_keys


def create_model(
    model_name: str,
    pretrained: bool = False,
    pretrained_cfg: Optional[Union[str, Dict[str, Any], PretrainedCfg]] = None,
    pretrained_cfg_overlay: Optional[Dict[str, Any]] = None,
    checkpoint_path: str = "",
    scriptable: Optional[bool] = None,
    exportable: Optional[bool] = None,
    no_jit: Optional[bool] = None,
    filter_keys=None,
    state_dict_map=None,
    **kwargs,
):
    """Create a model
    Lookup model's entrypoint function and pass relevant args to create a new model.
    """
    # Parameters that aren't supported by all models or are intended to only override model defaults if set
    # should default to None in command line args/cfg. Remove them if they are present and not set so that
    # non-supporting models don't break and default args remain in effect.
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    model = timm.create_model(
        model_name,
        pretrained=pretrained,
        pretrained_cfg=pretrained_cfg,
        pretrained_cfg_overlay=pretrained_cfg_overlay,
        scriptable=scriptable,
        exportable=exportable,
        no_jit=no_jit,
        **kwargs,
    )

    if checkpoint_path:
        load_checkpoint(model, checkpoint_path, filter_keys=filter_keys, state_dict_map=state_dict_map)

    return model
