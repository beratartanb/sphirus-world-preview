# SHME V2.38 research: NVIDIA motion models and UE features for hard 45/90/135/180 deg redirects

Read-only web/docs research. All sources were read on **2026-10-30**, so "(read 2026-10-30)" applies to every URL below unless a line says otherwise. Nothing was downloaded, cloned, installed or run.

Some lines are labelled **[assessment]**. Those are my engineering judgement for SPHIRUS and are not claims made by the source. A few lines rest only on a search-result snippet because the page itself refused the fetch (HTTP 403). Those lines are labelled **[snippet only]**.

Physics caveat for the whole file: MotionBricks, ARDY and Kimodo are **kinematic** generators. They produce joint transforms and foot-contact labels. They give **no physical balance, momentum or friction guarantee**. Any braking or support-transfer realism has to be checked in our own SHME COM/support/capture-point metrics and by eye.

---

## 1. NVIDIA MotionBricks

**What it generates**
- It is described as "a modular latent generative model that animates characters and robots in real time": a root module (duration plus root path), a pose module and a decoder. https://github.com/NVlabs/motionbricks
- The output is kinematic. The SOMA model card says "kinematic output does not establish dynamic feasibility, collision avoidance, or safe contact", and the HF card says it is "not a controller for a physical robot". https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md and https://huggingface.co/nvidia/MotionBricks

**Inputs and conditioning**
- Context is the 4 most recent poses. Targets are 1 to 4 placed poses: 1 pose sets where the character ends up and stops, and 2 to 4 poses also constrain velocity and acceleration at the target. https://github.com/NVlabs/motionbricks and https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/runtime_api.md
- There is no text input and no scene-geometry input. The application places the targets and handles obstacles. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md
- Speed and direction are set indirectly. The locomotion example samples target poses that match the desired speed and places them ahead of the character along the desired velocity. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/runtime_api.md
- Per-target options are `transition_early_by_frames` (treat a target as a guide) and, on SOMA only, an `ik_pin_mask`. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/runtime_api.md
- Style comes through "Smart Primitives", which turn target poses into building blocks. Scene Preview has 6 style modes (for example skipping and zombie). https://github.com/NVlabs/motionbricks and https://nvlabs.github.io/motionbricks/

**Skeleton**
- Supported skeletons are SOMA (30 joints, root `Hips`, metres, Y-up, 30 FPS) and Unitree G1. The two are not interchangeable. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md and https://huggingface.co/nvidia/MotionBricks
- It is not SMPL. SOMA is NVIDIA's unifying body layer over SMPL, SMPL-X, MHR and Anny. https://arxiv.org/abs/2603.16858 (search-result summary)

**Retargeting to MetaHuman**
- The NVIDIA SOMA Retargeter only targets robots. It reads SOMA BVH and writes robot CSV, with no human-skeleton or Unreal target. https://github.com/NVIDIA/soma-retargeter
- I found no official SOMA to MetaHuman/UE path. The UE route would be the standard IK Retargeter (source IK Rig to target IK Rig). https://dev.epicgames.com/documentation/metahuman/animation (search-result summary)
- **[assessment]** We would need to do all of the following ourselves:
  - Build a SOMA skeletal mesh or skeleton in UE (or import a SOMA BVH via Blender to FBX).
  - Write an exporter from `AnimationBuffer` to BVH or FBX. Writing files to disk is not documented.
  - Convert Y-up metres to Z-up centimetres.
  - Author a SOMA IK Rig with leg IK chains plus a retargeter to the MetaHuman IK Rig. Our own memory notes that missing IK-chain ops shortened stride by 3.8 %.
  - Extract root motion, transfer the 4 heel/toe contact channels to curves or notifies, and resample 30 to 30/60 Hz.

**Changing targets mid-motion**
- The application decides when to generate. Calling `generate()` again reads the recorded history, generates toward the new target and restarts playback. It is "usually" called when `time_to_transition` falls below the update time, or earlier when the input changes. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/runtime_api.md
- Interrupting a generation that is already running is not documented. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/runtime_api.md
- Errors can accumulate when output is fed back as context. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md

**Output frame rate and format**
- Output is 30 Hz. One generation is 24 to 64 raw frames, or 18 to 58 valid frames (about 0.6 to 1.9 s).
- The tensor is `pred_global_motions [N,64,366]`: root pos+heading, joint positions, 6D rotations, joint velocities and 4 foot-contact flags (L/R heel and toe). https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md
- The model ships as ONNX (opset 17, FP32 or mixed FP16, about 200 M parameters), with SafeTensors checkpoints. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md

**Runtime cost and GPU/VRAM**
- The paper claims "15,000 FPS with 2 ms latency". https://arxiv.org/abs/2604.24833
- Timings are reported only for an RTX 4090. VRAM is not stated. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md
- It needs an NVIDIA GPU with TensorRT 10.8. The first launch per model/precision builds a TensorRT plan, which takes "a few minutes". https://github.com/NVlabs/motionbricks and https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/runtime_api.md

**OS support**
- Demos were tested on Windows and Linux x86-64. The SOMA card lists Windows as the tested OS. https://github.com/NVlabs/motionbricks and https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md

**Licenses**
- Code is Apache 2.0. https://github.com/NVlabs/motionbricks
- Weights are under the NVIDIA Open Model Agreement, and **commercial use is allowed**. https://huggingface.co/nvidia/MotionBricks
- That license text says "Models are commercially usable", that NVIDIA claims no ownership of outputs, and that a Notice file is required when the model is redistributed. It also has guardrail-bypass and patent-litigation termination clauses. https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
- The sample BVH/CSV motions are under the NVIDIA Sample Data Evaluation License, which allows **internal evaluation only**. They must not be shipped. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md

**Release and maturity**
- The arXiv v1 is dated 2026-04-27 (SIGGRAPH 2026 / ACM TOG). https://arxiv.org/abs/2604.24833
- The repo calls itself a first release after a G1 preview. It is not accepting contributions, and the training pipeline and data are not included. https://github.com/NVlabs/motionbricks and https://huggingface.co/nvidia/MotionBricks

**Braking, redirect and catch-step examples**
- No clip is labelled as braking, a pivot or a catch step. The project page claims "continuous runtime transitions across speed, direction, and gait" (idle, walk, jog, run) and plays a 2:40 uncut UE5 demo. https://nvlabs.github.io/motionbricks/
- The demo uses **no foot-locking, blending or collision detection**. A foot-skating result is not reported. https://nvlabs.github.io/motionbricks/ and https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md
- Training data is Bones RigPlay 1: 313,526 clips selected from about 350k clips and 700 h. https://raw.githubusercontent.com/NVlabs/motionbricks/main/docs/soma_model.md
- **[assessment]** Its context-plus-target interface matches our offline use well. As context we would feed 4 poses of the jog/sprint loop. As targets we would feed 2 to 4 poses of the destination-direction loop, rotated 45/90/135/180 deg. It then picks timing and root path itself. Whether it produces a real brake plant, pivot foot and re-push for hard cuts is **unverified**: it has to be measured against our generator on slip, pelvis drop and support timing.

---

## 2. NVIDIA ARDY

**What it generates**
- The full name is "Autoregressive Diffusion with Hybrid Representation for Interactive Human Motion Generation". It is a streaming, two-stage autoregressive transformer denoiser: root first, then latent body tokens. https://research.nvidia.com/labs/sil/projects/ardy/ and https://arxiv.org/abs/2607.08741
- Output is **kinematic**: joint positions/rotations, root positions and foot contacts, saved as `.npz`. G1 also gets MuJoCo qpos CSV. https://github.com/nv-tlabs/ardy

**Conditioning**
- Supported conditions are online text prompts, root paths/waypoints, full-body keyframes, and sparse end-effector joint positions/rotations, plus long-horizon goals beyond the window and constraint chains. https://research.nvidia.com/labs/sil/projects/ardy/
- The demo adds target-velocity control (arrow keys) and a waypoint mode. https://github.com/nv-tlabs/ardy
- Running without text appears in the benchmark tables, but the README gives no switch to skip the text encoder. https://github.com/nv-tlabs/ardy

**Skeletons and checkpoints**
- Core (20 FPS) and Unitree G1 (25 FPS) were released 2026-07-10. **SOMA 30-joint checkpoints at 30 FPS, Horizon 60** (`ARDY-SOMA-RP-30FPS-Horizon60` and `...-KimodoRep-Horizon60`) were released **2026-10-15**, about 2 weeks before this research. https://github.com/nv-tlabs/ardy and https://huggingface.co/nvidia/ARDY-SOMA-RP-30FPS-Horizon60
- The output tensor covers up to 8 s. https://huggingface.co/nvidia/ARDY-SOMA-RP-30FPS-Horizon60
- A search snippet from earlier still said SOMA was "coming soon". The current README supersedes it. https://github.com/nv-tlabs/ardy

**Retargeting**
- Retargeting needs the same SOMA to MetaHuman work as for MotionBricks (section 1). No UE path is provided. **[assessment]**

**Changing targets mid-motion**
- Yes. It is designed for streaming with online prompt changes, and there is a replan buffer. The rule is that generation time must be less than "(replan buffer + 1) frames playback time". https://github.com/nv-tlabs/ardy

**Cost and hardware**
- Tested on an RTX 4090 with driver 575. Latency figures are not given. https://github.com/nv-tlabs/ardy
- The text encoder is LLM2Vec on the **gated Meta-Llama-3-8B-Instruct**, which needs a Hugging Face access grant and token and is under Meta's own license terms (not quoted here). It uses about **14 GB VRAM** in bf16 on GPU, or it can run on CPU. https://github.com/nv-tlabs/ardy
- Install needs Python 3.10+ and PyTorch 2.4+. A C++17/CMake build is required for the optional motion-correction extension, which reduces foot skating, is slower and is off by default. https://github.com/nv-tlabs/ardy

**OS**
- The README says "mainly tested on Ubuntu Linux 22.04". The SOMA HF card lists **Linux** as the OS. **Windows is not stated.** https://github.com/nv-tlabs/ardy and https://huggingface.co/nvidia/ARDY-SOMA-RP-30FPS-Horizon60

**Licenses**
- Code is Apache-2.0. https://github.com/nv-tlabs/ardy
- Weights are under the NVIDIA Open Model Agreement, and the SOMA card says "ready for commercial or non-commercial use". https://huggingface.co/nvidia/ARDY-SOMA-RP-30FPS-Horizon60
- The text encoder adds a Meta Llama 3 dependency with separate terms. https://github.com/nv-tlabs/ardy

**Maturity**
- arXiv v1 is dated 2026-07-09. It is SIGGRAPH 2026 / TOG 45(4). https://arxiv.org/abs/2607.08741

**Balance correction or recovery**
- No recovery, push or balance examples are shown. https://research.nvidia.com/labs/sil/projects/ardy/
- Listed limitations are foot skating, unawareness of scene objects, a single character, and motion that does not always follow the prompt. https://huggingface.co/nvidia/ARDY-SOMA-RP-30FPS-Horizon60
- **Any "recovery step" ARDY produces would be a kinematic imitation of mocap, not a balance solution.**

### 2b. Related NVIDIA offline model: Kimodo (not asked, but closest to our offline use)
- Kimodo is a kinematic motion diffusion model. It takes text plus constraints at chosen frames: 3D joint positions, joint rotations, **2D heading** and **2D root position**. Clips are at most 10 s (300 frames) at 30 fps on the SOMA 30-joint skeleton. https://huggingface.co/nvidia/Kimodo-SOMA-SEED-v1.1
- The SOMA weights are under the NVIDIA Open Model License ("ready for commercial use"). OS is **Linux and Windows**. Tested GPUs are RTX 3090/4090/5090 and others. VRAM is not stated on the card. https://huggingface.co/nvidia/Kimodo-SOMA-SEED-v1.1
- A secondary source says about 17 GB of VRAM; this is unverified. https://howaiworks.ai/nvidia-kimodo-3d-motion-generation/ (search-result summary)
- The **SMPL-X Kimodo weights are non-commercial (NVIDIA R&D Model License)**. Do not use them. https://huggingface.co/nvidia/Kimodo-SMPLX-RP-v1 (search-result summary)
- Its limitations include foot skating. https://huggingface.co/nvidia/Kimodo-SOMA-SEED-v1.1

---

## 3. NVIDIA ProtoMotions

**What it is**
- It is a GPU-accelerated framework for **training physically simulated** humanoids and robots with RL (ProtoMotions3, v3). https://github.com/NVlabs/ProtoMotions
- Simulators are IsaacGym (legacy), IsaacLab/IsaacSim (recommended for training), Newton 1.0 (MuJoCo-Warp) and MuJoCo (CPU, single env, for testing only). https://nvlabs.github.io/ProtoMotions/getting_started/quickstart.html
- Genesis is not in the README. A third-party listing shows a `requirements_genesis.txt` file. https://tomevault.io/tome/NVlabs/ProtoMotions (search-result summary)

**Pretrained policies**
- The published policies are:
  - SOMA BONES-SEED tracker
  - SOMA BONES-SEED FSQ tracker
  - SOMA GPC prior
  - G1 BONES-SEED deployment tracker
  - **Metatron v1 G1 (MaskedMimic)**, described as "motion, recovery, and scene-conditioned control"
- The three SOMA models are **IsaacLab only**. https://nvlabs.github.io/ProtoMotions/getting_started/pretrained_models.html
- The quickstart also shows a MaskedMimic SMPL checkpoint path. https://gitverse.ru/redgpu/nvidia-ProtoMotions/content/main/docs/source/getting_started/quickstart.rst (mirror, search-result summary)

**Hardware and training cost**
- Full-AMASS training takes about 12 h on 4x A100. BONES training used 24x A100. https://github.com/NVlabs/ProtoMotions
- IsaacLab needs **Linux x86_64** (Python 3.12, Isaac Sim 6.0). Newton needs a GPU with CC 5.0+ and driver 545+. VRAM is not specified. https://nvlabs.github.io/ProtoMotions/getting_started/installation.html

**License**
- Code is Apache-2.0. NVIDIA models are under the NVIDIA Open Model License unless a model card says otherwise. Datasets and robot assets keep their own terms. https://nvlabs.github.io/ProtoMotions/getting_started/pretrained_models.html

**Usable in Unreal without its simulator?**
- No. Policies output actuator targets for a simulated body. An ONNX export exists for G1 deployment, and a C++ MuJoCo/Unitree runtime is marked experimental and "not a supported release artifact". https://github.com/NVlabs/ProtoMotions
- **[assessment]** Running a policy in Chaos would need matching body masses, joint limits, PD gains and timestep. That is not practical for a Blueprint-only project. The only realistic use is offline: physically "filtering" our generated clips by tracking them in Newton/MuJoCo or IsaacLab, then re-exporting them kinematically. That is research-grade work, Linux-leaning for SOMA, and would still need retargeting both ways.

**Balance and recovery ideas that could inform a cheap kinematic decision layer**

From the sources:
- Recovery is learned from **randomised velocity-impulse pushes**:
  - Interval of 1.0 to 3.0 s.
  - Linear velocity up to (0.5, 0.5, 0.2) m/s.
  - Angular up to (0.52, 0.52, 0.78) rad/s.
  - Plus reset noise on the start pose and velocity, and friction 0.3 to 1.6 static / 0.3 to 1.2 dynamic.
  https://nvlabs.github.io/ProtoMotions/tutorials/workflows/domain_randomization.html
- Steering targets are transformed into a **robot-local frame** and reduced to a 5D feature. Trackers observe proprioception plus **target future poses**. https://github.com/NVlabs/ProtoMotions and https://nvlabs.github.io/ProtoMotions/user_guide/experiments.html
- MaskedMimic treats control as **motion inpainting from partial constraints** (sparse keyframes, text, objects). https://arxiv.org/abs/2409.14393
- PHC learns fail-state recovery as an added task without resets. https://arxiv.org/abs/2305.06456

**[assessment]** — how SHME could translate these:
- Express perturbation as a **velocity error** (planned versus actual COM velocity), in the same units as the push randomisation. Trigger a recovery step when the capture-point offset from the support polygon exceeds a margin. Do not trigger it on angle alone.
- Keep the decision in the **heading-local frame** of the new intent.
- Pick clips by matching the future root/foot targets ("inpainting" view): brake plant position and re-push foot are the constraints, everything else is free.
- Use friction and traction (`GroundFriction` / surface) as a scalar that scales the allowed deceleration and turn rate. This mirrors friction randomisation.

---

## 4. Unreal Engine features (docs header says **Unreal Engine 5.8**, the newest available)

| Feature | What it does (sourced) | Blueprint access | Cost / risk **[assessment]** | Fit for hard 90 deg redirect + brake + support transfer **[assessment]** |
|---|---|---|---|---|
| Pose Search / Motion Matching | Selects poses from a database by Schema query. Channels: Group, Heading, Padding, Phase, Pose, Position, Sampling Time, Trajectory, Velocity (experimental: Crashing Legs, Permutation Time). The Pose History node has Generate Trajectory and Collected Bones. Continuing Pose Cost Bias below 0 keeps the current clip, above 0 discourages it. Search modes: Brute Force, PCAKDTree, VPTree (experimental). Node settings include Blend Time/Profile, Use Inertial Blend, Pose Jump Threshold, Pose Reselect History, Search Throttle Time and Max Active Blends. https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-matching-in-unreal-engine | Yes: AnimBP node plus Choosers. Debug through the Rewind Debugger Pose Search track and the Channel Breakdown cost view. https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-matching-debugging-in-unreal-engine | Already the owner. More channels and samples raise memory/CPU. The risk is DB churn (see project memory traps). | **Usable now (owner).** Hard cuts depend on the clip content in the DB, so better authored clips are what helps. |
| Interrupt modes | `EPoseSearchInterruptMode` values: DoNotInterrupt, InterruptOnDatabaseChange, InterruptOnDatabaseChange**AndInvalidateContinuingPose**, ForceInterrupt, ForceInterrupt**AndInvalidateContinuingPose**. The invalidate variants make the schema build its query from pose history. https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PoseSearch/EPoseSearchInterruptMode | Yes: Set Database(s) To Search / Set Interrupt Mode. https://dev.epicgames.com/documentation/unreal-engine/BlueprintAPI/Animation/MotionMatching/SetInterruptMode | Low cost. Over-forcing causes pose jumps. | **Usable now.** Use it to force entry into a dedicated redirect DB at the decision frame. |
| Trajectory prediction | CharacterTrajectoryComponent (world-space history/prediction for MM). PoseSearchTrajectoryLibrary prediction from movement intent. `UpdatePrediction_SimulateCharacterMovement` simulates CMC ground math. https://docs.unrealengine.com/5.3/en-US/PythonAPI/class/CharacterTrajectoryComponent.html and https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PoseSearch/UPoseSearchTrajectoryLibrary/UpdatePrediction- | Yes | Low cost. The prediction only reflects CMC braking/turn settings, not the body. | **Usable now.** Brake realism in the query depends on the CMC values below. |
| Motion Warping | Warps **root motion** to named warp targets inside a montage notify-state window or a runtime-added modifier. Skew Warp matches location/rotation by the window end; there is also a Scale modifier. Needs EnableRootMotion. Add or Update Warp Target in BP. https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-warping-in-unreal-engine | Yes | Needs root-motion montages, which is a parallel path to MM capsule-driven motion. | **Needs adaptation.** Only useful if a redirect becomes a montage. It conflicts with the current MM/CMC ownership. |
| Orientation Warping | Rotates leg IK bones toward the locomotion direction and counter-twists the spine. Graph or Manual mode. Location Angle Delta Threshold defaults to 90 deg. https://dev.epicgames.com/documentation/en-us/unreal-engine/pose-warping-in-unreal-engine | AnimBP node | Cheap. At large angles feet twist instead of stepping. | **Usable now as a residual fix (a few degrees).** It cannot create a pivot step. |
| Stride Warping | Scales stride by `LocomotionSpeed / RootMotionSpeed` with a clamp. https://dev.epicgames.com/documentation/en-us/unreal-engine/pose-warping-in-unreal-engine | AnimBP node | Cheap. Shortening stride during a brake can hide slip but can look skating. | **Usable now (small clamp range)** for the brake speed mismatch. |
| Slope Warping | Documented as "still in development", testing environments only. https://dev.epicgames.com/documentation/en-us/unreal-engine/pose-warping-in-unreal-engine | AnimBP node | Experimental | **Experimental only.** |
| Inertialization | A post-process transition: the source pose stops evaluating, and per-request blend profiles set per-joint times. With several requests the shortest wins. Source notifies stop firing. Chained interrupted blends degrade quality. Dead Blending is **experimental, not recommended for shipping**. https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-blend-nodes-in-unreal-engine | Yes: node plus blend profile assets | Cheap. Notify loss and stacked interruptions are real risks. | **Usable now.** Use a lower-body-faster blend profile so the plant foot hands over quickly. |
| Control Rig Full Body IK | PBIK solver with effectors (position/rotation/strength alpha), Root Behavior (Pre Pull / Pin to Input / Free), Pull Chain Alpha, Mass Multiplier and Iterations (the main CPU cost). Needs the FullBodyIK plugin. https://dev.epicgames.com/documentation/en-us/unreal-engine/control-rig-full-body-ik-in-unreal-engine | Control Rig asset run from an AnimBP Control Rig node | Per-iteration CPU cost. It can fight FootPlacement. | **Needs adaptation.** Possible plant-foot pin plus pelvis-shift fixup, but it would duplicate the FootPlacement/LegIK owner. |
| Physics Control | Component of spring/damper "Controls" (body to body or world) plus "Body Modifiers" (kinematic/simulated, gravity, blend weight). BP functions include CreateControl, SetControlTarget*, SetBodyModifierMovementType. The 5.8 header is under `Plugins/Animation/PhysicsControl`. The 5.8 class page does not state a maturity level; older API paths were under `Experimental/`. https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/PhysicsControl/UPhysicsControlComponent | Yes | Simulates bodies (cost, stability, collision). It does **not** balance the character. | **Experimental only** for secondary reaction (upper body or arms). Not a brake solution. |
| Physical Animation component | Motors drive physics bodies toward animation through profiles. BP functions: ApplyPhysicalAnimationProfileBelow / SettingsBelow, SetStrengthMultiplyer. The class is **marked Experimental** in 5.8. https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UPhysicalAnimationComponent | Yes | Simulated bodies, jitter risk | **Unnecessary cost** for the redirect itself. |
| CMC braking/turn | BrakingFriction (used when bUseSeparateBrakingFriction is on and acceleration is 0) × BrakingFrictionFactor. BrakingDecelerationWalking. MaxAcceleration. RotationRate (with bOrientRotationToMovement / bUseControllerDesiredRotation). BrakingSubStepTime. https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UCharacterMovementComponent. GroundFriction: "Higher values allow faster changes in direction". **[snippet only]** https://docs.unrealengine.com/4.26/en-US/API/Runtime/Engine/GameFramework/UCharacterMovementComponent/GroundFriction/index.html | Yes, all BP-settable | Free | **Usable now.** These own the capsule's brake/turn profile that MM tries to match. Keep SHME as the single writer. |

Other note: the UE 5.8 Game Animation Sample update (blog dated 2026-08-12) adds Pose Search Interaction Assets, multi-character MM and a ragdoll pawn that gets up via MM. **[snippet only]** https://www.unrealengine.com/tech-blog/download-the-latest-game-animation-sample-project-now-updated-for-ue-5-8

---

## 5. Decision table

| # | Item | Category | One-line reason |
|---|---|---|---|
| 1 | CMC BrakingFriction / GroundFriction / MaxAcceleration / RotationRate (SHME-owned) | (1) usable now | Free, BP-settable, and it sets the capsule brake/turn that MM must match. |
| 2 | Pose Search DB + Continuing Pose Bias + Interrupt modes (InvalidateContinuingPose) | (1) usable now | Existing owner. A forced entry into a redirect DB at the decision frame is cheap. |
| 3 | Inertialization with a per-joint blend profile | (1) usable now | Cheap. Faster lower-body handover protects the plant foot. Avoid Dead Blending (experimental). |
| 4 | Orientation / Stride Warping (small ranges) | (1) usable now | Residual angle and speed fixes. They cannot create a pivot step. |
| 5 | NVIDIA MotionBricks (SOMA) as an **offline candidate-clip** generator | (2) needs adaptation | Commercial weights, **runs on Windows**, context-to-target interface fits. **Needs a SOMA skeleton we don't have** plus a SOMA to MetaHuman retarget and exporter. Kinematic, so no balance guarantee. |
| 6 | NVIDIA Kimodo (SOMA-SEED weights) offline with heading/root/keyframe constraints | (2) needs adaptation | Commercial (SOMA weights), Windows+Linux, offline clips up to 10 s. Same SOMA retarget need. Known foot skating. **SMPL-X weights are non-commercial.** |
| 7 | NVIDIA ARDY (SOMA checkpoints, 2026-10-15) | (3) experimental only | Commercial weights, but **Linux-only (tested)**, gated Llama-3-8B text encoder (~14 GB), SOMA weights about 2 weeks old. Kinematic, with no recovery examples. |
| 8 | Control Rig Full Body IK plant-foot / pelvis fixup | (2) needs adaptation | Works, but duplicates the FootPlacement/LegIK owner and adds iteration cost. |
| 9 | Motion Warping | (2) needs adaptation | Needs root-motion montages, which is a parallel path to MM/CMC. Only if redirects become montages. |
| 10 | Physics Control component | (3) experimental only | Maturity not stated in 5.8 docs. Spring/damper body drives give secondary reaction only, not balance. |
| 11 | Slope Warping / Dead Blending | (3) experimental only | Both documented as in development/experimental, not for shipping. |
| 12 | NVIDIA ProtoMotions (training or running policies) | (4) unnecessary cost | Physics RL needs IsaacLab (Linux) and multi-A100 training. Policies can't run in UE. Only its push/frame/inpainting **ideas** are useful. |
| 13 | Physical Animation component | (4) unnecessary cost | Experimental, simulated bodies and jitter risk, and it does nothing for the brake/support plan. |

Plain statements:
- **No ARDY, MotionBricks or Kimodo SOMA weight is non-commercial.** The Kimodo **SMPL-X** weights are.
- **ARDY is Linux-tested only. ProtoMotions' SOMA policies need IsaacLab on Linux.** MotionBricks and Kimodo list Windows.
- **All three generators use SOMA (or G1/Core), a skeleton SPHIRUS does not have.**
- **None of them guarantees physical balance.**
