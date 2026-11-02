"""Exact adapter-invariance guards, used only by the bounded engineering probe."""
from __future__ import annotations

import math


def verify_state(actual, expected, *, equal, finite, stage):
    if set(actual) != set(expected) or not actual:
        raise RuntimeError(f"{stage}: empty or mismatched adapter keys")
    elements = 0
    for key, reference in expected.items():
        current = actual[key]
        if current.shape != reference.shape or current.dtype != reference.dtype:
            raise RuntimeError(f"{stage}: adapter shape/dtype changed: {key}")
        if not finite(current) or not finite(reference):
            raise RuntimeError(f"{stage}: nonfinite adapter tensor: {key}")
        if not equal(current, reference):
            raise RuntimeError(f"{stage}: adapter parameter changed: {key}")
        elements += current.numel()
    return {"stage": stage, "tensors": len(actual), "elements": elements,
            "keys_shapes_dtypes_match": True, "all_finite": True, "all_exactly_equal": True}


def adapter_receipt(model, expected, stage):
    import torch
    from peft import get_peft_model_state_dict
    return verify_state(get_peft_model_state_dict(model, adapter_name="default"), expected,
                        equal=torch.equal, finite=lambda x: bool(torch.isfinite(x).all().item()),
                        stage=stage)


def validate_progress(*, global_step, max_steps, learning_rate, weight_decay,
                      group_lrs, optimizer_steps, train_loss):
    if learning_rate != 0.0 or weight_decay != 0.0 or not group_lrs or any(x != 0.0 for x in group_lrs):
        raise RuntimeError("Zero-update check requires zero LR and weight decay")
    if global_step <= 0 or global_step != max_steps or not optimizer_steps or min(optimizer_steps) <= 0:
        raise RuntimeError("Expected complete, nonzero trainer/optimizer steps")
    if not math.isfinite(train_loss):
        raise RuntimeError("Nonfinite training loss")
    return {"global_step": global_step, "max_steps": max_steps,
            "learning_rate": learning_rate, "weight_decay": weight_decay,
            "optimizer_group_lrs": group_lrs, "optimizer_state_entries": len(optimizer_steps),
            "optimizer_step_min": min(optimizer_steps), "optimizer_step_max": max(optimizer_steps),
            "train_loss": train_loss, "training_executed": True}


def finish_receipt(model, expected, trainer, stats, reset_receipt):
    steps = []
    for state in trainer.optimizer.state.values():
        if "step" in state:
            value = state["step"]
            steps.append(int(value.item() if hasattr(value, "item") else value))
    progress = validate_progress(
        global_step=int(trainer.state.global_step), max_steps=int(trainer.state.max_steps),
        learning_rate=float(trainer.args.learning_rate), weight_decay=float(trainer.args.weight_decay),
        group_lrs=[float(g["lr"]) for g in trainer.optimizer.param_groups],
        optimizer_steps=steps, train_loss=float(stats.metrics["train_loss"]),
    )
    return {"status": "PASS", "after_reset": reset_receipt,
            "after_training": adapter_receipt(model, expected, "after_training"),
            "training": progress, "train_dataset_rows": len(trainer.train_dataset),
            "purpose": "Synthetic engineering invariant; not benchmark accuracy", "inference_executed": False}
