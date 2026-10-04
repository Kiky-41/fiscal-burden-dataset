#!/usr/bin/env python3
"""Runs build_fiscal.py (build + validation checks). Run: python3 Fiscal-Burden-Dataset/build_all.py"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, 'build_fiscal.py')], cwd=HERE, check=True)
subprocess.run([sys.executable, os.path.join(HERE, 'build_news_updates.py')], cwd=HERE, check=True)
