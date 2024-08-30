See README.pdf

## Steps

1. modify config.yaml to write down your openai apikey sk-...
2. define the trajectory description in : `/Users/huangziheng/PycharmProjects/final_LLM_enhance/prompt/trajectories.txt`
3. run `/Users/huangziheng/PycharmProjects/final_LLM_enhance/several_prompts_good.py` npy will be saved to`/Users/huangziheng/PycharmProjects/final_LLM_enhance/npysave`
4. run `/Users/huangziheng/PycharmProjects/final_LLM_enhance/Humanml/scale_tool_group.py` to get scaled data (align with humanml dataset) after this step you can get final data in `/Users/huangziheng/PycharmProjects/final_LLM_enhance/npysave/scaled`
5. recomend to run `/Users/huangziheng/PycharmProjects/final_LLM_enhance/plot_ingroup.py` to plot everything.



Update friday 9/30:

There are 2 functions in the main py: `several_prompts_good.py`

```
interpolate_and_resample_velocity
```

uses

```
dx, dy = splev(ui, tck, der=1)  # First derivative gives the tangent vector
root_linear_velocity.append((dx, dy))
```





```
interpolate_and_resample_velocity2
```

uses

```
velocity_vectors = [(uniform_points[i][0] - uniform_points[i - 1][0],
                     uniform_points[i][1] - uniform_points[i - 1][1]) for i in range(1, len(uniform_points))]
```



So I recommend `interpolate_and_resample_velocity2`function 

this time you should still  run `/Users/huangziheng/PycharmProjects/final_LLM_enhance/Humanml/scale_tool_group.py` to get scaled data

this time you should use plot_unscaled_velocityrecover_v2.py to plot `interpolate_and_resample_velocity2` result and use `plot_scaled.py` to plot scaled result ( in `/Users/huangziheng/PycharmProjects/final_LLM_enhance/npysave/scaled`)

generated from /Users/huangziheng/PycharmProjects/final_LLM_enhance/Humanml/scale_tool_group.py 



```
Last login: Fri Aug 30 10:26:03 on console
You have new mail.
(base) ➜  ~ /Users/huangziheng/PycharmProjects/final_LLM_enhance 
(base) ➜  final_LLM_enhance git:(main) ✗ tree /Users/huangziheng/PycharmProjects/final_LLM_enhance
/Users/huangziheng/PycharmProjects/final_LLM_enhance
├── 1.py
├── Humanml
│   ├── 012314_npy_Data.csv
│   ├── checkdata263.py
│   ├── new_joint_vecs
│   │   └── 012314.npy
│   ├── new_joints
│   │   └── 012314.npy
│   ├── scale_tool.py
│   ├── scale_tool_group.py
│   └── visualize.py
├── README.md
├── README.pdf
├── bad.py
├── config.yaml
├── image
│   ├── Screenshot 2024-08-29 at 00.35.08.png
│   ├── U_shape.png
│   ├── U_turn.png
│   ├── capital_W.png
│   ├── capital_j.png
│   ├── capital_pi.png
│   ├── figure_eight.png
│   ├── inverse_N.png
│   ├── number9.png
│   ├── semicircle.png
│   ├── spiral.png
│   ├── spiral_staircase.png
│   ├── triangle.png
│   ├── walk_turn_continue.png
│   └── zigzag.png
├── log
│   └── model_interaction_log.txt
├── npysave
│   ├── U_shape.npy
│   ├── U_turn.npy
│   ├── already
│   │   ├── capital_W.npy
│   │   ├── capital_j.npy
│   │   ├── capital_j_scaled.npy
│   │   ├── capital_pi.npy
│   │   ├── figure_eight.npy
│   │   ├── inverse_N.npy
│   │   ├── number9.npy
│   │   ├── semicircle.npy
│   │   ├── spiral.npy
│   │   ├── spiral_staircase.npy
│   │   ├── triangle.npy
│   │   ├── walk_turn_continue.npy
│   │   └── zigzag.npy
│   └── scaled
│       ├── U_shape_scaled.npy
│       ├── U_turn_scaled.npy
│       ├── capital_W_scaled.npy
│       ├── capital_j_scaled.npy
│       ├── capital_j_scaled_scaled.npy
│       ├── capital_pi_scaled.npy
│       ├── figure_eight_scaled.npy
│       ├── inverse_N_scaled.npy
│       ├── number9_scaled.npy
│       ├── semicircle_scaled.npy
│       ├── spiral_scaled.npy
│       ├── spiral_staircase_scaled.npy
│       ├── triangle_scaled.npy
│       ├── walk_turn_continue_scaled.npy
│       └── zigzag_scaled.npy
├── plot.py
├── plot_ingroup_velocityrecover_v1.py
├── plot_scaled.py
├── plot_unscaled_velocityrecover_v2.py
├── prompt
│   ├── ChainPrompt.txt
│   ├── follow_up_question.txt
│   ├── trajectories.txt
│   └── trajectories_copy.txt
├── result
│   └── newResult.txt
├── root_linear_velocity.txt
├── several_prompts_good.py
├── several_prompts原来的sample点的.py
├── some possible errors
├── test
│   ├── 111.py
│   ├── draw_patterns.py
│   ├── execute_code_and_compute_keyframes.py
│   ├── great_recover_speed_test.py
│   ├── great_recover_speed_test2.py
│   ├── imagesGPT
│   │   ├── 20240828231607_keyframes.png
│   │   ├── 20240829003813_keyframes.png
│   │   └── 20240830143413_keyframes.png
│   ├── interpolate_and_resample_velocity_test.py
│   ├── keyframes.txt
│   ├── keyframes8.txt
│   ├── pattern.txt
│   └── shape_curve.txt
└── useless
    ├── ChainPromptResult2 copy.txt
    ├── ChainPromptResult2.txt
    ├── ChainPrompt_onlycurve_en.txt
    ├── Result.txt
    ├── follow_up_question2.txt
    ├── follow_up_question3.txt
    ├── model_interaction_log_old.txt
    ├── several_prompts.py
    ├── several_prompts2.py
    ├── trajectories.txt
    └── trajectories2.txt

14 directories, 95 files
(base) ➜  final_LLM_enhance git:(main) ✗ 

```





