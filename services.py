import json
import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis


def get_stats(data):
    df = pd.read_json(json.dumps(data))
    valid_df = df[((df["HoldTime"] < 3000) & (df["LatencyTime"] < 3000))]
    hold_by_user = valid_df[valid_df["Hand"] != "S"].groupby(
        ["Hand"])["HoldTime"].agg([np.mean, np.std, skew, kurtosis])
    latency_by_user = valid_df[np.in1d(valid_df["Direction"], ["LL", "LR", "RL", "RR"])].groupby(["Direction"])[
        "LatencyTime"].agg([np.mean, np.std, skew, kurtosis])
    hold_by_user_flat = hold_by_user.unstack()
    hold_by_user_flat = hold_by_user_flat.to_frame().T
    hold_by_user_flat.columns = [
        "_".join(col).strip() for col in hold_by_user_flat.columns.values]
    hold_by_user_flat["mean_hold_diff"] = hold_by_user_flat["mean_L"] - \
        hold_by_user_flat["mean_R"]
    latency_by_user_flat = latency_by_user.unstack()
    latency_by_user_flat = latency_by_user_flat.to_frame().T
    latency_by_user_flat.columns = [
        "_".join(col).strip() for col in latency_by_user_flat.columns.values]
    latency_by_user_flat["mean_LR_RL_diff"] = latency_by_user_flat["mean_LR"] - \
        latency_by_user_flat["mean_RL"]
    latency_by_user_flat["mean_LL_RR_diff"] = latency_by_user_flat["mean_LL"] - \
        latency_by_user_flat["mean_RR"]
    combined = pd.concat([hold_by_user_flat, latency_by_user_flat], axis=1)
    stats = json.loads(combined.to_json(orient="records"))[0]

    return stats
