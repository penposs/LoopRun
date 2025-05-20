import math

class BatchInfoCalculator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "total_items": ("INT", {
                    "default": 1000, "min": 1, "max": 10000000, "step": 1,
                    "display": "Total Items (e.g., Frames) / 总项目数 (例如总帧数)"
                }),
                "items_per_batch": ("INT", {
                    "default": 81, "min": 1, "max": 10000, "step": 1,
                    "display": "Items Per Batch (Frames per run) / 每批项目数 (每轮运行帧数)"
                }),
                "current_run_number": ("INT", { # 1-indexed for user input
                    "default": 1, "min": 1, "max": 10000, "step": 1,
                    "display": "Current Run Number (1-indexed) / 当前运行轮次 (从1开始)"
                }),
            },
            "optional": {
                 "start_item_offset": ("INT", {
                     "default": 0, "min": 0, "max": 10000000, "step": 1,
                     "display": "Start Item Offset (0-indexed) / 起始项目偏移 (从0开始)"
                 }),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "BOOLEAN", "BOOLEAN")
    RETURN_NAMES = (
        "frame_start",          # Calculated start frame for the current run
        "frame_count",          # Calculated frames in this run
        "total_runs_needed",    # Total runs needed to process all items
        "is_last_valid_run",    # True if this run_number processes the last items
        "is_valid_run"          # True if current_run_number is within the valid range
    )
    FUNCTION = "calculate_batch_info"
    CATEGORY = "Utilities/Batching" # Or your preferred category

    def calculate_batch_info(self, total_items, items_per_batch, current_run_number, start_item_offset=0):
        if items_per_batch <= 0:
            items_per_batch = 1
        if total_items <= 0: # If total_items is 0 or negative, no valid runs possible
            return (start_item_offset, 0, 0, False, False)
        if current_run_number <=0: # Run number should be positive
            current_run_number = 1

        effective_total_items = total_items - start_item_offset
        if effective_total_items <= 0: # Offset is beyond or at the end
             return (start_item_offset, 0, 0, False, False) # No items to process

        total_runs_needed = math.ceil(effective_total_items / items_per_batch)
        if total_runs_needed == 0 and effective_total_items > 0 : # e.g. items_per_batch > effective_total_items
            total_runs_needed = 1


        is_valid_run = (1 <= current_run_number <= total_runs_needed)
        is_last_valid_run = (is_valid_run and current_run_number == total_runs_needed)

        frame_start_calculated = 0
        frame_count_calculated = 0

        if is_valid_run:
            # Convert 1-indexed current_run_number to 0-indexed iteration for calculation
            current_iteration_0_indexed = current_run_number - 1
            
            start_index_relative = current_iteration_0_indexed * items_per_batch
            frame_start_calculated = start_index_relative + start_item_offset
            
            remaining_items_from_start_relative = effective_total_items - start_index_relative
            frame_count_calculated = min(items_per_batch, remaining_items_from_start_relative)
        else:
            # If run_number is invalid (e.g., too high or too low)
            # Output values that signify no processing or an error state
            if current_run_number > total_runs_needed and total_runs_needed > 0:
                # If user requests a run beyond the last valid one, point to the end with 0 frames
                last_valid_iteration_0_indexed = total_runs_needed - 1
                start_index_relative_for_last = last_valid_iteration_0_indexed * items_per_batch
                frame_start_calculated = start_index_relative_for_last + start_item_offset + (effective_total_items - start_index_relative_for_last) # Start after the very last item
                frame_count_calculated = 0 # No frames to process
            else: # (current_run_number <= 0 or total_runs_needed == 0)
                frame_start_calculated = start_item_offset # Default to start offset
                frame_count_calculated = 0


        return (
            int(frame_start_calculated),
            int(frame_count_calculated),
            int(total_runs_needed),
            is_last_valid_run,
            is_valid_run
        )