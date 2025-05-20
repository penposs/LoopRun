# ComfyUI Batch Info Calculator Node

A custom node for ComfyUI designed to calculate batch information (start frame, frame count) for processing sequences like video frames. It's intended to be used with an external mechanism for providing the "current run number," such as a manual integer input or a specialized integer node that auto-increments after each generation.

# ComfyUI 批处理信息计算器节点

一个为 ComfyUI 设计的自定义节点，用于计算处理序列（如视频帧）的批处理信息（起始帧、帧计数）。它旨在与外部机制（例如手动整数输入或每次生成后自动递增的专用整数节点）配合使用，以提供“当前运行轮次”。

---
![Uploading baebcbf3c0a80c2f8a1d458bec53775.png…]()



## Features

-   **Batch Calculation**: Determines the start frame and number of frames for a specific run/batch based on total items, items per batch, and the current run number.
-   **Run Information**: Outputs the total number of runs needed, and flags for a valid run or the last valid run.
-   **Flexible Iteration**: Works прозрачно with manual run number input or with auto-incrementing integer nodes for semi-automated batch processing.
-   **Bilingual UI**: Node name and input parameter names provide English and Chinese.

## 特性

-   **批次计算**: 根据总项目数、每批项目数和当前运行轮次，确定特定运行/批次的起始帧和帧数。
-   **运行信息**: 输出所需的总运行轮次数，以及用于指示有效运行或最后有效运行的标志。
-   **灵活迭代**: 可与手动运行轮次输入或自动递增的整数节点配合使用，实现半自动化的批处理。
-   **双语界面**: 节点名称和输入参数名称提供中英文。

---

## Installation

1.  **Clone or Download:**
    If this node is part of a larger pack (e.g., `ComfyUI-MyVideoTools`), clone or download that pack into your `ComfyUI/custom_nodes/` directory.
    Example for a pack named `ComfyUI-MyVideoTools`:
    ```bash
    cd ComfyUI/custom_nodes/
    git clone https://github.com/Penposs/ComfyUI-LoopRun.git
    ```
    (Replace with the actual repository URL.)
    Alternatively, if it's a single file distribution, place the `batch_info_calculator.py` and `__init__.py` (if provided as part of a minimal pack structure) into a new folder like `ComfyUI-MyVideoTools` inside `ComfyUI/custom_nodes/`.

2.  **Restart ComfyUI:**
    After installation, restart ComfyUI. The node "Batch Info Calculator / 批处理信息计算器" should appear under its designated category (e.g., "Utilities/Batching") when you right-click and "Add Node".

## 安装

1.  **克隆或下载:**
    如果此节点是一个更大包（例如 `ComfyUI-LoopRun`）的一部分，请将该包克隆或下载到您的 `ComfyUI/custom_nodes/` 目录中。
    名为 `ComfyUI-MyVideoTools` 的包的示例：
    ```bash
    cd ComfyUI/custom_nodes/
    git clone https://github.com/penposs/ComfyUI-LoopRun.git
    ```
    (请替换为实际的仓库 URL。)
    或者，如果是单个文件分发，请将 `batch_info_calculator.py` 和 `__init__.py`（如果作为最小包结构的一部分提供）放入 `ComfyUI/custom_nodes/` 内的新文件夹中，例如 `ComfyUI-MyVideoTools`。

2.  **重启 ComfyUI:**
    安装后，重启 ComfyUI。“Batch Info Calculator / 批处理信息计算器”节点应该会出现在其指定的类别下（例如 "Utilities/Batching"），当您右键单击并选择“添加节点”时。

---

## How to Use

The `Batch Info Calculator` determines which frames to process for a given run number. To process an entire sequence, you'll need to increment the run number for each execution.

**Inputs:**

*   `Total Items (e.g., Frames) / 总项目数 (例如总帧数)`: The total number of items in your sequence.
*   `Items Per Batch (Frames per run) / 每批项目数 (每轮运行帧数)`: How many items to process in each run.
*   `Current Run Number (1-indexed) / 当前运行轮次 (从1开始)`: The current run number (1 for the first run, 2 for the second, etc.). This is typically fed by an external integer node.
*   `Start Item Offset (0-indexed) / 起始项目偏移 (从0开始)` (Optional): Offset for the starting item.

**Outputs:**

*   `frame_start` (Frame Start / 起始帧): The calculated starting frame index (0-based) for the current run.
*   `frame_count` (Frame Count / 帧计数): The number of frames to process in the current run. Will be 0 if `Current Run Number` is invalid.
*   `total_runs_needed` (Total Runs Needed / 总运行轮数): The total number of runs required to process all items.
*   `is_last_valid_run` (Is Last Valid Run / 是否最后有效轮): Boolean, true if this is the last run that processes actual items.
*   `is_valid_run` (Is Valid Run / 是否有效轮): Boolean, true if the provided `Current Run Number` is within the range of `total_runs_needed`.

**Example Workflow (Using an Auto-Incrementing Integer Node):**

This workflow assumes you have an integer node (like the `#25 Int` node in your example with `control_after_generate: increment`) that automatically increases its value after each generation.

1.  **Add Nodes**:
    *   `Batch Info Calculator / 批处理信息计算器`
    *   Your video/image loading node (e.g., VHS `Load Video`).
    *   An **Auto-Incrementing Integer Node**. Configure its starting value (e.g., to `1` if it's 1-indexed, or `0` if you need to add 1 afterwards) and ensure its auto-increment feature is active.

2.  **Connect Auto-Incrementing Integer**:
    *   Connect the output of your Auto-Incrementing Integer Node to the `Current Run Number / 当前运行轮次` input of the `Batch Info Calculator`.
    *   *(If your auto-incrementing node starts at 0 and `Batch Info Calculator` expects 1-indexed runs, you might need a simple Math node to add 1 in between).*

3.  **Configure `Batch Info Calculator`**:
    *   Set `Total Items` and `Items Per Batch`.

4.  **Connect to Loader**:
    *   `Batch Info Calculator` -> `frame_start` to Video Loader's start frame input.
    *   `Batch Info Calculator` -> `frame_count` to Video Loader's frame count input.

5.  **Control Downstream Processing (Optional but Recommended)**:
    *   Use the `is_valid_run` output from `Batch Info Calculator` with a conditional gate/switch (e.g., from Impact Pack) to control whether downstream nodes (like image saving) execute. Only execute them if `is_valid_run` is `True`.

6.  **Run**:
    *   Enable "Auto Queue" in ComfyUI's options.
    *   Click "Queue Prompt" once. The workflow should now automatically process batch after batch.

```mermaid
graph LR
    subgraph IterationControl ["轮次控制 (使用自增整数节点)"]
        AutoIncrementInt["#25 Auto-Incrementing INT\n(e.g., starts at 1, increment after gen)\n(例如, 初始值1, 生成后递增)"]
    end

    subgraph BatchCalculation ["批处理计算"]
        BatchCalc["Batch Info Calculator\n批处理信息计算器"]
        AutoIncrementInt -- "轮次 (1, 2, 3...)" --> BatchCalc("Current Run Number / 当前运行轮次")
    end
    
    BatchCalc -- "total_runs_needed\n(总运行轮数)" --> DisplayTotalRuns["(显示节点: 共需N轮)"]


    subgraph VideoLoading ["视频加载"]
        VideoLoader["Video Loader\n视频加载器"]
        BatchCalc -- "frame_start (起始帧)" --> VideoLoader(start_frame)
        BatchCalc -- "frame_count (帧计数)" --> VideoLoader(frame_count)
    end
    
    VideoLoader --> MainProcessing["Main Processing Logic...\n主要处理逻辑..."]

    subgraph ConditionalSaving ["可选: 条件性保存"]
        ConditionalGate["Conditional Gate / Switch\n条件门/开关"]
        SaveNode["Save Image/Video\n保存图像/视频"]
        BatchCalc -- "is_valid_run (是否有效轮)" --> ConditionalGate(condition)
        MainProcessing -- Data --> ConditionalGate(input_if_true)
        ConditionalGate -- output_if_true --> SaveNode
    end
