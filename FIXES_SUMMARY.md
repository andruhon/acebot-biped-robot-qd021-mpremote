# Summary of Fixes for Acebot Biped Robot

This document summarizes the issues identified and corrected in the Acebot Biped Robot codebase (QD021). These fixes address pin wiring discrepancies and movement logic errors ("limping") which appeared to be caused by asymmetric values in the motion matrices.

## 1. Core Library Fixes

**File:** `libs/ACB_Biped_Robot.py`

- **Issue:** The `servo_init` function incorrectly swapped the mapping for the 3rd and 4th servos.
  - _Original:_ `[pin1, pin2, pin4, pin3]`
  - _Fixed:_ `[pin1, pin2, pin3, pin4]`
- **Issue:** The internal `backward` movement matrix resulted in asymmetric/limping motion.
  - _Fixed:_ Replaced with a new symmetric gait matrix derived by mathematically inverting the working Forward movement (inverting Thigh angles).

## 2. Pin Configuration Corrections

**Status:** All Lesson files were defining pins contrary to the physical wiring/documentation.

- **Issue:** Code defined `Right_thigh = 26`, `Right_calf = 25`.
- **Fixed:** Updated all files to `Right_thigh = 25`, `Right_calf = 26` to match the paper documentation and physical hardware.
- **Applied to:**
  - `lesson1/servo_90.py`
  - `lesson2/*.py` (All files)
  - `lesson3/Move_Follow.py`
  - `lesson4/Move_Avoid.py`
  - `lesson5/Move_Dance1.py`
  - `lesson6/Move_Dance2.py`
  - `lesson7/Biped_Robot_Web.py`
  - `lesson8/QD021_Robot_APP.py`

## 3. Movement Logic Fixes

**Status:** Backward motion was corrupted in multiple locations.

- **Issue:** "Limping" backward gait caused by incorrect servo angles in the matrix.
- **Fixed:** Replaced the local `backward` matrix with the corrected symmetric version (same as Library fix).
- **Applied to:**
  - `lesson2/Move_Backward.py`
  - `lesson2/Serial_Control.py`
  - `lesson3/Move_Follow.py`
  - `lesson4/Move_Avoid.py` (Local backward matrix was present and corrupt)

## Summary Table

| Component              | Issue                    | Fix                    |
| :--------------------- | :----------------------- | :--------------------- |
| **ACB_Biped_Robot.py** | Swapped pins 3/4 in init | Corrected list order   |
| **All Lessons**        | Wrong RT/RC pin numbers  | Set RT=25, RC=26       |
| **Backward Matrix**    | Asymmetric gait (Limps)  | Inverted Forward logic |
