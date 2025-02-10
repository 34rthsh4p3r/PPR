# Parameter Generation Trends

This document describes the trends used for generating parameter values in a simulation. These trends control how values change over depth or time within different zones and environments. It also explains how to tune and refine these trends, and includes the relevant code snippets.

## Trend Descriptions and Tuning

The following trends are available, along with instructions on how to tune their parameters within the `generate_value` function:

*   **`SP` (Sporadic):** 70% chance of the value being 0. 30% chance of a random value between the minimum and maximum.

    *   `probability_of_zero`: Change the `0.7` in the code to adjust the probability of the value being zero.
    *   `min_val`, `max_val`: These define the range for the random values.

    ```python
    elif trend == "SP":  # Sporadic: 70% chance to be 0
        if random.random() < 0.7:
            return round(0, 2)
        else:
            return round(random.uniform(min_val, max_val), 2)
    ```

*   **`UP` (Up):** Values increase gradually over time (or depth). Each new value is randomly selected between the *previous* value and a limit calculated as a fraction of the way toward the maximum. The increase is capped at 30% of the remaining range to the maximum, for a gradual increase.

    *   `increase_limit`: Modify the `0.3` in the code to change the maximum percentage increase per step.  Lower values create slower increases.
    *   `min_val`, `max_val`: These set the absolute bounds.
    *   `param.last_val_up`: Is the dynamically changing lower bound.

    ```python
    elif trend == "UP":  # Up: Increasing values
        if not hasattr(param, 'last_val_up'):
            param.last_val_up = min_val  # Initialize at min_val
        new_val = random.uniform(param.last_val_up, param.last_val_up + (max_val - param.last_val_up) * 0.3) # Limit increase per step
        param.last_val_up = new_val
        return round(new_val, 2)
    ```

*   **`DN` (Down):** Values decrease gradually. Each new value is between a fraction of the distance down to the minimum and the *previous* value. The decrease is capped at 30% of the remaining range to the minimum, for a gradual decrease.

    *   `decrease_limit`: Similar to `UP`, modify the `0.3` to control the maximum percentage *decrease* per step.
    *   `min_val`, `max_val`: Set the absolute bounds.
    *   `param.last_val_dn`: Is the dynamically changing upper bound.

    ```python
    elif trend == "DN":  # Down: Decreasing values
        if not hasattr(param, 'last_val_dn'):
            param.last_val_dn = max_val # Initialize at max_val
        new_val = random.uniform(param.last_val_dn - (param.last_val_dn - min_val) * 0.3, param.last_val_dn)  # Limit decrease per step
        param.last_val_dn = new_val
        return round(new_val, 2)
    ```

*   **`LF` (LowFluctuation):** Values fluctuate around a slowly drifting center point. The fluctuation is small (5% of the total range). The center itself also moves randomly by a small amount on each step, preventing the trend from getting "stuck."

    *   `fluctuation_percentage`: Change the `0.05` in the code to adjust the fluctuation range (as a percentage of the total range).
    *   `drift_amount`: Modify the range in the code to control how much the center point can drift per step.
    *   `min_val`, `max_val`: Set the absolute bounds.
    *   `param.lf_center`: Is the dynamically changing center of the fluctuation.

    ```python
    elif trend == "LF":  # LowFluctuation
        if not hasattr(param, 'lf_center'):
            param.lf_center = (min_val + max_val) / 2  # or some other initial value
        fluctuation = (max_val - min_val) * 0.05  # Reduced fluctuation to 5%
        new_val = random.uniform(param.lf_center - fluctuation, param.lf_center + fluctuation)
        param.lf_center = new_val + random.uniform(-fluctuation/2, fluctuation/2)  # Add small random drift to the center
        param.lf_center = max(min_val, min(param.lf_center, max_val)) # Keep center within bounds
        return round(new_val, 2)
    ```

*   **`HF` (HighFluctuation):** Values fluctuate significantly (40% of the total range) around the midpoint of the minimum and maximum.

    *   `fluctuation_percentage`: Change the `0.4` in the code to control the fluctuation range.
    *   `min_val`, `max_val`: Set the absolute bounds.

    ```python
    elif trend == "HF":  # HighFluctuation
        fluctuation = (max_val - min_val) * 0.4  # 40% fluctuation
        center = (min_val + max_val) / 2
        new_val =  round(random.uniform(center - fluctuation, center + fluctuation), 2)
        return max(min_val, min(new_val, max_val)) #Limit the value
    ```

*   **`SL` (StagnantLow):** *First*, the values are stagnant and fluctuate around a *randomly chosen point* between `min_val * 1.2` and `max_val * 0.8` (with a small 5% fluctuation). *Then*, after a midpoint (40-60% of the depth), the values begin to *decrease* gradually towards the minimum.

    *   `midpoint_ratio`: The range `0.4, 0.6` in the code determines the range for the midpoint (as a percentage of `depth`).
    *   `stagnant_fluctuation`: Change the `0.05` in `fluctuation = (max_val - min_val) * 0.05` to control the fluctuation during the stagnant phase.
    *   `decrease_rate`: Modify the `0.5` in the code to adjust how quickly the value decreases after the midpoint.
    *   `min_val`, `max_val`: Set the absolute bounds.
    *   `param.stagnant_center_sl`: Stores the randomly chosen center point for the stagnant phase.  This is initialized *once*.
    *   `param.last_val_sl`: Stores the last value of the previous step, used in the decreasing phase.

    ```python
    elif trend == "SL": #StagnantLow: first stagnant, then decreasing
        midpoint_ratio = random.uniform(0.4, 0.6)
        midpoint = depth * midpoint_ratio
        if d <= midpoint:
            if not hasattr(param, 'stagnant_center_sl'):
                param.stagnant_center_sl = random.uniform(min_val * 1.2, max_val * 0.8)
            fluctuation = (max_val - min_val) * 0.05  # 5% fluctuation
            return round(random.uniform(max(min_val, param.stagnant_center_sl - fluctuation), min(max_val, param.stagnant_center_sl + fluctuation)), 2)

        else:
            if not hasattr(param, 'last_val_sl'):
                param.last_val_sl = param.stagnant_center_sl #initialize with the stagnant value
            normalized_depth = (d - midpoint) / (depth - midpoint) if (depth - midpoint) > 0 else 0
            new_val = round(float(param.last_val_sl - (param.last_val_sl-min_val) * normalized_depth * 0.5 ),2) #slower decreasing
            param.last_val_sl = new_val
            return max(min_val, min(new_val, max_val)) #Limit the value
    ```

*   **`SH` (StagnantHigh):** *First*, the values are stagnant and fluctuate around a *randomly chosen point* between `min_val * 1.2` and `max_val * 0.8` (with a small 5% fluctuation). *Then*, after a midpoint (40-60% of the depth), the values begin to *increase* gradually towards the maximum.

    *   `midpoint_ratio`: Same as in `SL`, controls the midpoint.
    *   `stagnant_fluctuation`: Change the `0.05` in `fluctuation = (max_val - min_val) * 0.05` to control the fluctuation during the stagnant phase.
    *   `increase_rate`: Similar to `SL`, but controls the *increase* rate after the midpoint, using the `0.5` factor.
    *   `min_val`, `max_val`: Set the absolute bounds.
    *   `param.stagnant_center_sh`: Stores the randomly chosen center point for the stagnant phase. This is initialized *once*.
    *   `param.last_val_sh`: Stores the last value of the previous step.

    ```python
    elif trend == "SH": #StagnantHigh: first stagnant, then increasing
        midpoint_ratio = random.uniform(0.4, 0.6)
        midpoint = depth * midpoint_ratio
        if d <= midpoint:
            if not hasattr(param, 'stagnant_center_sh'):
                param.stagnant_center_sh = random.uniform(min_val * 1.2, max_val * 0.8)
            fluctuation = (max_val - min_val) * 0.05
            return round(random.uniform(max(min_val, param.stagnant_center_sh - fluctuation), min(max_val, param.stagnant_center_sh + fluctuation)), 2)
        else:
            if not hasattr(param, 'last_val_sh'):
                param.last_val_sh = param.stagnant_center_sh #initialize with the stagnant value
            normalized_depth = (d - midpoint) / (depth - midpoint) if (depth - midpoint) > 0 else 0

            new_val = round(float(param.last_val_sh + (max_val - param.last_val_sh) * normalized_depth * 0.5),2) #Slower increasing
            param.last_val_sh = new_val
            return max(min_val, min(new_val, max_val))  #Limit the value
    ```

*   **`UD` (UpDown):** Values *increase* linearly from the minimum to the maximum until a randomly determined midpoint (40-60% of the zone's depth). After the midpoint, values *decrease* linearly from the maximum back to the minimum.

    *   `midpoint_ratio`: The range `0.4, 0.6` in the code controls the midpoint (as a percentage of the zone's depth).
    *   `min_val`, `max_val`: Set the absolute bounds.

    ```python
    elif trend == "UD":  # UpDown
        midpoint_ratio = random.uniform(0.4, 0.6)
        midpoint = zones[zone_num][0] + (zones[zone_num][1] - zones[zone_num][0]) * midpoint_ratio

        if d <= midpoint:
            # Increasing part
            normalized_zone_depth = (d - zones[zone_num][0]) / (midpoint - zones[zone_num][0]) if (midpoint - zones[zone_num][0]) > 0 else 0
            return round(float(min_val + (max_val - min_val) * normalized_zone_depth), 2)
        else:
            # Decreasing part
            normalized_zone_depth = (d - midpoint) / (zones[zone_num][1] - midpoint) if (zones[zone_num][1] - midpoint) > 0 else 0
            return round(float(max_val - (max_val - min_val) * normalized_zone_depth), 2)
    ```

*   **`DU` (DownUp):** Values *decrease* linearly from the maximum to the minimum until a randomly determined midpoint (40-60% of the zone's depth). After the midpoint, values *increase* linearly from the minimum back to the maximum.

    *   `midpoint_ratio`: Same as in `UD`.
    *   `min_val`, `max_val`: Set the absolute bounds.

    ```python
    elif trend == "DU":  # DownUp
        midpoint_ratio = random.uniform(0.4, 0.6)
        midpoint = zones[zone_num][0] + (zones[zone_num][1] - zones[zone_num][0]) * midpoint_ratio

        if d <= midpoint:
            # Decreasing part
            normalized_zone_depth = (d - zones[zone_num][0]) / (midpoint - zones[zone_num][0]) if (midpoint - zones[zone_num][0]) > 0 else 0
            return round(float(max_val - (max_val - min_val) * normalized_zone_depth), 2)
        else:
            # Increasing part
            normalized_zone_depth = (d - midpoint) / (zones[zone_num][1] - midpoint) if (zones[zone_num][1] - midpoint) > 0 else 0
            return round(float(min_val + (max_val - min_val) * normalized_zone_depth), 2)
    ```

*   **`RM` (Random):** Values generated completely randomly, from min to max.
    *   `min_val`, `max_val`: Set the absolute bounds.

    ```python
     elif trend == "RM": # Random
        return round(random.uniform(min_val, max_val), 2)
    ```

## Ideas for Other Trends

Here are some ideas for additional trends:

*   **`Oscillating`**: The value oscillates between the minimum and maximum values with a defined period and amplitude (e.g., using a sine wave). You could control the frequency and amplitude.
*   **`Step`**: The value remains constant for a certain depth/time, then abruptly jumps to a new value (either randomly or by a fixed amount). You'd need parameters for the step size and the interval between steps.
*   **`NoisyIncreasing` / `NoisyDecreasing`**: Similar to `UP` and `DN`, but with added random noise. This would combine a general trend with more short-term variability. You could control the noise level.
*   **`ExponentialIncrease` / `ExponentialDecrease`**: The value increases or decreases exponentially. You'd need a parameter for the growth/decay rate.
*   **`RandomWalk`**: The value changes by a random amount at each step (can go up or down). This is different from `HF` because there's no central tendency. You'd need a parameter for the maximum step size.
*   **`CyclicUpDown`**: Repeatedly cycles through an UpDown pattern. This would be like `UD`, but instead of stopping at the end, it would repeat. You'd need a parameter for the cycle length.
*   **`DelayedTrend`**: Combines a stagnant phase with any other trend. It remains stagnant for a specified depth/time, and *then* starts behaving according to the other chosen trend (e.g., "DelayedUP", "DelayedHF").
*   **`CombinedTrend`**: Combines two trends, applying one for a portion of the depth and the other after. Could have parameters for both trend types, and where the switch occurs.

These are just a few examples. The key is to think about how you want the parameters to vary in your simulation and then design a trend that captures that behavior. You can combine aspects of existing trends and introduce new parameters to create a wide variety of dynamic patterns.
