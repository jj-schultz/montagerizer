#!/usr/bin/env python3
"""
Example showing how to use different timing configurations
"""
from create_movie import create_movie
import logging

logging.basicConfig(level=logging.INFO)

def create_fast_movie():
    """Example: Fast-paced movie with short durations"""
    print("\n=== Creating FAST-PACED movie ===")
    create_movie(
        images_short_dir="./files/images_short",
        images_long_dir="./files/images_long", 
        audio_path="./files/audio.mp3",
        output_path="./fast_movie.mp4",
        long_duration=2.0,           # Shorter long images
        short_start_duration=0.3,    # Very fast start
        short_end_duration=0.1       # Very fast end
    )

def create_slow_movie():
    """Example: Slow-paced movie with longer durations"""  
    print("\n=== Creating SLOW-PACED movie ===")
    create_movie(
        images_short_dir="./files/images_short",
        images_long_dir="./files/images_long",
        audio_path="./files/audio.mp3", 
        output_path="./slow_movie.mp4",
        long_duration=5.0,           # Longer long images
        short_start_duration=1.5,    # Slower start
        short_end_duration=0.5       # Slower end
    )

def create_uniform_movie():
    """Example: Uniform timing (no progression)"""
    print("\n=== Creating UNIFORM timing movie ===")
    create_movie(
        images_short_dir="./files/images_short",
        images_long_dir="./files/images_long",
        audio_path="./files/audio.mp3",
        output_path="./uniform_movie.mp4", 
        long_duration=3.0,           # Standard long images
        short_start_duration=0.5,    # Same start and end = no progression
        short_end_duration=0.5       # Same start and end = no progression
    )

if __name__ == "__main__":
    # Uncomment the example you want to run:
    
    create_fast_movie()
    # create_slow_movie() 
    # create_uniform_movie()