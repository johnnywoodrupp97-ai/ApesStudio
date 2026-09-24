"""Space travel & planet transitions — No Man's Sky-style seamless flight.

One continuous world: take off, leave the atmosphere, pulse across the system, drop out,
enter another atmosphere and land, with no loading screens. Every transition is a short,
spectacular sequence that also hides streaming. Numbers here drive the per-planet
threshold tables (build.py) and the transition shells in the Blender planet scaffold.
"""

FLIGHT = {
    # Assisted flight (default): arcade handling scaled by the ship's build.
    "atmo_cruise_mps": (30, 250), "atmo_boost_mps": 400,
    "space_cruise_mps": 1200, "space_boost_mps": 2000,
    "airless_approach_cap_mps": 400,        # airless bodies: speed cap below the approach altitude
    "min_terrain_clearance_m": 15,          # assisted flight holds this height unless landing
    "landing_prompt_altitude_m": 150, "landing_max_slope_deg": 20, "auto_land_s": 6,
    "launch_lift_m": 30, "launch_s": 3, "launch_min_twr": 1.2,  # auto-launch needs TWR ≥ 1.2 in local gravity
    "entry_speed_ramp_s": 4, "entry_sequence_s": 8, "exit_sequence_s": 5,
    "dive_angle_deg": 45,
}

PULSE = {"spool_s": 3, "max_mps": 30000, "accel_s": 15, "min_altitude_frac": 0.5,
         "encounter_chance_per_min": 0.05, "dropout": "Automatic at a planet's pulse-dropout altitude, a station's 20 km bubble, or an encounter"}

JUMP = {"charge_s": 10, "tunnel_s": (8, 12), "arrival_km": (10, 20), "cooldown_s": 300,
        "arrival": "10–20 km from the destination system's station or beacon"}

THRESHOLDS = {
    # as fractions of planet radius R (altitudes above the surface unless noted)
    "streaming_start_frac": 6.0,     # distance from the centre where voxel clipmap streaming begins (impostor before)
    "pulse_dropout_frac": 0.5,       # altitude where pulse drive drops out / is blocked
    "airless_approach_frac": 0.15,   # altitude where the airless speed cap begins (Moon-type bodies)
    "cloud_layer_frac_of_atmo": 0.4, # cloud deck height as a fraction of atmosphere height
    "orbit_parking_frac": 0.25,      # capital ships park this far above the atmosphere top (fraction of R)
}

STATIONS = [
    ("Small hangar bay", "30 × 20 × 15 m", "Landers, fighters, small-grid ships"),
    ("Medium hangar bay", "60 × 40 × 25 m", "Medium ships; auto-dock inside the approach cone below 100 m/s"),
    ("Capital docking arm", "External clamp, 200 m clearance", "Large-grid capital ships (they never enter bays)"),
]
