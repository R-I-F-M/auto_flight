# custom_dronekit.py
import sys
import importlib
import collections.abc

# Apply the patch before importing dronekit
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping

# Import the original dronekit library
dronekit = importlib.import_module('dronekit')

# Export all attributes from the dronekit module
globals().update(dronekit.__dict__)

# import custom_dronekit as dronekit

# from dronekit import connect, VehicleMode