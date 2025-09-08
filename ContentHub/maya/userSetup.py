import sys
import os

tool_paths = [
    r"D:\Xicheng\Projects\HarshBlue\Maya-Unreal-Tool-Dev-Course\Code\maya-unreal-devtools\ContentHub\maya",
    r"D:\Xicheng\Projects\HarshBlue\Maya-Unreal-Tool-Dev-Course\Code\maya-unreal-devtools\ContentHub\shared",
]

for p in tool_paths:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.append(p)
        print(">>> Custom tool path added:", p)