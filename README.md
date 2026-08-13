# 🚌 1:1 Electric City Bus 3D Web App (Blender & Three.js)

An interactive 3D Web application built with **Three.js** and **Blender 5.2**, featuring 1:1 PBR car paint materials, crystal clear glass, custom livery graphics, and interactive controls.

## 🌟 Key Features
- **1:1 Livery & PBR Car Paint**: High-gloss car paint (`clearcoat: 1.0`), cyan geometric stripes, bold `CITY BUS` branding, and amber LED route board (`025 CENTRAL STATION`).
- **Blender 5.2 Automated Pipeline**: Generated procedurally via `generate_bus.py` and exported to `.glb` and `.blend`.
- **Crystal Transmission Glass**: Dual-sided physical glass (`transmission: 0.96`) revealing interior seats and handrails.
- **Interactive Controls**: Door sliding animations, pantograph trolley arm up/down, wheel rotation, and camera view presets.

## 📁 Repository Structure
- `index.html` - Interactive Three.js Web3D Application
- `generate_bus.py` - Blender 5.2 Python script for model generation & export
- `bus.glb` - Compiled 3D GLTF asset
- `bus.blend` - Native Blender 5.2 project file
- `bus_ref.jpg` - Original concept reference image

## 🚀 Quick Start
Serve locally with Python HTTP server:
```bash
python -m http.server 8080
```
Then open `http://localhost:8080` in your browser!
